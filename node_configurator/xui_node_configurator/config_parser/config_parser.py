from enum import StrEnum

from xui_node_configurator.config import (
    TInboundClientConfig,
    TInboundConfig,
    TInboundSettingsConfig,
    TNodeConfig,
    TNodeRegistrationConfig,
    TPanelConfig,
    TParentMasterConfig,
    TRealityNestedSettingsConfig,
    TRealitySettingsConfig,
    TSniffingConfig,
    TStreamSettingsConfig,
    TTcpHeaderConfig,
    TTcpSettingsConfig,
)
from xui_node_configurator.exceptions import TConfigError


class TConfigParser:
    def parse_node(self, data: dict[str, object], path: str = "node") -> TNodeConfig:
        node_id = self._required_str(data, TNodeConfig.EYamlKey.ID, path)
        role = TNodeConfig.ERole(
            self._required_str(data, TNodeConfig.EYamlKey.ROLE, path)
        )

        panel = self._parse_optional_panel(data, path)
        parent_master = self._parse_optional_parent_master(data, path)

        children_data = self._optional_mapping_list(
            data,
            TNodeConfig.EYamlKey.CHILDREN,
            path,
        )

        inbounds_data = self._optional_mapping_list(
            data,
            TNodeConfig.EYamlKey.INBOUNDS,
            path,
        )

        children: list[TNodeConfig] = []
        for index, child_data in enumerate(children_data):
            children.append(
                self.parse_node(
                    child_data,
                    f"{path}.{TNodeConfig.EYamlKey.CHILDREN}[{index}]",
                )
            )

        inbounds: list[TInboundConfig] = []
        for index, inbound_data in enumerate(inbounds_data):
            inbounds.append(
                self._parse_inbound(
                    inbound_data,
                    f"{path}.{TNodeConfig.EYamlKey.INBOUNDS}[{index}]",
                )
            )

        return TNodeConfig(
            id=node_id,
            role=role,
            panel=panel,
            parent_master=parent_master,
            children=children,
            inbounds=inbounds,
        )

    def _parse_optional_panel(
        self,
        data: dict[str, object],
        path: str,
    ) -> TPanelConfig | None:
        panel_data = self._optional_mapping(data, TNodeConfig.EYamlKey.PANEL, path)

        if panel_data is None:
            return None

        return self._parse_panel(
            panel_data,
            f"{path}.{TNodeConfig.EYamlKey.PANEL}",
        )

    def _parse_panel(
        self,
        data: dict[str, object],
        path: str,
    ) -> TPanelConfig:
        return TPanelConfig(
            api_url=self._required_str(data, TPanelConfig.EYamlKey.API_URL, path),
            token=self._required_str(data, TPanelConfig.EYamlKey.TOKEN, path),
            verify_ssl=self._optional_bool(
                data,
                TPanelConfig.EYamlKey.VERIFY_SSL,
                TPanelConfig.DEFAULT_VERIFY_SSL,
                path,
            ),
            timeout_seconds=self._optional_int(
                data,
                TPanelConfig.EYamlKey.TIMEOUT,
                TPanelConfig.DEFAULT_TIMEOUT_SECONDS,
                path,
            ),
        )

    def _parse_optional_parent_master(
        self,
        data: dict[str, object],
        path: str,
    ) -> TParentMasterConfig | None:
        parent_master_data = self._optional_mapping(
            data,
            TNodeConfig.EYamlKey.PARENT_MASTER,
            path,
        )

        if parent_master_data is None:
            return None

        parent_master_path = f"{path}.{TNodeConfig.EYamlKey.PARENT_MASTER}"

        panel_data = self._required_mapping(
            parent_master_data,
            TParentMasterConfig.EYamlKey.PANEL,
            parent_master_path,
        )

        node_registration_data = self._required_mapping(
            parent_master_data,
            TParentMasterConfig.EYamlKey.NODE_REGISTRATION,
            parent_master_path,
        )

        return TParentMasterConfig(
            id=self._required_str(
                parent_master_data,
                TParentMasterConfig.EYamlKey.ID,
                parent_master_path,
            ),
            panel=self._parse_panel(
                panel_data,
                f"{parent_master_path}.{TParentMasterConfig.EYamlKey.PANEL}",
            ),
            node_registration=self._parse_node_registration(
                node_registration_data,
                (
                    f"{parent_master_path}."
                    f"{TParentMasterConfig.EYamlKey.NODE_REGISTRATION}"
                ),
            ),
        )

    def _parse_node_registration(
        self,
        data: dict[str, object],
        path: str,
    ) -> TNodeRegistrationConfig:
        return TNodeRegistrationConfig(
            name=self._required_str(data, TNodeRegistrationConfig.EYamlKey.NAME, path),
            remark=self._required_str(data, TNodeRegistrationConfig.EYamlKey.REMARK, path),
            verify_ssl=self._optional_bool(
                data,
                TNodeRegistrationConfig.EYamlKey.VERIFY_SSL,
                TNodeRegistrationConfig.DEFAULT_VERIFY_SSL,
                path,
            ),
        )


    def _parse_inbound(
        self,
        data: dict[str, object],
        path: str,
    ) -> TInboundConfig:
        port = self._required_int(data, TInboundConfig.EYamlKey.PORT, path)

        return TInboundConfig(
            remark=self._optional_str(
                data,
                TInboundConfig.EYamlKey.REMARK,
                TInboundConfig.DEFAULT_REMARK_TEMPLATE.format(port=port),
                path,
            ),
            enable=self._optional_bool(
                data,
                TInboundConfig.EYamlKey.ENABLE,
                TInboundConfig.DEFAULT_ENABLE,
                path,
            ),
            expiry_time=self._optional_int(
                data,
                TInboundConfig.EYamlKey.EXPIRY_TIME,
                TInboundConfig.DEFAULT_EXPIRY_TIME,
                path,
            ),
            listen=self._optional_str(
                data,
                TInboundConfig.EYamlKey.LISTEN,
                TInboundConfig.DEFAULT_LISTEN,
                path,
            ),
            port=port,
            protocol=self._optional_str(
                data,
                TInboundConfig.EYamlKey.PROTOCOL,
                TInboundConfig.DEFAULT_PROTOCOL,
                path,
            ),
            tag=self._optional_str(
                data,
                TInboundConfig.EYamlKey.TAG,
                TInboundConfig.DEFAULT_TAG_TEMPLATE.format(port=port),
                path,
            ),
            settings=self._parse_inbound_settings(
                self._optional_mapping(data, TInboundConfig.EYamlKey.SETTINGS, path),
                f"{path}.{TInboundConfig.EYamlKey.SETTINGS}",
            ),
            sniffing=self._parse_optional_sniffing(
                self._optional_mapping(data, TInboundConfig.EYamlKey.SNIFFING, path),
                f"{path}.{TInboundConfig.EYamlKey.SNIFFING}",
            ),
            stream_settings=self._parse_stream_settings(
                self._optional_mapping(
                    data,
                    TInboundConfig.EYamlKey.STREAM_SETTINGS,
                    path,
                ),
                f"{path}.{TInboundConfig.EYamlKey.STREAM_SETTINGS}",
            ),
        )

    def _parse_inbound_settings(
        self,
        data: dict[str, object] | None,
        path: str,
    ) -> TInboundSettingsConfig:
        settings_data = data or {}

        clients_data = self._optional_mapping_list(
            settings_data,
            TInboundSettingsConfig.EYamlKey.CLIENTS,
            path,
        )

        clients: list[TInboundClientConfig] = []
        for index, client_data in enumerate(clients_data):
            client_path = f"{path}.{TInboundSettingsConfig.EYamlKey.CLIENTS}[{index}]"

            clients.append(
                TInboundClientConfig(
                    id=self._required_str(
                        client_data,
                        TInboundClientConfig.EYamlKey.ID,
                        client_path,
                    ),
                    email=self._required_str(
                        client_data,
                        TInboundClientConfig.EYamlKey.EMAIL,
                        client_path,
                    ),
                    enable=self._optional_bool(
                        client_data,
                        TInboundClientConfig.EYamlKey.ENABLE,
                        TInboundClientConfig.DEFAULT_ENABLE,
                        client_path,
                    ),
                )
            )

        return TInboundSettingsConfig(
            clients=clients,
            decryption=self._optional_str(
                settings_data,
                TInboundSettingsConfig.EYamlKey.DECRYPTION,
                TInboundSettingsConfig.DEFAULT_DECRYPTION,
                path,
            ),
            encryption=self._optional_str(
                settings_data,
                TInboundSettingsConfig.EYamlKey.ENCRYPTION,
                TInboundSettingsConfig.DEFAULT_ENCRYPTION,
                path,
            ),
            testseed=self._nullable_int_list(
                settings_data,
                TInboundSettingsConfig.EYamlKey.TEST_SEED,
                path,
            ),
        )

    def _parse_optional_sniffing(
        self,
        data: dict[str, object] | None,
        path: str,
    ) -> TSniffingConfig | None:
        if data is None:
            return None

        return TSniffingConfig(
            enabled=self._optional_bool(
                data,
                TSniffingConfig.EYamlKey.ENABLED,
                TSniffingConfig.DEFAULT_ENABLED,
                path,
            )
        )

    def _parse_stream_settings(
        self,
        data: dict[str, object] | None,
        path: str,
    ) -> TStreamSettingsConfig:
        stream_data = data or {}

        network = TStreamSettingsConfig.ENetwork(
            self._optional_str(
                stream_data,
                TStreamSettingsConfig.EYamlKey.NETWORK,
                str(TStreamSettingsConfig.DEFAULT_NETWORK),
                path,
            )
        )

        security = TStreamSettingsConfig.ESecurity(
            self._optional_str(
                stream_data,
                TStreamSettingsConfig.EYamlKey.SECURITY,
                str(TStreamSettingsConfig.DEFAULT_SECURITY),
                path,
            )
        )

        reality_data = self._optional_mapping(
            stream_data,
            TStreamSettingsConfig.EYamlKey.REALITY_SETTINGS,
            path,
        )

        if reality_data is None:
            raise TConfigError(
                f"{path}.{TStreamSettingsConfig.EYamlKey.REALITY_SETTINGS} is required"
            )

        return TStreamSettingsConfig(
            network=network,
            security=security,
            tcp_settings=self._parse_tcp_settings(
                self._optional_mapping(
                    stream_data,
                    TStreamSettingsConfig.EYamlKey.TCP_SETTINGS,
                    path,
                ),
                f"{path}.{TStreamSettingsConfig.EYamlKey.TCP_SETTINGS}",
            ),
            reality_settings=self._parse_reality_settings(
                reality_data,
                f"{path}.{TStreamSettingsConfig.EYamlKey.REALITY_SETTINGS}",
            ),
        )

    def _parse_tcp_settings(
        self,
        data: dict[str, object] | None,
        path: str,
    ) -> TTcpSettingsConfig:
        tcp_data = data or {}

        return TTcpSettingsConfig(
            accept_proxy_protocol=self._optional_bool(
                tcp_data,
                TTcpSettingsConfig.EYamlKey.ACCEPT_PROXY_PROTOCOL,
                TTcpSettingsConfig.DEFAULT_ACCEPT_PROXY_PROTOCOL,
                path,
            ),
            header=self._parse_tcp_header(
                self._optional_mapping(
                    tcp_data,
                    TTcpSettingsConfig.EYamlKey.HEADER,
                    path,
                ),
                f"{path}.{TTcpSettingsConfig.EYamlKey.HEADER}",
            ),
        )

    def _parse_tcp_header(
        self,
        data: dict[str, object] | None,
        path: str,
    ) -> TTcpHeaderConfig:
        header_data = data or {}

        return TTcpHeaderConfig(
            type=TTcpHeaderConfig.EType(
                self._optional_str(
                    header_data,
                    TTcpHeaderConfig.EYamlKey.TYPE,
                    str(TTcpHeaderConfig.DEFAULT_TYPE),
                    path,
                )
            )
        )

    def _parse_reality_settings(
        self,
        data: dict[str, object],
        path: str,
    ) -> TRealitySettingsConfig:
        return TRealitySettingsConfig(
            show=self._optional_bool(
                data,
                TRealitySettingsConfig.EYamlKey.SHOW,
                TRealitySettingsConfig.DEFAULT_SHOW,
                path,
            ),
            xver=self._optional_int(
                data,
                TRealitySettingsConfig.EYamlKey.XVER,
                TRealitySettingsConfig.DEFAULT_XVER,
                path,
            ),
            target=self._nullable_str(
                data,
                TRealitySettingsConfig.EYamlKey.TARGET,
                path,
            ),
            dest=self._nullable_str(
                data,
                TRealitySettingsConfig.EYamlKey.DEST,
                path,
            ),
            server_names=self._optional_str_list(
                data,
                TRealitySettingsConfig.EYamlKey.SERVER_NAMES,
                [],
                path,
            ),
            private_key=self._nullable_str(
                data,
                TRealitySettingsConfig.EYamlKey.PRIVATE_KEY,
                path,
            ),
            public_key=self._nullable_str(
                data,
                TRealitySettingsConfig.EYamlKey.PUBLIC_KEY,
                path,
            ),
            min_client_ver=self._optional_str(
                data,
                TRealitySettingsConfig.EYamlKey.MIN_CLIENT_VER,
                TRealitySettingsConfig.DEFAULT_MIN_CLIENT_VER,
                path,
            ),
            max_client_ver=self._optional_str(
                data,
                TRealitySettingsConfig.EYamlKey.MAX_CLIENT_VER,
                TRealitySettingsConfig.DEFAULT_MAX_CLIENT_VER,
                path,
            ),
            max_timediff=self._optional_int(
                data,
                TRealitySettingsConfig.EYamlKey.MAX_TIMEDIFF,
                TRealitySettingsConfig.DEFAULT_MAX_TIMEDIFF,
                path,
            ),
            short_ids=self._nullable_str_list(
                data,
                TRealitySettingsConfig.EYamlKey.SHORT_IDS,
                path,
            ),
            short_ids_count=self._optional_int(
                data,
                TRealitySettingsConfig.EYamlKey.SHORT_IDS_COUNT,
                TRealitySettingsConfig.DEFAULT_SHORT_IDS_COUNT,
                path,
            ),
            mldsa65_seed=self._optional_str(
                data,
                TRealitySettingsConfig.EYamlKey.MLDSA65_SEED,
                TRealitySettingsConfig.DEFAULT_MLDSA65_SEED,
                path,
            ),
            spider_x=self._nullable_str(
                data,
                TRealitySettingsConfig.EYamlKey.SPIDER_X,
                path,
            ),
            spider_x_length=self._optional_int(
                data,
                TRealitySettingsConfig.EYamlKey.SPIDER_X_LENGTH,
                TRealitySettingsConfig.DEFAULT_SPIDER_X_LENGTH,
                path,
            ),
            settings=self._parse_reality_nested_settings(
                self._optional_mapping(
                    data,
                    TRealitySettingsConfig.EYamlKey.SETTINGS,
                    path,
                ),
                f"{path}.{TRealitySettingsConfig.EYamlKey.SETTINGS}",
            ),
        )

    def _parse_reality_nested_settings(
        self,
        data: dict[str, object] | None,
        path: str,
    ) -> TRealityNestedSettingsConfig:
        settings_data = data or {}

        return TRealityNestedSettingsConfig(
            public_key=self._nullable_str(
                settings_data,
                TRealityNestedSettingsConfig.EYamlKey.PUBLIC_KEY,
                path,
            ),
            fingerprint=self._optional_str(
                settings_data,
                TRealityNestedSettingsConfig.EYamlKey.FINGERPRINT,
                TRealityNestedSettingsConfig.DEFAULT_FINGERPRINT,
                path,
            ),
            server_name=self._optional_str(
                settings_data,
                TRealityNestedSettingsConfig.EYamlKey.SERVER_NAME,
                TRealityNestedSettingsConfig.DEFAULT_SERVER_NAME,
                path,
            ),
            spider_x=self._nullable_str(
                settings_data,
                TRealityNestedSettingsConfig.EYamlKey.SPIDER_X,
                path,
            ),
            mldsa65_verify=self._optional_str(
                settings_data,
                TRealityNestedSettingsConfig.EYamlKey.MLDSA65_VERIFY,
                TRealityNestedSettingsConfig.DEFAULT_MLDSA65_VERIFY,
                path,
            ),
        )

    def _required_mapping(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> dict[str, object]:
        key_value = str(key)

        if key_value not in data:
            raise TConfigError(f"{path}.{key_value} is required")

        value = data[key_value]

        if not isinstance(value, dict):
            raise TConfigError(f"{path}.{key_value} has invalid structure")

        return value

    def _optional_mapping(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> dict[str, object] | None:
        key_value = str(key)
        value = data.get(key_value)

        if value is None:
            return None

        if not isinstance(value, dict):
            raise TConfigError(f"{path}.{key_value} has invalid structure")

        return value

    def _optional_mapping_list(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> list[dict[str, object]]:
        key_value = str(key)
        value = data.get(key_value, [])

        if not isinstance(value, list):
            raise TConfigError(f"{path}.{key_value} has invalid structure")

        result: list[dict[str, object]] = []

        for index, item in enumerate(value):
            item_path = f"{path}.{key_value}[{index}]"

            if not isinstance(item, dict):
                raise TConfigError(f"{item_path} has invalid structure")

            result.append(item)

        return result

    def _required_str(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> str:
        key_value = str(key)

        if key_value not in data:
            raise TConfigError(f"{path}.{key_value} is required")

        value = data[key_value]

        if not isinstance(value, str):
            raise TConfigError(f"{path}.{key_value} must be string")

        if value == "":
            raise TConfigError(f"{path}.{key_value} must not be empty")

        return value

    def _optional_str(
        self,
        data: dict[str, object],
        key: StrEnum,
        default: str,
        path: str,
    ) -> str:
        key_value = str(key)
        value = data.get(key_value, default)

        if not isinstance(value, str):
            raise TConfigError(f"{path}.{key_value} must be string")

        return value

    def _nullable_str(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> str | None:
        key_value = str(key)
        value = data.get(key_value)

        if value is None:
            return None

        if not isinstance(value, str):
            raise TConfigError(f"{path}.{key_value} must be string")

        return value

    def _required_int(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> int:
        key_value = str(key)

        if key_value not in data:
            raise TConfigError(f"{path}.{key_value} is required")

        value = data[key_value]

        if not isinstance(value, int):
            raise TConfigError(f"{path}.{key_value} must be integer")

        return value

    def _optional_int(
        self,
        data: dict[str, object],
        key: StrEnum,
        default: int,
        path: str,
    ) -> int:
        key_value = str(key)
        value = data.get(key_value, default)

        if not isinstance(value, int):
            raise TConfigError(f"{path}.{key_value} must be integer")

        return value

    def _optional_bool(
        self,
        data: dict[str, object],
        key: StrEnum,
        default: bool,
        path: str,
    ) -> bool:
        key_value = str(key)
        value = data.get(key_value, default)

        if not isinstance(value, bool):
            raise TConfigError(f"{path}.{key_value} must be boolean")

        return value

    def _optional_str_list(
        self,
        data: dict[str, object],
        key: StrEnum,
        default: list[str],
        path: str,
    ) -> list[str]:
        key_value = str(key)
        value = data.get(key_value, default)

        if not isinstance(value, list):
            raise TConfigError(f"{path}.{key_value} has invalid structure")

        result: list[str] = []

        for index, item in enumerate(value):
            if not isinstance(item, str):
                raise TConfigError(f"{path}.{key_value}[{index}] must be string")

            result.append(item)

        return result

    def _nullable_str_list(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> list[str] | None:
        key_value = str(key)
        value = data.get(key_value)

        if value is None:
            return None

        if not isinstance(value, list):
            raise TConfigError(f"{path}.{key_value} has invalid structure")

        result: list[str] = []

        for index, item in enumerate(value):
            if not isinstance(item, str):
                raise TConfigError(f"{path}.{key_value}[{index}] must be string")

            result.append(item)

        return result

    def _nullable_int_list(
        self,
        data: dict[str, object],
        key: StrEnum,
        path: str,
    ) -> list[int] | None:
        key_value = str(key)
        value = data.get(key_value)

        if value is None:
            return None

        if not isinstance(value, list):
            raise TConfigError(f"{path}.{key_value} has invalid structure")

        result: list[int] = []

        for index, item in enumerate(value):
            if not isinstance(item, int):
                raise TConfigError(f"{path}.{key_value}[{index}] must be integer")

            result.append(item)

        return result
