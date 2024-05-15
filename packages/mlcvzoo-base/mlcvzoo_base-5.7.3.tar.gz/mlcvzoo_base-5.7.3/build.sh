#!/bin/sh

TARGET_PYTHON_VERSION=$(python3 -c 'import platform;print("".join(platform.python_version().split(".")[0:2]))')

REQUIREMENTS_FILE="${REQUIREMENTS_FILE:=./requirements_locked/requirements-lock-uv-py$TARGET_PYTHON_VERSION-all.txt}"

uv pip sync "$REQUIREMENTS_FILE"
