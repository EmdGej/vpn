from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class TNodeRegistrationConfig:
    name: str
    address: str
    port: int
    api_url: str
    token: str
    remark: str
    verify_ssl: bool

    class EYamlKey(StrEnum):
        NAME = "name"
        ADDRESS = "address"
        PORT = "port"
        API_URL = "api_url"
        TOKEN = "token"
        REMARK = "remark"
        VERIFY_SSL = "verify_ssl"

    DEFAULT_VERIFY_SSL = False
