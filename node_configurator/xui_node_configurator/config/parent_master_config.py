from dataclasses import dataclass
from enum import StrEnum

from xui_node_configurator.config.node_registration_config import (
    TNodeRegistrationConfig,
)
from xui_node_configurator.config.panel_config import TPanelConfig


@dataclass(frozen=True)
class TParentMasterConfig:
    id: str
    panel: TPanelConfig
    node_registration: TNodeRegistrationConfig

    class EYamlKey(StrEnum):
        ID = "id"
        PANEL = "panel"
        NODE_REGISTRATION = "node_registration"
