#!/usr/bin/env bash

require_command() {
  local cmd="$1"

  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "ERROR: command not found: ${cmd}" >&2
    exit 1
  fi
}

check_dependencies() {
  require_command bash
  require_command curl
  require_command grep
  require_command sed
  require_command python3
}
