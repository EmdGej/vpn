import secrets
import string
from dataclasses import replace
from typing import cast

from xui_node_configurator.api import TXuiApiClient
from xui_node_configurator.config import (
    TInboundConfig,
    TRealityNestedSettingsConfig,
    TRealitySettingsConfig,
)


class TRealityConfigEnricher:
    SHORT_ID_BYTE_LENGTH = 8
    SPIDER_X_PREFIX = "/"
    SPIDER_X_ALPHABET = string.ascii_letters + string.digits

    def __init__(self, xui_client: TXuiApiClient):
        self._xui_client = xui_client

    def enrich_inbound(self, inbound: TInboundConfig) -> TInboundConfig:
        reality = inbound.stream_settings.reality_settings

        private_key = reality.private_key
        public_key = reality.settings.public_key

        if private_key is None or public_key is None:
            cert = self._get_new_x25519_cert()

            private_key = private_key or self._get_private_key(cert)
            public_key = public_key or self._get_public_key(cert)

        short_ids = reality.short_ids
        if short_ids is None:
            short_ids = self._generate_short_ids(reality.short_ids_count)

        spider_x = reality.settings.spider_x
        if spider_x is None:
            spider_x = self._generate_spider_x(reality.spider_x_length)

        enriched_nested_settings = replace(
            reality.settings,
            public_key=public_key,
            spider_x=spider_x,
        )

        enriched_reality = replace(
            reality,
            private_key=private_key,
            short_ids=short_ids,
            settings=enriched_nested_settings,
        )

        enriched_stream_settings = replace(
            inbound.stream_settings,
            reality_settings=enriched_reality,
        )

        return replace(
            inbound,
            stream_settings=enriched_stream_settings,
        )

    def _get_new_x25519_cert(self) -> dict[str, object]:
        response = self._xui_client.get_new_x25519_cert()

        obj = response.get(self._xui_client.RESPONSE_OBJECT_KEY)

        if not isinstance(obj, dict):
            raise RuntimeError("getNewX25519Cert response obj has invalid structure")

        return cast(dict[str, object], obj)

    def _get_private_key(self, cert: dict[str, object]) -> str:
        value = cert.get(str(TRealitySettingsConfig.EYamlKey.PRIVATE_KEY))

        if not isinstance(value, str):
            raise RuntimeError("getNewX25519Cert response privateKey is missing")

        return value

    def _get_public_key(self, cert: dict[str, object]) -> str:
        value = cert.get(str(TRealityNestedSettingsConfig.EYamlKey.PUBLIC_KEY))

        if not isinstance(value, str):
            raise RuntimeError("getNewX25519Cert response publicKey is missing")

        return value

    def _generate_short_ids(self, count: int) -> list[str]:
        return [
            secrets.token_hex(self.SHORT_ID_BYTE_LENGTH)
            for _ in range(count)
        ]

    def _generate_spider_x(self, length: int) -> str:
        value = "".join(
            secrets.choice(self.SPIDER_X_ALPHABET)
            for _ in range(length)
        )

        return f"{self.SPIDER_X_PREFIX}{value}"
