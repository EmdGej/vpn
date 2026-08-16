#!/usr/bin/env bash

INSTALL_LOG="${PROJECT_ROOT}/3xui_install.log"
INSTALL_URL="https://raw.githubusercontent.com/MHSanaei/3x-ui/master/install.sh"

install_3xui() {
  echo "Installing 3x-ui..."
  echo "Install log: ${INSTALL_LOG}"

  if [[ "${AUTO_INSTALL}" == "true" ]]; then
    install_3xui_auto
    return
  fi

  install_3xui_manual
}

install_3xui_manual() {
  echo "Installer mode: manual"

  bash <(curl -Ls "${INSTALL_URL}") 2>&1 | tee "${INSTALL_LOG}"
}

install_3xui_auto() {
  echo "Installer mode: auto"
  echo "Answer file: ${INSTALL_ANSWER_FILE}"

  cat "${INSTALL_ANSWER_FILE}" \
    | bash <(curl -Ls "${INSTALL_URL}") 2>&1 \
    | tee "${INSTALL_LOG}"
}
