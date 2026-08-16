#!/usr/bin/env bash

TEMPLATE_FILE="${PROJECT_ROOT}/templates/slave.yaml.tpl"
GENERATED_YAML_DIR="${PROJECT_ROOT}/xui_node_configurator/yamls"
GENERATED_YAML_FILE=""

yaml_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

render_server_names_yaml_to_file() {
  local csv="$1"
  local output_file="$2"
  local item=""

  : > "${output_file}"

  IFS=',' read -ra items <<< "${csv}"

  for item in "${items[@]}"; do
    item="$(echo "${item}" | xargs)"
    if [[ -n "${item}" ]]; then
      printf '          - "%s"\n' "$(yaml_escape "${item}")" >> "${output_file}"
    fi
  done
}

generate_slave_yaml() {
  mkdir -p "${GENERATED_YAML_DIR}"

  if [[ ! -f "${TEMPLATE_FILE}" ]]; then
    echo "ERROR: YAML template not found: ${TEMPLATE_FILE}" >&2
    exit 1
  fi

  GENERATED_YAML_FILE="${GENERATED_YAML_DIR}/${NODE_ID}.yaml"

  local server_names_file
  server_names_file="$(mktemp)"

  render_server_names_yaml_to_file "${REALITY_SERVER_NAMES}" "${server_names_file}"

  cp "${TEMPLATE_FILE}" "${GENERATED_YAML_FILE}"

  sed -i.bak \
    -e "s|__NODE_ID__|$(yaml_escape "${NODE_ID}")|g" \
    -e "s|__NODE_REMARK__|$(yaml_escape "${NODE_REMARK}")|g" \
    -e "s|__PARENT_PANEL_ID__|$(yaml_escape "${PARENT_PANEL_ID}")|g" \
    -e "s|__SLAVE_API_URL__|$(yaml_escape "${PANEL_API_URL}")|g" \
    -e "s|__SLAVE_API_TOKEN__|$(yaml_escape "${PANEL_API_TOKEN}")|g" \
    -e "s|__PARENT_PANEL_API_URL__|$(yaml_escape "${PARENT_API_URL}")|g" \
    -e "s|__PARENT_PANEL_API_TOKEN__|$(yaml_escape "${PARENT_API_TOKEN}")|g" \
    -e "s|__INBOUND_PORT__|${INBOUND_PORT}|g" \
    -e "s|__INBOUND_REMARK__|$(yaml_escape "${NODE_ID}-vless-reality-${INBOUND_PORT}")|g" \
    -e "s|__REALITY_TARGET__|$(yaml_escape "${REALITY_TARGET}")|g" \
    -e "s|__REALITY_FINGERPRINT__|$(yaml_escape "${REALITY_FINGERPRINT}")|g" \
    -e "s|__SHORT_IDS_COUNT__|${SHORT_IDS_COUNT}|g" \
    -e "s|__SPIDER_X_LENGTH__|${SPIDER_X_LENGTH}|g" \
    "${GENERATED_YAML_FILE}"

  rm -f "${GENERATED_YAML_FILE}.bak"

  local result_file
  result_file="$(mktemp)"

  while IFS= read -r line; do
    if [[ "${line}" == "__REALITY_SERVER_NAMES__" ]]; then
      cat "${server_names_file}" >> "${result_file}"
    else
      printf '%s\n' "${line}" >> "${result_file}"
    fi
  done < "${GENERATED_YAML_FILE}"

  mv "${result_file}" "${GENERATED_YAML_FILE}"
  rm -f "${server_names_file}"

  chmod 600 "${GENERATED_YAML_FILE}"

  echo
  echo "Generated slave YAML:"
  echo "  ${GENERATED_YAML_FILE}"
}
