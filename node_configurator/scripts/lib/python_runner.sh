#!/usr/bin/env bash

PYTHON_MODULE="xui_node_configurator.main"

run_python_configurator() {
  if [[ -z "${GENERATED_YAML_FILE}" ]]; then
    echo "ERROR: GENERATED_YAML_FILE is empty" >&2
    exit 1
  fi

  echo
  echo "Running Python configurator..."
  echo "  module: ${PYTHON_MODULE}"
  echo "  config: ${GENERATED_YAML_FILE}"

  cd "${PROJECT_ROOT}"

  python3 -m "${PYTHON_MODULE}" \
    --config "${GENERATED_YAML_FILE}"
}
