"""Tests for pipelines.common.logging -- structured logger factory."""
from __future__ import annotations

import logging

import pytest

from pipelines.common.logging import get_logger


def test_get_logger_returns_logger_instance() -> None:
    logger = get_logger("test_pipeline")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_pipeline"


def test_get_logger_attaches_exactly_one_stderr_handler() -> None:
    logger = get_logger("test_handler_count")
    # Calling a second time must not attach a duplicate handler.
    _ = get_logger("test_handler_count")
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_get_logger_does_not_propagate_to_root() -> None:
    logger = get_logger("test_no_propagate")
    assert logger.propagate is False


def test_get_logger_default_level_is_info() -> None:
    logger = get_logger("test_default_level")
    assert logger.level == logging.INFO


def test_get_logger_respects_explicit_level() -> None:
    logger = get_logger("test_debug_level", level=logging.DEBUG)
    assert logger.level == logging.DEBUG


def test_get_logger_formats_messages_with_name_and_level(
    capsys: pytest.CaptureFixture[str],
) -> None:
    logger = get_logger("fmt_test")
    logger.info("hello world")
    captured = capsys.readouterr()
    # Handler writes to stderr
    assert "hello world" in captured.err
    assert "fmt_test" in captured.err
    assert "INFO" in captured.err
