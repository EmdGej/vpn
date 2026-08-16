from xui_node_configurator.config import TNodeConfig
from xui_node_configurator.config_parser.config_parser import TConfigParser
from xui_node_configurator.config_parser.yaml_reader import TYamlReader


class TConfigLoader:
    def __init__(
        self,
        yaml_reader: TYamlReader,
        config_parser: TConfigParser,
    ):
        self._yaml_reader = yaml_reader
        self._config_parser = config_parser

    def load(self, path: str) -> TNodeConfig:
        data = self._yaml_reader.read_mapping(path)
        return self._config_parser.parse_node(data)
