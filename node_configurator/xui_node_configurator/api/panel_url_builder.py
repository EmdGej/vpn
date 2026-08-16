from xui_node_configurator.config import TPanelConfig
from xui_node_configurator.exceptions import TConfigError


class TPanelUrlBuilder:
    PANEL_API_SUFFIX = "/panel/api"

    def build_api_url(self, panel: TPanelConfig, endpoint: str) -> str:
        return f"{panel.api_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def build_panel_url(self, panel: TPanelConfig, endpoint: str) -> str:
        panel_base_url = self.get_panel_base_url(panel)
        return f"{panel_base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def get_panel_base_url(self, panel: TPanelConfig) -> str:
        api_url = panel.api_url.rstrip("/")

        if not api_url.endswith(self.PANEL_API_SUFFIX):
            raise TConfigError(
                f"panel.api_url must end with {self.PANEL_API_SUFFIX}"
            )

        return api_url[: -len(self.PANEL_API_SUFFIX)]
