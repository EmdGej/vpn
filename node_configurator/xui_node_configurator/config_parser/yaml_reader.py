from pathlib import Path

import yaml

from xui_node_configurator.exceptions import TConfigError


class TYamlReader:
    def read_mapping(self, path: str) -> dict[str, object]:
        config_path = Path(path)

        if not config_path.exists():
            raise TConfigError(f"Config file not found: {path}")

        with config_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise TConfigError("Config root has invalid structure")

        return data
