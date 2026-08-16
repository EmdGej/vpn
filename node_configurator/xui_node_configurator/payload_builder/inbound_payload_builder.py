import json
from enum import StrEnum

from xui_node_configurator.config import (
    TInboundClientConfig,
    TInboundConfig,
    TInboundSettingsConfig,
    TRealityNestedSettingsConfig,
    TRealitySettingsConfig,
    TSniffingConfig,
    TStreamSettingsConfig,
    TTcpHeaderConfig,
    TTcpSettingsConfig,
)


class TInboundPayloadBuilder:
    JSON_ENSURE_ASCII = False
    JSON_SEPARATORS = (",", ":")

    def build(self, inbound: TInboundConfig) -> dict[str, object]:
        payload: dict[str, object] = {
            self._key(TInboundConfig.EYamlKey.REMARK): inbound.remark,
            self._key(TInboundConfig.EYamlKey.ENABLE): inbound.enable,
            self._key(TInboundConfig.EYamlKey.EXPIRY_TIME): inbound.expiry_time,
            self._key(TInboundConfig.EYamlKey.LISTEN): inbound.listen,
            self._key(TInboundConfig.EYamlKey.PORT): inbound.port,
            self._key(TInboundConfig.EYamlKey.PROTOCOL): inbound.protocol,
            self._key(TInboundConfig.EYamlKey.TAG): inbound.tag,
            self._key(TInboundConfig.EYamlKey.SETTINGS): self._json_string(
                self._build_settings(inbound.settings)
            ),
            self._key(TInboundConfig.EYamlKey.STREAM_SETTINGS): self._json_string(
                self._build_stream_settings(inbound.stream_settings)
            ),
        }

        if inbound.sniffing is not None:
            payload[self._key(TInboundConfig.EYamlKey.SNIFFING)] = self._json_string(
                self._build_sniffing(inbound.sniffing)
            )

        return payload

    def _build_settings(self, settings: TInboundSettingsConfig) -> dict[str, object]:
        data: dict[str, object] = {
            self._key(TInboundSettingsConfig.EYamlKey.CLIENTS): [
                self._build_client(client)
                for client in settings.clients
            ],
            self._key(TInboundSettingsConfig.EYamlKey.DECRYPTION): settings.decryption,
            self._key(TInboundSettingsConfig.EYamlKey.ENCRYPTION): settings.encryption,
        }

        if settings.testseed is not None:
            data[self._key(TInboundSettingsConfig.EYamlKey.TEST_SEED)] = (
                settings.testseed
            )

        return data

    def _build_client(self, client: TInboundClientConfig) -> dict[str, object]:
        return {
            self._key(TInboundClientConfig.EYamlKey.ID): client.id,
            self._key(TInboundClientConfig.EYamlKey.EMAIL): client.email,
            self._key(TInboundClientConfig.EYamlKey.ENABLE): client.enable,
        }

    def _build_sniffing(self, sniffing: TSniffingConfig) -> dict[str, object]:
        return {
            self._key(TSniffingConfig.EYamlKey.ENABLED): sniffing.enabled,
        }

    def _build_stream_settings(
        self,
        stream_settings: TStreamSettingsConfig,
    ) -> dict[str, object]:
        return {
            self._key(TStreamSettingsConfig.EYamlKey.NETWORK): str(
                stream_settings.network
            ),
            self._key(TStreamSettingsConfig.EYamlKey.SECURITY): str(
                stream_settings.security
            ),
            self._key(TStreamSettingsConfig.EYamlKey.TCP_SETTINGS): (
                self._build_tcp_settings(stream_settings.tcp_settings)
            ),
            self._key(TStreamSettingsConfig.EYamlKey.REALITY_SETTINGS): (
                self._build_reality_settings(stream_settings.reality_settings)
            ),
        }

    def _build_tcp_settings(
        self,
        tcp_settings: TTcpSettingsConfig,
    ) -> dict[str, object]:
        return {
            self._key(TTcpSettingsConfig.EYamlKey.ACCEPT_PROXY_PROTOCOL): (
                tcp_settings.accept_proxy_protocol
            ),
            self._key(TTcpSettingsConfig.EYamlKey.HEADER): self._build_tcp_header(
                tcp_settings.header
            ),
        }

    def _build_tcp_header(self, header: TTcpHeaderConfig) -> dict[str, object]:
        return {
            self._key(TTcpHeaderConfig.EYamlKey.TYPE): str(header.type),
        }

    def _build_reality_settings(
        self,
        reality: TRealitySettingsConfig,
    ) -> dict[str, object]:
        data: dict[str, object] = {
            self._key(TRealitySettingsConfig.EYamlKey.SHOW): reality.show,
            self._key(TRealitySettingsConfig.EYamlKey.XVER): reality.xver,
            self._key(TRealitySettingsConfig.EYamlKey.SERVER_NAMES): (
                reality.server_names
            ),
            self._key(TRealitySettingsConfig.EYamlKey.MIN_CLIENT_VER): (
                reality.min_client_ver
            ),
            self._key(TRealitySettingsConfig.EYamlKey.MAX_CLIENT_VER): (
                reality.max_client_ver
            ),
            self._key(TRealitySettingsConfig.EYamlKey.MAX_TIMEDIFF): (
                reality.max_timediff
            ),
            self._key(TRealitySettingsConfig.EYamlKey.MLDSA65_SEED): (
                reality.mldsa65_seed
            ),
            self._key(TRealitySettingsConfig.EYamlKey.SETTINGS): (
                self._build_reality_nested_settings(reality.settings)
            ),
        }

        if reality.target is not None:
            data[self._key(TRealitySettingsConfig.EYamlKey.TARGET)] = reality.target

        if reality.dest is not None:
            data[self._key(TRealitySettingsConfig.EYamlKey.DEST)] = reality.dest

        if reality.private_key is not None:
            data[self._key(TRealitySettingsConfig.EYamlKey.PRIVATE_KEY)] = (
                reality.private_key
            )

        if reality.public_key is not None:
            data[self._key(TRealitySettingsConfig.EYamlKey.PUBLIC_KEY)] = (
                reality.public_key
            )

        if reality.short_ids is not None:
            data[self._key(TRealitySettingsConfig.EYamlKey.SHORT_IDS)] = (
                reality.short_ids
            )

        if reality.spider_x is not None:
            data[self._key(TRealitySettingsConfig.EYamlKey.SPIDER_X)] = (
                reality.spider_x
            )

        return data

    def _build_reality_nested_settings(
        self,
        settings: TRealityNestedSettingsConfig,
    ) -> dict[str, object]:
        data: dict[str, object] = {
            self._key(TRealityNestedSettingsConfig.EYamlKey.FINGERPRINT): (
                settings.fingerprint
            ),
            self._key(TRealityNestedSettingsConfig.EYamlKey.SERVER_NAME): (
                settings.server_name
            ),
            self._key(TRealityNestedSettingsConfig.EYamlKey.MLDSA65_VERIFY): (
                settings.mldsa65_verify
            ),
        }

        if settings.public_key is not None:
            data[self._key(TRealityNestedSettingsConfig.EYamlKey.PUBLIC_KEY)] = (
                settings.public_key
            )

        if settings.spider_x is not None:
            data[self._key(TRealityNestedSettingsConfig.EYamlKey.SPIDER_X)] = (
                settings.spider_x
            )

        return data

    def _json_string(self, data: dict[str, object]) -> str:
        return json.dumps(
            data,
            ensure_ascii=self.JSON_ENSURE_ASCII,
            separators=self.JSON_SEPARATORS,
        )

    @staticmethod
    def _key(key: StrEnum) -> str:
        return str(key)
