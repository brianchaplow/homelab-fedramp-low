"""Assemble an OSCAL System Security Plan (SSP) from Trestle markdown.

This module is a thin wrapper around ``trestle author ssp-assemble``.
Plan 2 scope is to wire the assembly path without filling the 156
control markdown files — that is Plan 3's job. Running this with the
empty scaffold will either produce a minimal SSP or fail with a
Trestle-specific diagnostic; either outcome is informative for Plan 3.

Per ADR 0006 Amendment Task 4, Trestle 4.0.1 writes the markdown
scaffold to ``trestle-workspace/<ssp_name>/`` (top-level), NOT
``trestle-workspace/system-security-plans/<ssp_name>``. The ``-m``
flag points at the top-level directory name. The assembled output
lands under
``trestle-workspace/system-security-plans/<ssp_name>/system-security-plan.json``
and this module copies it to ``output_path`` so callers outside the
workspace can reference it.

**Trestle binary discovery:** the ``trestle`` command is installed as
a console script at ``.venv/Scripts/trestle.exe`` on Windows and
``.venv/bin/trestle`` on POSIX. Plan 2 cannot rely on it being on
``PATH`` because Git Bash on Windows does not activate the venv by
default. :func:`_find_trestle_binary` resolves the correct absolute
path at call time.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from pipelines.common.logging import get_logger


logger = get_logger(__name__)


def _find_trestle_binary() -> str:
    """Return an absolute path to the ``trestle`` executable.

    Resolution order:

    1. ``.venv/Scripts/trestle.exe`` relative to ``sys.executable``'s
       parent (Git Bash / CMD on Windows inside this project's venv).
    2. ``.venv/bin/trestle`` relative to ``sys.executable``'s parent
       (POSIX venv layout).
    3. ``shutil.which("trestle")`` as a last-resort PATH lookup.

    Raises :class:`FileNotFoundError` if none of the above resolve.
    """
    venv_scripts = Path(sys.executable).parent
    for candidate in (
        venv_scripts / "trestle.exe",
        venv_scripts / "trestle",
    ):
        if candidate.exists():
            return str(candidate)

    on_path = shutil.which("trestle")
    if on_path:
        return on_path

    raise FileNotFoundError(
        "trestle executable not found in venv or PATH — run "
        "`./pipelines.sh install` to reinstall dependencies"
    )


def build_ssp_assemble_cmd(
    ssp_name: str,
    component_defs: list[str] | None = None,
    trestle_binary: str = "trestle",
) -> list[str]:
    """Return the argv list for ``trestle author ssp-assemble``.

    Split out from :func:`assemble_ssp` so tests can assert the exact
    command shape without mocking subprocess. The default
    ``trestle_binary="trestle"`` keeps the bare-name form for tests
    that only inspect the argument layout; :func:`assemble_ssp` passes
    an absolute path discovered via :func:`_find_trestle_binary`.
    """
    cmd: list[str] = [
        trestle_binary,
        "author",
        "ssp-assemble",
        "-m",
        ssp_name,
        "-o",
        ssp_name,
    ]
    if component_defs:
        cmd.extend(["-cd", ",".join(component_defs)])
    return cmd


def assemble_ssp(
    ssp_name: str,
    workspace: Path,
    output_path: Path,
    component_defs: list[str] | None = None,
) -> Path:
    """Run ``trestle author ssp-assemble`` and copy the result out.

    Args:
        ssp_name: top-level markdown directory name inside ``workspace``
            (e.g. ``"mss-ssp"``).
        workspace: the trestle workspace root (contains ``catalogs/``,
            ``profiles/``, and ``<ssp_name>/``).
        output_path: where to copy the assembled SSP JSON.
        component_defs: optional list of component-definition names to
            include via the ``-cd`` flag.

    Returns:
        The ``output_path`` that was written.

    Raises:
        subprocess.CalledProcessError: if ``trestle`` returns non-zero.
        FileNotFoundError: if Trestle exits 0 but does not produce the
            expected ``system-security-plans/<ssp_name>/system-security-plan.json``.
    """
    cmd = build_ssp_assemble_cmd(
        ssp_name,
        component_defs=component_defs,
        trestle_binary=_find_trestle_binary(),
    )
    logger.info("invoking: %s (cwd=%s)", " ".join(cmd), workspace)
    result = subprocess.run(
        cmd,
        cwd=workspace,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.stdout:
        logger.info("trestle stdout: %s", result.stdout.strip())
    if result.stderr:
        logger.info("trestle stderr: %s", result.stderr.strip())

    assembled = (
        workspace / "system-security-plans" / ssp_name / "system-security-plan.json"
    )
    if not assembled.exists():
        raise FileNotFoundError(
            f"Trestle did not produce SSP at {assembled} — check for "
            f"unresolved control prose or missing compdefs"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(assembled, output_path)
    logger.info("copied assembled SSP to %s", output_path)
    return output_path
