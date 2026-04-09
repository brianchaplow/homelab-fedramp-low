"""Tests for pipelines.common.config — env loader.

Covers ADR 0006 Deviations 3 (HTTPS validator scoped to Wazuh endpoints
only) and 4 (hybrid env var defaults with secrets-only REQUIRED_ENV_VARS).
"""
from __future__ import annotations

import pytest

from pipelines.common.config import (
    Config,
    REQUIRED_ENV_VARS,
    WAZUH_API_URL_DEFAULT,
    WAZUH_API_USER_DEFAULT,
    WAZUH_INDEXER_URL_DEFAULT,
    WAZUH_INDEXER_USER_DEFAULT,
    load_config,
)


def _set_required(monkeypatch: pytest.MonkeyPatch) -> None:
    """Populate the seven secrets-only required env vars."""
    monkeypatch.setenv("WAZUH_API_PASSWORD", "wapi-secret")
    monkeypatch.setenv("WAZUH_INDEXER_PASSWORD", "widx-secret")
    monkeypatch.setenv("DEFECTDOJO_URL", "http://10.10.30.27:8080")
    monkeypatch.setenv("DEFECTDOJO_API_KEY", "dd-key")
    monkeypatch.setenv("REGSCALE_URL", "http://10.10.30.28")
    monkeypatch.setenv("REGSCALE_USERNAME", "admin")
    monkeypatch.setenv("REGSCALE_PASSWORD", "rs-secret")


def _clear_all(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove every env var that load_config consults."""
    for var in (
        "WAZUH_API_URL",
        "WAZUH_API_USER",
        "WAZUH_API_PASSWORD",
        "WAZUH_INDEXER_URL",
        "WAZUH_INDEXER_USER",
        "WAZUH_INDEXER_PASSWORD",
        "DEFECTDOJO_URL",
        "DEFECTDOJO_API_KEY",
        "REGSCALE_URL",
        "REGSCALE_USERNAME",
        "REGSCALE_PASSWORD",
    ):
        monkeypatch.delenv(var, raising=False)


def test_load_config_reads_required_secrets_and_applies_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Load with only the required secrets set — architectural constants fill in."""
    _clear_all(monkeypatch)
    _set_required(monkeypatch)

    cfg = load_config()

    assert isinstance(cfg, Config)
    # Architectural defaults (from code, per ADR 0006 Deviation 4)
    assert cfg.wazuh_api_url == WAZUH_API_URL_DEFAULT
    assert cfg.wazuh_api_user == WAZUH_API_USER_DEFAULT
    assert cfg.wazuh_indexer_url == WAZUH_INDEXER_URL_DEFAULT
    assert cfg.wazuh_indexer_user == WAZUH_INDEXER_USER_DEFAULT
    # Secrets from env
    assert cfg.wazuh_api_password == "wapi-secret"
    assert cfg.wazuh_indexer_password == "widx-secret"
    assert cfg.defectdojo_url == "http://10.10.30.27:8080"
    assert cfg.defectdojo_api_key == "dd-key"
    assert cfg.regscale_url == "http://10.10.30.28"
    assert cfg.regscale_username == "admin"
    assert cfg.regscale_password == "rs-secret"


def test_load_config_env_overrides_architectural_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A fork targeting a different Wazuh host overrides via env vars."""
    _clear_all(monkeypatch)
    _set_required(monkeypatch)
    monkeypatch.setenv("WAZUH_API_URL", "https://wazuh.example.org:55000")
    monkeypatch.setenv("WAZUH_API_USER", "ci-bot")
    monkeypatch.setenv("WAZUH_INDEXER_URL", "https://indexer.example.org:9200")
    monkeypatch.setenv("WAZUH_INDEXER_USER", "ci-reader")

    cfg = load_config()

    assert cfg.wazuh_api_url == "https://wazuh.example.org:55000"
    assert cfg.wazuh_api_user == "ci-bot"
    assert cfg.wazuh_indexer_url == "https://indexer.example.org:9200"
    assert cfg.wazuh_indexer_user == "ci-reader"


def test_load_config_missing_required_raises_with_each_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every missing required var is named in the error."""
    _clear_all(monkeypatch)

    with pytest.raises(ValueError, match="missing required env"):
        load_config()

    # Exercise partial-set: all-but-one missing → error still raised
    _set_required(monkeypatch)
    monkeypatch.delenv("REGSCALE_PASSWORD", raising=False)
    with pytest.raises(ValueError, match="REGSCALE_PASSWORD"):
        load_config()


def test_required_env_vars_tuple_matches_adr_0006(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """REQUIRED_ENV_VARS is the canonical secrets-only tuple from ADR 0006."""
    assert REQUIRED_ENV_VARS == (
        "WAZUH_API_PASSWORD",
        "WAZUH_INDEXER_PASSWORD",
        "DEFECTDOJO_URL",
        "DEFECTDOJO_API_KEY",
        "REGSCALE_URL",
        "REGSCALE_USERNAME",
        "REGSCALE_PASSWORD",
    )


def test_https_validator_accepts_https_wazuh_endpoints(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Wazuh endpoints must use https:// (ADR 0006 Deviation 3)."""
    _clear_all(monkeypatch)
    _set_required(monkeypatch)
    # Defaults are already https — load should succeed
    cfg = load_config()
    assert cfg.wazuh_api_url.startswith("https://")
    assert cfg.wazuh_indexer_url.startswith("https://")


def test_https_validator_rejects_http_wazuh_api_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """wazuh_api_url must be https://."""
    _clear_all(monkeypatch)
    _set_required(monkeypatch)
    monkeypatch.setenv("WAZUH_API_URL", "http://10.10.20.30:55000")
    with pytest.raises(ValueError, match="https"):
        load_config()


def test_https_validator_rejects_http_wazuh_indexer_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """wazuh_indexer_url must be https://."""
    _clear_all(monkeypatch)
    _set_required(monkeypatch)
    monkeypatch.setenv("WAZUH_INDEXER_URL", "http://10.10.20.30:9200")
    with pytest.raises(ValueError, match="https"):
        load_config()


def test_defectdojo_and_regscale_accept_http(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DefectDojo and RegScale run http:// in lab — validator must not reject.

    ADRs 0003 (RegScale CE port 80) and 0004 (DefectDojo bundled nginx no TLS)
    are the source of this asymmetry. ADR 0006 Deviation 3 scopes the HTTPS
    validator to Wazuh endpoints only.
    """
    _clear_all(monkeypatch)
    _set_required(monkeypatch)
    # Already http:// in _set_required — a plain load must succeed
    cfg = load_config()
    assert cfg.defectdojo_url.startswith("http://")
    assert cfg.regscale_url.startswith("http://")


def test_config_is_frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    """Config is immutable — downstream code cannot mutate loaded settings."""
    _clear_all(monkeypatch)
    _set_required(monkeypatch)
    cfg = load_config()
    with pytest.raises((TypeError, ValueError)):
        cfg.wazuh_api_password = "tampered"  # type: ignore[misc]


def test_no_regscale_api_key_field() -> None:
    """RegScale CE has no long-lived API key (ADR 0006 Deviation 7)."""
    assert "regscale_api_key" not in Config.model_fields
    assert "REGSCALE_API_KEY" not in REQUIRED_ENV_VARS
