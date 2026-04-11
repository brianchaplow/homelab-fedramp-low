"""Structured logging for FedRAMP pipelines.

Every pipeline entry point calls :func:`get_logger` exactly once at startup
and shares the returned instance. The logger writes to stderr with a fixed
format ``<timestamp> <level> [<name>] <message>`` that is both human-
readable for interactive runs and easy to parse for later log shipping.

Handlers are attached idempotently -- a second call to :func:`get_logger`
with the same name returns the existing logger without stacking duplicate
handlers. ``propagate`` is disabled so messages do not double-print via the
root logger if the host application also configures logging.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path


_FORMAT: str = "%(asctime)s %(levelname)-7s [%(name)s] %(message)s"
_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"


def get_logger(name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """Return a configured stderr logger.

    Args:
        name: Logger name. If ``None``, the basename of ``sys.argv[0]`` is
            used (falling back to ``"pipeline"`` for bare interpreters).
        level: Logging level. Defaults to :data:`logging.INFO`.

    Returns:
        A :class:`logging.Logger` with a single stderr handler, the
        pipeline format, propagation disabled, and the requested level.
    """
    if name is None:
        name = Path(sys.argv[0]).stem if sys.argv and sys.argv[0] else "pipeline"

    logger = logging.getLogger(name)
    if logger.handlers:
        # Already configured -- return it without stacking another handler.
        return logger

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATE_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
