from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from xui_node_configurator.config.inbound_config import TInboundConfig
from xui_node_configurator.config.panel_config import TPanelConfig
from xui_node_configurator.config.parent_master_config import TParentMasterConfig


@dataclass(frozen=True)
class TNodeConfig:
    id: str
    role: "TNodeConfig.ERole"
    panel: TPanelConfig | None
    parent_master: TParentMasterConfig | None
    children: list[TNodeConfig]
    inbounds: list[TInboundConfig]

    class ERole(StrEnum):
        MASTER = "master"
        SLAVE = "slave"

    class EYamlKey(StrEnum):
        ID = "id"
        ROLE = "role"
        PANEL = "panel"
        PARENT_MASTER = "parent_master"
        CHILDREN = "children"
        INBOUNDS = "inbounds"
