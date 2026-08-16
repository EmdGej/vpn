#!/usr/bin/env bash

PANEL_USERNAME=""
PANEL_PASSWORD=""
PANEL_PORT=""
PANEL_WEB_BASE_PATH=""
PANEL_ACCESS_URL=""
PANEL_API_URL=""
PANEL_API_TOKEN=""

extract_panel_value() {
  local key="$1"

  grep -E "^${key}:" "${INSTALL_LOG}" \
    | tail -n 1 \
    | sed -E "s/^${key}:[[:space:]]*//" \
    | tr -d '\r'
}

parse_panel_installation() {
  PANEL_USERNAME="$(extract_panel_value "Username")"
  PANEL_PASSWORD="$(extract_panel_value "Password")"
  PANEL_PORT="$(extract_panel_value "Port")"
  PANEL_WEB_BASE_PATH="$(extract_panel_value "WebBasePath")"
  PANEL_ACCESS_URL="$(extract_panel_value "Access URL")"
  PANEL_API_TOKEN="$(extract_panel_value "API Token")"

  if [[ -z "${PANEL_PORT}" || -z "${PANEL_WEB_BASE_PATH}" || -z "${PANEL_ACCESS_URL}" || -z "${PANEL_API_TOKEN}" ]]; then
    echo "ERROR: failed to parse panel installation output" >&2
    echo "Check log: ${INSTALL_LOG}" >&2
    exit 1
  fi

  PANEL_API_URL="${PANEL_ACCESS_URL}/panel/api"

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
