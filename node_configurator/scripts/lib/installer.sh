#!/usr/bin/env bash

INSTALL_LOG="${PROJECT_ROOT}/3xui_install.log"
INSTALL_URL="https://raw.githubusercontent.com/MHSanaei/3x-ui/master/install.sh"

install_3xui() {
  echo "Installing 3x-ui..."
  echo "Install log: ${INSTALL_LOG}"

  bash <(curl -Ls "${INSTALL_URL}") 2>&1 | tee "${INSTALL_LOG}"
}
