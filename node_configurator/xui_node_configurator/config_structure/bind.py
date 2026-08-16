from dataclasses import dataclass

from xui_node_configurator.utils.http.constants import EHttpMethod


@dataclass(frozen=True)
class TNodeBindPayload:
    name: str
    address: str
    port: int
    api_url: str
    api_token: str
    remark: str
    verify_ssl: bool


@dataclass(frozen=True)
class TBindConfig:
    method: EHttpMethod
    api_endpoint: str
    node: TNodeBindPayload
