import argparse
import sys
from pathlib import Path

from xui_node_configurator.api import TPanelUrlBuilder
from xui_node_configurator.config_parser import (
    TConfigLoader,
    TConfigParser,
    TYamlReader,
)
from xui_node_configurator.exceptions import TBaseError
from xui_node_configurator.payload_builder import (
    TInboundPayloadBuilder,
    TNodeRegistrationPayloadBuilder,
)
from xui_node_configurator.service import TNodeConfiguratorService


PACKAGE_ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="xui-node-configurator",
        description="Configure 3x-ui node from YAML",
    )

    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help=f"Path to YAML config file",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print payloads without API requests",
    )

    return parser.parse_args()


def create_config_loader() -> TConfigLoader:
    return TConfigLoader(
        yaml_reader=TYamlReader(),
        config_parser=TConfigParser(),
    )


def create_service(dry_run: bool) -> TNodeConfiguratorService:
    url_builder = TPanelUrlBuilder()

    return TNodeConfiguratorService(
        inbound_payload_builder=TInboundPayloadBuilder(),
        node_registration_payload_builder=TNodeRegistrationPayloadBuilder(),
        url_builder=url_builder,
        dry_run=dry_run,
    )


def main() -> int:
    args = parse_args()

    try:
        loader = create_config_loader()
        node = loader.load(args.config)

        service = create_service(dry_run=args.dry_run)
        service.configure(node)

        return 0

    except TBaseError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
