#!/usr/bin/env bash

TEMPLATE_FILE="${PROJECT_ROOT}/templates/slave.yaml.tpl"
GENERATED_YAML_DIR="${PROJECT_ROOT}/xui_node_configurator/yamls"
GENERATED_YAML_FILE=""

yaml_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

render_server_names_yaml() {
  local csv="$1"
  local result=""
  local item=""

  IFS=',' read -ra items <<< "${csv}"

  for item in "${items[@]}"; do
    item="$(echo "${item}" | xargs)"
    if [[ -n "${item}" ]]; then
      result="${result}          - \"$(yaml_escape "${item}")\""$'\n'
    fi
  done

  printf '%s' "${result}"
}

generate_slave_yaml() {
  mkdir -p "${GENERATED_YAML_DIR}"

  if [[ ! -f "${TEMPLATE_FILE}" ]]; then
    echo "ERROR: YAML template not found: ${TEMPLATE_FILE}" >&2
    exit 1
  fi

  GENERATED_YAML_FILE="${GENERATED_YAML_DIR}/${NODE_ID}.yaml"

  local server_names_yaml
  server_names_yaml="$(render_server_names_yaml "${REALITY_SERVER_NAMES}")"

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

  python3 - <<PY
from pathlib import Path

path = Path("${GENERATED_YAML_FILE}")
content = path.read_text()
content = content.replace("__REALITY_SERVER_NAMES__\n", """${server_names_yaml}""")
path.write_text(content)
PY

  chmod 600 "${GENERATED_YAML_FILE}"

  echo
  echo "Generated slave YAML:"
  echo "  ${GENERATED_YAML_FILE}"
}
