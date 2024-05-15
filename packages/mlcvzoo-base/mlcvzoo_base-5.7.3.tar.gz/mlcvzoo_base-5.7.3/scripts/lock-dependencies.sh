#!/bin/bash

TARGET_PYTHON_VERSION=$(python3 -c 'import platform;print("".join(platform.python_version().split(".")[0:2]))')

uv pip compile -U \
  pyproject.toml \
  --extra dev \
  --output-file "requirements_locked/requirements-lock-uv-py$TARGET_PYTHON_VERSION-all.txt"

uv pip compile -U \
  pyproject.toml \
  --output-file "requirements_locked/requirements-lock-uv-py$TARGET_PYTHON_VERSION-without-dev.txt"
