.PHONY: help smoke smoke-dojo smoke-regscale install clean venv-win

# Canonical entry point is pipelines.sh -- this Makefile is a thin alias for
# POSIX systems (Linux, WSL, macOS) that have make. Git Bash on Windows does
# not ship make; use ./pipelines.sh instead.

help:
	@./pipelines.sh help

smoke:
	@./pipelines.sh smoke

smoke-dojo:
	@./pipelines.sh smoke-dojo

smoke-regscale:
	@./pipelines.sh smoke-regscale

install:
	@./pipelines.sh install

clean:
	@./pipelines.sh clean
