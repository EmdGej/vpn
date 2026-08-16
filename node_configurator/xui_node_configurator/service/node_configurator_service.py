from xui_node_configurator.api import TPanelUrlBuilder, TXuiApiClient
from xui_node_configurator.config import TNodeConfig
from xui_node_configurator.exceptions import TConfigError
from xui_node_configurator.payload_builder import (
    TInboundPayloadBuilder,
    TNodeRegistrationPayloadBuilder,
)


class TNodeConfiguratorService:
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
        self._create_inbounds(node)
        self._register_node_in_parent_master(node)

    def _create_inbounds(self, node: TNodeConfig) -> None:
        if not node.inbounds:
            print("No inbounds to create")
            return

        if node.panel is None:
            raise TConfigError("node.panel is required to create inbounds")

        client = TXuiApiClient(node.panel, self._url_builder)

        for inbound in node.inbounds:
            payload = self._inbound_payload_builder.build(inbound)

            if self._dry_run:
                print("DRY-RUN inbound payload:")
                print(payload)
                continue

            response = client.add_inbound(payload)
            print(f"Inbound created: {response}")

    def _register_node_in_parent_master(self, node: TNodeConfig) -> None:
        if node.parent_master is None:
            print("No parent master configured")
            return

        client = TXuiApiClient(node.parent_master.panel, self._url_builder)

        payload = self._node_registration_payload_builder.build(
            node.parent_master.node_registration
        )

        if self._dry_run:
            print("DRY-RUN node registration payload:")
            print(payload)
            return

        response = client.add_node(payload)
        print(f"Node registered in master: {response}")
