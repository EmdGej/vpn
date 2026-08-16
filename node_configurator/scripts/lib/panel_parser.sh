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
  if [[ ! -f "${XUI_INSTALL_RESULT_FILE}" ]]; then
    echo "ERROR: x-ui install result file not found: ${XUI_INSTALL_RESULT_FILE}" >&2
    echo "Run installer first or do not use --skip-install." >&2
    exit 1
  fi

  read_panel_install_result
  validate_panel_values

  PANEL_API_URL="${PANEL_ACCESS_URL}/panel/api"

  print_panel_info
}

read_env_value() {
  local key="$1"

  grep -E "^${key}=" "${XUI_INSTALL_RESULT_FILE}" \
    | tail -n 1 \
    | sed -E "s/^${key}=//" \
    | sed -E 's/^"//; s/"$//' \
    | tr -d '\r'
}

read_panel_install_result() {
  echo "Reading panel parameters from ${XUI_INSTALL_RESULT_FILE}"

  PANEL_USERNAME="$(read_env_value "XUI_USERNAME")"
  PANEL_PASSWORD="$(read_env_value "XUI_PASSWORD")"
  PANEL_PORT="$(read_env_value "XUI_PANEL_PORT")"
  PANEL_WEB_BASE_PATH="$(read_env_value "XUI_WEB_BASE_PATH")"
  PANEL_ACCESS_URL="$(read_env_value "XUI_ACCESS_URL")"
  PANEL_API_TOKEN="$(read_env_value "XUI_API_TOKEN")"
}

validate_panel_values() {
  if [[ -z "${PANEL_USERNAME}" ]]; then
    echo "ERROR: failed to parse XUI_USERNAME" >&2
    exit 1
  fi

  if [[ -z "${PANEL_PASSWORD}" ]]; then
    echo "ERROR: failed to parse XUI_PASSWORD" >&2
    exit 1
  fi

  if [[ -z "${PANEL_PORT}" ]]; then
    echo "ERROR: failed to parse XUI_PANEL_PORT" >&2
    exit 1
  fi

  if [[ -z "${PANEL_WEB_BASE_PATH}" ]]; then
    echo "ERROR: failed to parse XUI_WEB_BASE_PATH" >&2
    exit 1
  fi

  if [[ -z "${PANEL_ACCESS_URL}" ]]; then
    echo "ERROR: failed to parse XUI_ACCESS_URL" >&2
    exit 1
  fi

  if [[ -z "${PANEL_API_TOKEN}" ]]; then
    echo "ERROR: failed to parse XUI_API_TOKEN" >&2
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
