from typing import cast

import requests

from xui_node_configurator.exceptions import TApiError
from xui_node_configurator.utils.http.constants import EHttpMethod
from xui_node_configurator.api.panel_url_builder import TPanelUrlBuilder
from xui_node_configurator.api.xui_endpoints import EInboundEndpoint, ENodeEndpoint, EServerEndpoint
from xui_node_configurator.config import TPanelConfig


class TXuiApiClient:
    HEADER_CONTENT_TYPE = "Content-Type"
    HEADER_AUTHORIZATION = "Authorization"

    CONTENT_TYPE_JSON = "application/json"
    AUTHORIZATION_BEARER_PREFIX = "Bearer"

    RESPONSE_SUCCESS_KEY = "success"
    RESPONSE_MESSAGE_KEY = "msg"
    RESPONSE_OBJECT_KEY = "obj"

    def __init__(self, panel: TPanelConfig, url_builder: TPanelUrlBuilder):
        self._panel = panel
        self._url_builder = url_builder

        self._session = requests.Session()
        self._session.verify = panel.verify_ssl
        self._session.headers.update(
            {
                self.HEADER_CONTENT_TYPE: self.CONTENT_TYPE_JSON,
                self.HEADER_AUTHORIZATION: (
                    f"{self.AUTHORIZATION_BEARER_PREFIX} {panel.token}"
                ),
            }
        )

    def add_inbound(self, payload: dict[str, object]) -> dict[str, object]:
        url = self._url_builder.build_api_url(
            self._panel,
            str(EInboundEndpoint.ADD),
        )

        return self._request_json(EHttpMethod.POST, url, payload)

    def add_node(self, payload: dict[str, object]) -> dict[str, object]:
        url = self._url_builder.build_api_url(
            self._panel,
            str(ENodeEndpoint.ADD),
        )

        return self._request_json(EHttpMethod.POST, url, payload)

    def get_new_x25519_cert(self) -> dict[str, object]:
        url = self._url_builder.build_api_url(
            self._panel,
            str(EServerEndpoint.GET_NEW_X25519_CERT),
        )

        return self._request_json(EHttpMethod.GET, url, None)

    def _request_json(
        self,
        method: EHttpMethod,
        url: str,
        payload: dict[str, object] | None,
    ) -> dict[str, object]:
        try:
            response = self._session.request(
                method=str(method),
                url=url,
                json=payload,
                timeout=self._panel.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise TApiError(f"Request failed: {exc}") from exc

        if not response.ok:
            raise TApiError(f"HTTP {response.status_code}: {response.text}")

        try:
            response_data = response.json()
        except ValueError as exc:
            raise TApiError(f"Invalid JSON response: {response.text}") from exc

        if not isinstance(response_data, dict):
            raise TApiError("API response has invalid structure")

        response_dict = cast(dict[str, object], response_data)

        success = response_dict.get(self.RESPONSE_SUCCESS_KEY)

        if success is False:
            raise TApiError(
                f"API error: {response_dict.get(self.RESPONSE_MESSAGE_KEY)}"
            )

        return response_dict

