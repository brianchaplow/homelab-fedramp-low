#!/usr/bin/env bash
#
# Pipeline / verification entry point for homelab-fedramp-low.
#
# Canonical entry point. Works on Git Bash (Windows, Python 3.14 native),
# WSL Ubuntu 22.04 (Python 3.10), and any POSIX Linux / macOS. The Makefile
# is a thin alias that calls into this script for systems that have make.
#
# Usage:
#   ./pipelines.sh help
#   ./pipelines.sh install
#   ./pipelines.sh smoke          # both tools
#   ./pipelines.sh smoke-dojo
#   ./pipelines.sh smoke-regscale
#   ./pipelines.sh clean
#
# Env is sourced from /c/Projects/.env on PITBOSS (or ~/.env on POSIX hosts).

set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

# Locate the env file — PITBOSS stores it in /c/Projects/.env per
# homelab convention. On POSIX hosts (WSL, Linux, macOS) fall back to
# the repo root .env then ~/.env.
find_env() {
  for p in /c/Projects/.env "$REPO_ROOT/.env" "$HOME/.env"; do
    if [ -f "$p" ]; then
      echo "$p"
      return 0
    fi
  done
  return 1
}

load_env() {
  local envfile
  envfile="$(find_env)" || { echo "ERROR: no .env file found" >&2; exit 1; }
  set -a
  # shellcheck disable=SC1090
  source "$envfile"
  set +a
}

# pip/python selection: prefer the local venv if present, fall back to
# system python. Git Bash venvs live under .venv/Scripts/, POSIX venvs
# under .venv/bin/.
VENV_PY=""
if [ -x ".venv/Scripts/python.exe" ]; then
  VENV_PY=".venv/Scripts/python.exe"
elif [ -x ".venv/bin/python" ]; then
  VENV_PY=".venv/bin/python"
fi

cmd="${1:-help}"
case "$cmd" in
  help)
    cat <<EOF
Infrastructure targets:
  install         Create .venv and install project + dev deps in editable mode
  test            Run the pytest suite
  smoke           Run all smoke checks (DefectDojo + RegScale)
  smoke-dojo      Check DefectDojo availability
  smoke-regscale  Check RegScale CE availability
  clean           Remove .venv and build artifacts

Pipeline targets (forwarded to pipelines.cli):
  inventory       Wazuh inventory → oscal/component-definition.json
  render-iiw     OSCAL component-def → inventory/IIW-<YYYY-MM>.xlsx
  ingest-findings Wazuh indexer vulns → DefectDojo (grouped by product)
  build-poam     DefectDojo findings → oscal/poam.json
  render-poam    OSCAL POA&M → poam/POAM-<YYYY-MM>.xlsx
  oscal          Composite: inventory + build-poam
  conmon         Full monthly cycle: ingest-findings + oscal + render-iiw + render-poam
EOF
    ;;

  test)
    if [ -z "$VENV_PY" ]; then
      echo "ERROR: no .venv — run ./pipelines.sh install first" >&2
      exit 1
    fi
    # Use the POSIX-style pytest binary when present, else module mode.
    if [ -x ".venv/Scripts/pytest.exe" ]; then
      ".venv/Scripts/pytest.exe" tests/ "$@"
    elif [ -x ".venv/bin/pytest" ]; then
      ".venv/bin/pytest" tests/ "$@"
    else
      "$VENV_PY" -m pytest tests/ "$@"
    fi
    ;;

  install)
    if [ -z "$VENV_PY" ]; then
      echo "Creating .venv..."
      python -m venv .venv
      if [ -x ".venv/Scripts/python.exe" ]; then
        VENV_PY=".venv/Scripts/python.exe"
      elif [ -x ".venv/bin/python" ]; then
        VENV_PY=".venv/bin/python"
      fi
    fi
    "$VENV_PY" -m pip install --upgrade pip
    "$VENV_PY" -m pip install -e ".[dev]"
    "$VENV_PY" -c "import trestle; print('Trestle', trestle.__version__ if hasattr(trestle,'__version__') else 'unknown')"
    echo "install OK"
    ;;

  smoke)
    load_env
    ./tests/smoke/check_defectdojo.sh
    ./tests/smoke/check_regscale.sh
    echo "All smoke checks passed."
    ;;

  smoke-dojo)
    load_env
    ./tests/smoke/check_defectdojo.sh
    ;;

  smoke-regscale)
    load_env
    ./tests/smoke/check_regscale.sh
    ;;

  clean)
    rm -rf .venv build dist ./*.egg-info .pytest_cache
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    echo "clean OK"
    ;;

  *)
    # Unknown commands forward to the Click CLI (ADR 0006 Deviation 2).
    # Every pipeline subcommand (inventory, render-iiw, ingest-findings,
    # build-poam, render-poam, oscal, conmon) lands here and is executed
    # by pipelines/cli.py via the same venv that pipelines.sh selected.
    if [ -z "$VENV_PY" ]; then
      echo "ERROR: no .venv — run ./pipelines.sh install first" >&2
      exit 1
    fi
    load_env
    shift
    exec "$VENV_PY" -m pipelines.cli "$cmd" "$@"
    ;;
esac
