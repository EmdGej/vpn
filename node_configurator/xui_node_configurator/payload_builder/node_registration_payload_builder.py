from enum import StrEnum
from urllib.parse import urlparse

from xui_node_configurator.config import TNodeRegistrationConfig


class TNodeRegistrationPayloadBuilder:
    PANEL_API_SUFFIX = "/panel/api"

    class EApiKey(StrEnum):
        NAME = "name"
        REMARK = "remark"
        SCHEME = "scheme"
        ADDRESS = "address"
        PORT = "port"
        BASE_PATH = "basePath"
        API_TOKEN = "apiToken"
        ENABLE = "enable"
        ALLOW_PRIVATE_ADDRESS = "allowPrivateAddress"
        TLS_VERIFY_MODE = "tlsVerifyMode"
        INBOUND_SYNC_MODE = "inboundSyncMode"

    TLS_VERIFY_MODE_VERIFY = "verify"
    TLS_VERIFY_MODE_SKIP = "skip"

    INBOUND_SYNC_MODE_ALL = "all"

    def build(self, registration: TNodeRegistrationConfig) -> dict[str, object]:
        parsed_api_url = urlparse(registration.api_url)

        address = parsed_api_url.hostname or registration.address
        port = parsed_api_url.port or registration.port
        scheme = parsed_api_url.scheme

        base_path = self._extract_base_path(parsed_api_url.path)

        return {
            str(self.EApiKey.NAME): registration.name,
            str(self.EApiKey.REMARK): registration.remark,
            str(self.EApiKey.SCHEME): scheme,
            str(self.EApiKey.ADDRESS): address,
            str(self.EApiKey.PORT): port,
            str(self.EApiKey.BASE_PATH): base_path,
            str(self.EApiKey.API_TOKEN): registration.token,
            str(self.EApiKey.ENABLE): True,
            str(self.EApiKey.ALLOW_PRIVATE_ADDRESS): False,
            str(self.EApiKey.TLS_VERIFY_MODE): self._get_tls_verify_mode(
                registration.verify_ssl
            ),
            str(self.EApiKey.INBOUND_SYNC_MODE): self.INBOUND_SYNC_MODE_ALL,
        }

    def _extract_base_path(self, api_path: str) -> str:
        if api_path.endswith(self.PANEL_API_SUFFIX):
            base_path = api_path[: -len(self.PANEL_API_SUFFIX)]
        else:
            base_path = api_path

        if not base_path.startswith("/"):
            base_path = f"/{base_path}"

        if not base_path.endswith("/"):
            base_path = f"{base_path}/"

        return base_path

    def _get_tls_verify_mode(self, verify_ssl: bool) -> str:
        if verify_ssl:
            return self.TLS_VERIFY_MODE_VERIFY

        return self.TLS_VERIFY_MODE_SKIP
