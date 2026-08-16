#!/usr/bin/env bash

ROLE=""

PANEL_ID=""

NODE_ID=""
NODE_REMARK=""

PARENT_PANEL_ID=""
PARENT_API_URL=""
PARENT_API_TOKEN=""

INBOUND_PORT=""
REALITY_TARGET=""
REALITY_SERVER_NAMES=""
REALITY_FINGERPRINT=""
SHORT_IDS_COUNT=""
SPIDER_X_LENGTH=""

RUN_CONFIGURATOR="true"

usage() {
  cat <<EOF
Usage:

  Install master:
    ./scripts/install_node.sh \\
      --master \\
      --panel-id <master_panel_id>

  Install slave:
    ./scripts/install_node.sh \\
      --slave \\
      --panel-id <slave_panel_id> \\
      --node-id <slave_node_id> \\
      --node-remark <slave_node_remark> \\
      --parent-panel-id <master_panel_id> \\
      --parent-api-url <https://MASTER_IP:PORT/WEBBASEPATH/panel/api> \\
      --parent-api-token <MASTER_API_TOKEN> \\
      --inbound-port <port> \\
      --reality-target <reality_target> \\
      --reality-server-names <reality_server_names> \\
      --fingerprint <fingerprint> \\
      --short-ids-count <short_ids_count> \\
      --spider-x-length <spider_x_length>

Options:
  --master                         Install this server as master
  --slave                          Install this server as slave

  --panel-id VALUE                 ID for this installed panel. Required.

  --node-id VALUE                  Slave node id. Required for --slave.
  --node-remark VALUE              Slave node remark. Required for --slave.

  --parent-panel-id VALUE          Parent/master panel id. Required for --slave.
  --parent-api-url VALUE           Parent/master panel API URL. Required for --slave.
  --parent-api-token VALUE         Parent/master panel API token. Required for --slave.

  --inbound-port VALUE             Inbound port. Required for --slave.
  --reality-target VALUE           Reality target. Required for --slave.
  --reality-server-names VALUE     Comma-separated SNI list. Required for --slave.
  --fingerprint VALUE              Reality fingerprint. Required for --slave.
  --short-ids-count VALUE          ShortIds count. Required for --slave.
  --spider-x-length VALUE          SpiderX length. Required for --slave.

  --no-run                         Generate YAML but do not run Python configurator
  -h, --help                       Show help
EOF
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --master)
        ROLE="master"
        shift
        ;;
      --slave)
        ROLE="slave"
        shift
        ;;
      --panel-id)
        PANEL_ID="$2"
        shift 2
        ;;
      --node-id)
        NODE_ID="$2"
        shift 2
        ;;
      --node-remark)
        NODE_REMARK="$2"
        shift 2
        ;;
      --parent-panel-id)
        PARENT_PANEL_ID="$2"
        shift 2
        ;;
      --parent-api-url)
        PARENT_API_URL="$2"
        shift 2
        ;;
      --parent-api-token)
        PARENT_API_TOKEN="$2"
        shift 2
        ;;
      --inbound-port)
        INBOUND_PORT="$2"
        shift 2
        ;;
      --reality-target)
        REALITY_TARGET="$2"
        shift 2
        ;;
      --reality-server-names)
        REALITY_SERVER_NAMES="$2"
        shift 2
        ;;
      --fingerprint)
        REALITY_FINGERPRINT="$2"
        shift 2
        ;;
      --short-ids-count)
        SHORT_IDS_COUNT="$2"
        shift 2
        ;;
      --spider-x-length)
        SPIDER_X_LENGTH="$2"
        shift 2
        ;;
      --no-run)
        RUN_CONFIGURATOR="false"
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "ERROR: unknown argument: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  validate_args
}

require_arg() {
  local value="$1"
  local name="$2"

  if [[ -z "${value}" ]]; then
    echo "ERROR: ${name} is required" >&2
    usage
    exit 1
  fi
}

validate_positive_int() {
  local value="$1"
  local name="$2"

  if ! [[ "${value}" =~ ^[0-9]+$ ]]; then
    echo "ERROR: ${name} must be a positive integer" >&2
    exit 1
  fi

  if [[ "${value}" -lt 1 ]]; then
    echo "ERROR: ${name} must be greater than 0" >&2
    exit 1
  fi
}

validate_args() {
  require_arg "${ROLE}" "--master or --slave"
  require_arg "${PANEL_ID}" "--panel-id"

  if [[ "${ROLE}" != "master" && "${ROLE}" != "slave" ]]; then
    echo "ERROR: role must be master or slave" >&2
    exit 1
  fi

  if [[ "${ROLE}" == "slave" ]]; then
    require_arg "${NODE_ID}" "--node-id"
    require_arg "${NODE_REMARK}" "--node-remark"

    require_arg "${PARENT_PANEL_ID}" "--parent-panel-id"
    require_arg "${PARENT_API_URL}" "--parent-api-url"
    require_arg "${PARENT_API_TOKEN}" "--parent-api-token"

    require_arg "${INBOUND_PORT}" "--inbound-port"
    require_arg "${REALITY_TARGET}" "--reality-target"
    require_arg "${REALITY_SERVER_NAMES}" "--reality-server-names"
    require_arg "${REALITY_FINGERPRINT}" "--fingerprint"
    require_arg "${SHORT_IDS_COUNT}" "--short-ids-count"
    require_arg "${SPIDER_X_LENGTH}" "--spider-x-length"

    validate_positive_int "${INBOUND_PORT}" "--inbound-port"
    validate_positive_int "${SHORT_IDS_COUNT}" "--short-ids-count"
    validate_positive_int "${SPIDER_X_LENGTH}" "--spider-x-length"
  fi
}
