#!/usr/bin/env bash

XUI_INSTALL_RESULT_FILE="/etc/x-ui/install-result.env"

PANEL_USERNAME=""
PANEL_PASSWORD=""
PANEL_PORT=""
PANEL_WEB_BASE_PATH=""
PANEL_ACCESS_URL=""
PANEL_API_URL=""
PANEL_API_TOKEN=""

parse_panel_installation() {
  if [[ -f "${XUI_INSTALL_RESULT_FILE}" ]]; then
    parse_panel_from_install_result_env
  else
    parse_panel_from_install_log
  fi

  validate_panel_values

  PANEL_API_URL="${PANEL_ACCESS_URL}/panel/api"

  print_panel_info
}

parse_panel_from_install_result_env() {
  echo "Reading panel parameters from ${XUI_INSTALL_RESULT_FILE}"

  # shellcheck disable=SC1090
  source "${XUI_INSTALL_RESULT_FILE}"

  PANEL_USERNAME="${USERNAME:-${PANEL_USERNAME:-}}"
  PANEL_PASSWORD="${PASSWORD:-${PANEL_PASSWORD:-}}"
  PANEL_PORT="${PORT:-${PANEL_PORT:-}}"
  PANEL_WEB_BASE_PATH="${WEB_BASE_PATH:-${WEBBASEPATH:-${PANEL_WEB_BASE_PATH:-}}}"
  PANEL_ACCESS_URL="${ACCESS_URL:-${PANEL_ACCESS_URL:-}}"
  PANEL_API_TOKEN="${API_TOKEN:-${PANEL_API_TOKEN:-}}"
}

extract_panel_value() {
  local key="$1"

  grep -E "^[[:space:]]*${key}:[[:space:]]*" "${INSTALL_LOG}" \
    | tail -n 1 \
    | sed -E "s/^[[:space:]]*${key}:[[:space:]]*//" \
    | tr -d '\r'
}

parse_panel_from_install_log() {
  echo "Reading panel parameters from ${INSTALL_LOG}"

  if [[ ! -f "${INSTALL_LOG}" ]]; then
    echo "ERROR: install log not found: ${INSTALL_LOG}" >&2
    exit 1
  fi

  PANEL_USERNAME="$(extract_panel_value "Username")"
  PANEL_PASSWORD="$(extract_panel_value "Password")"
  PANEL_PORT="$(extract_panel_value "Port")"
  PANEL_WEB_BASE_PATH="$(extract_panel_value "WebBasePath")"
  PANEL_ACCESS_URL="$(extract_panel_value "Access URL")"
  PANEL_API_TOKEN="$(extract_panel_value "API Token")"
}

validate_panel_values() {
  if [[ -z "${PANEL_USERNAME}" ]]; then
    echo "ERROR: failed to parse panel username" >&2
    exit 1
  fi

  if [[ -z "${PANEL_PASSWORD}" ]]; then
    echo "ERROR: failed to parse panel password" >&2
    exit 1
  fi

  if [[ -z "${PANEL_PORT}" ]]; then
    echo "ERROR: failed to parse panel port" >&2
    exit 1
  fi

  if [[ -z "${PANEL_WEB_BASE_PATH}" ]]; then
    echo "ERROR: failed to parse panel web base path" >&2
    exit 1
  fi

  if [[ -z "${PANEL_ACCESS_URL}" ]]; then
    echo "ERROR: failed to parse panel access URL" >&2
    exit 1
  fi

  if [[ -z "${PANEL_API_TOKEN}" ]]; then
    echo "ERROR: failed to parse panel API token" >&2
    exit 1
  fi
}

print_panel_info() {
  echo
  echo "Parsed panel:"
  echo "  panelId:     ${PANEL_ID}"
  echo "  username:    ${PANEL_USERNAME}"
  echo "  password:    ${PANEL_PASSWORD}"
  echo "  port:        ${PANEL_PORT}"
  echo "  webBasePath: ${PANEL_WEB_BASE_PATH}"
  echo "  accessUrl:   ${PANEL_ACCESS_URL}"
  echo "  apiUrl:      ${PANEL_API_URL}"
  echo "  apiToken:    ${PANEL_API_TOKEN}"
}
