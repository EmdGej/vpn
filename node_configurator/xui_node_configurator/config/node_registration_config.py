from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class TNodeRegistrationConfig:
    name: str
    remark: str
    verify_ssl: bool

    class EYamlKey(StrEnum):
        NAME = "name"
        REMARK = "remark"
        VERIFY_SSL = "verify_ssl"

    DEFAULT_VERIFY_SSL = False
