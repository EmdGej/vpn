from typing import cast

from xui_node_configurator.api import TPanelUrlBuilder, TXuiApiClient
from xui_node_configurator.config import TInboundConfig, TNodeConfig
from xui_node_configurator.exceptions import TConfigError
from xui_node_configurator.payload_builder import (
    TInboundPayloadBuilder,
    TNodeRegistrationPayloadBuilder,
)
from xui_node_configurator.reality import TRealityConfigEnricher


class TNodeConfiguratorService:
    API_OBJECT_KEY = "obj"

    NODE_NAME_KEY = "name"
    NODE_ADDRESS_KEY = "address"
    NODE_PORT_KEY = "port"
    NODE_BASE_PATH_KEY = "basePath"

    INBOUND_PORT_KEY = "port"
    INBOUND_REMARK_KEY = "remark"

    def __init__(
        self,
        inbound_payload_builder: TInboundPayloadBuilder,
        node_registration_payload_builder: TNodeRegistrationPayloadBuilder,
        url_builder: TPanelUrlBuilder,
        dry_run: bool,
    ):
        self._inbound_payload_builder = inbound_payload_builder
        self._node_registration_payload_builder = node_registration_payload_builder
        self._url_builder = url_builder
        self._dry_run = dry_run

    def configure(self, node: TNodeConfig) -> None:
        self._register_node_in_parent_master(node)
        self._create_inbounds(node)

    def _register_node_in_parent_master(self, node: TNodeConfig) -> None:
        if node.parent_master is None:
            print("No parent master configured")
            return

        if node.panel is None:
            raise TConfigError("node.panel is required to register node in parent master")

        master_client = TXuiApiClient(node.parent_master.panel, self._url_builder)

        payload = self._node_registration_payload_builder.build(
            registration=node.parent_master.node_registration,
            node_panel=node.panel,
        )

        if self._dry_run:
            print("DRY-RUN node registration payload:")
            print(payload)
            return

        existing_nodes = self._get_nodes(master_client)

        if self._node_exists(existing_nodes, payload):
            print(
                f"Node already exists in master, skip registration: "
                f"{payload.get(self.NODE_NAME_KEY)}"
            )
            return

        response = master_client.add_node(payload)
        print(f"Node registered in master: {response}")

    def _create_inbounds(self, node: TNodeConfig) -> None:
        if not node.inbounds:
            print("No inbounds to create")
            return

        if node.panel is None:
            raise TConfigError("node.panel is required to create inbounds")

        slave_client = TXuiApiClient(node.panel, self._url_builder)
        reality_enricher = TRealityConfigEnricher(slave_client)

        existing_inbounds = self._get_inbounds(slave_client)

        for inbound in node.inbounds:
            if self._inbound_exists(existing_inbounds, inbound):
                print(
                    f"Inbound already exists, skip creation: "
                    f"port={inbound.port}, remark={inbound.remark}"
                )
                continue

            enriched_inbound = reality_enricher.enrich_inbound(inbound)
            payload = self._inbound_payload_builder.build(enriched_inbound)

            if self._dry_run:
                print("DRY-RUN inbound payload:")
                print(payload)
                continue

            response = slave_client.add_inbound(payload)
            print(f"Inbound created: {response}")

    def _get_nodes(self, client: TXuiApiClient) -> list[dict[str, object]]:
        response = client.list_nodes()
        obj = response.get(self.API_OBJECT_KEY)

        if not isinstance(obj, list):
            raise TConfigError("nodes list response has invalid structure")

        result: list[dict[str, object]] = []

        for item in obj:
            if isinstance(item, dict):
                result.append(cast(dict[str, object], item))

        return result

    def _get_inbounds(self, client: TXuiApiClient) -> list[dict[str, object]]:
        response = client.list_inbounds()
        obj = response.get(self.API_OBJECT_KEY)

        if not isinstance(obj, list):
            raise TConfigError("inbounds list response has invalid structure")

        result: list[dict[str, object]] = []

        for item in obj:
            if isinstance(item, dict):
                result.append(cast(dict[str, object], item))

        return result

    def _node_exists(
        self,
        existing_nodes: list[dict[str, object]],
        payload: dict[str, object],
    ) -> bool:
        expected_name = payload.get(self.NODE_NAME_KEY)
        expected_address = payload.get(self.NODE_ADDRESS_KEY)
        expected_port = payload.get(self.NODE_PORT_KEY)
        expected_base_path = payload.get(self.NODE_BASE_PATH_KEY)

        for node in existing_nodes:
            if (
                node.get(self.NODE_NAME_KEY) == expected_name
                and node.get(self.NODE_ADDRESS_KEY) == expected_address
                and node.get(self.NODE_PORT_KEY) == expected_port
                and node.get(self.NODE_BASE_PATH_KEY) == expected_base_path
            ):
                return True

        return False

    def _inbound_exists(
        self,
        existing_inbounds: list[dict[str, object]],
        inbound: TInboundConfig,
    ) -> bool:
        for existing_inbound in existing_inbounds:
            if existing_inbound.get(self.INBOUND_PORT_KEY) == inbound.port:
                return True

            if existing_inbound.get(self.INBOUND_REMARK_KEY) == inbound.remark:
                return True

        return False
