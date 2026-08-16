#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LIB_DIR="${SCRIPT_DIR}/lib"

source "${LIB_DIR}/args.sh"
source "${LIB_DIR}/checks.sh"
source "${LIB_DIR}/installer.sh"
source "${LIB_DIR}/panel_parser.sh"
source "${LIB_DIR}/panel_env.sh"
source "${LIB_DIR}/yaml_generator.sh"
source "${LIB_DIR}/python_runner.sh"

main() {
  parse_args "$@"
  check_dependencies

  install_3xui
  parse_panel_installation
  save_current_panel_env

  if [[ "${ROLE}" == "master" ]]; then
    echo
    echo "Master panel installed."
    echo "Panel parameters saved to: ${PANEL_ENV_FILE}"
    echo "Python configurator was not started."
    exit 0
  fi

  if [[ "${ROLE}" == "slave" ]]; then
    generate_slave_yaml

    if [[ "${RUN_CONFIGURATOR}" == "true" ]]; then
      run_python_configurator
    else
      echo "Skipping Python configurator because --no-run was specified."
    fi

    exit 0
  fi
}

main "$@"
