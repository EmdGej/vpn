from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class TPanelConfig:
    api_url: str
    token: str
    verify_ssl: bool
    timeout_seconds: int

    class EYamlKey(StrEnum):
        API_URL = "api_url"
        TOKEN = "token"
        VERIFY_SSL = "verify_ssl"
        TIMEOUT = "timeout"

    DEFAULT_VERIFY_SSL = True
    DEFAULT_TIMEOUT_SECONDS = 30
