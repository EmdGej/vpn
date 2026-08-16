from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class TInboundClientConfig:
    id: str
    email: str
    enable: bool

    class EYamlKey(StrEnum):
        ID = "id"
        EMAIL = "email"
        ENABLE = "enable"

    DEFAULT_ENABLE = True


@dataclass(frozen=True)
class TInboundSettingsConfig:
    clients: list[TInboundClientConfig]
    decryption: str
    encryption: str
    testseed: list[int] | None

    class EYamlKey(StrEnum):
        CLIENTS = "clients"
        DECRYPTION = "decryption"
        ENCRYPTION = "encryption"
        TEST_SEED = "testseed"

    DEFAULT_DECRYPTION = "none"
    DEFAULT_ENCRYPTION = "none"


@dataclass(frozen=True)
class TSniffingConfig:
    enabled: bool

    class EYamlKey(StrEnum):
        ENABLED = "enabled"

    DEFAULT_ENABLED = False


@dataclass(frozen=True)
class TTcpHeaderConfig:
    type: "TTcpHeaderConfig.EType"

    class EType(StrEnum):
        NONE = "none"
        HTTP = "http"

    class EYamlKey(StrEnum):
        TYPE = "type"

    DEFAULT_TYPE = EType.NONE


@dataclass(frozen=True)
class TTcpSettingsConfig:
    accept_proxy_protocol: bool
    header: TTcpHeaderConfig

    class EYamlKey(StrEnum):
        ACCEPT_PROXY_PROTOCOL = "acceptProxyProtocol"
        HEADER = "header"

    DEFAULT_ACCEPT_PROXY_PROTOCOL = False


@dataclass(frozen=True)
class TRealityNestedSettingsConfig:
    public_key: str | None
    fingerprint: str
    server_name: str
    spider_x: str | None
    mldsa65_verify: str

    class EYamlKey(StrEnum):
        PUBLIC_KEY = "publicKey"
        FINGERPRINT = "fingerprint"
        SERVER_NAME = "serverName"
        SPIDER_X = "spiderX"
        MLDSA65_VERIFY = "mldsa65Verify"

    DEFAULT_FINGERPRINT = "chrome"
    DEFAULT_SERVER_NAME = ""
    DEFAULT_MLDSA65_VERIFY = ""


@dataclass(frozen=True)
class TRealitySettingsConfig:
    show: bool
    xver: int
    target: str | None
    dest: str | None
    server_names: list[str]
    private_key: str | None
    public_key: str | None
    min_client_ver: str
    max_client_ver: str
    max_timediff: int
    short_ids: list[str] | None
    short_ids_count: int
    mldsa65_seed: str
    spider_x: str | None
    spider_x_length: int
    settings: TRealityNestedSettingsConfig

    class EYamlKey(StrEnum):
        SHOW = "show"
        XVER = "xver"
        TARGET = "target"
        DEST = "dest"
        SERVER_NAMES = "serverNames"
        PRIVATE_KEY = "privateKey"
        PUBLIC_KEY = "publicKey"
        MIN_CLIENT_VER = "minClientVer"
        MAX_CLIENT_VER = "maxClientVer"
        MAX_TIMEDIFF = "maxTimediff"
        SHORT_IDS = "shortIds"
        SHORT_IDS_COUNT = "shortIdsCount"
        MLDSA65_SEED = "mldsa65Seed"
        SETTINGS = "settings"
        SPIDER_X = "spiderX"
        SPIDER_X_LENGTH = "spiderXLength"

    DEFAULT_SHOW = False
    DEFAULT_XVER = 0
    DEFAULT_MIN_CLIENT_VER = ""
    DEFAULT_MAX_CLIENT_VER = ""
    DEFAULT_MAX_TIMEDIFF = 0
    DEFAULT_SHORT_IDS_COUNT = 8
    DEFAULT_MLDSA65_SEED = ""
    DEFAULT_SPIDER_X_LENGTH = 15


@dataclass(frozen=True)
class TStreamSettingsConfig:
    network: "TStreamSettingsConfig.ENetwork"
    security: "TStreamSettingsConfig.ESecurity"
    tcp_settings: TTcpSettingsConfig
    reality_settings: TRealitySettingsConfig

    class ENetwork(StrEnum):
        TCP = "tcp"

    class ESecurity(StrEnum):
        REALITY = "reality"

    class EYamlKey(StrEnum):
        NETWORK = "network"
        SECURITY = "security"
        TCP_SETTINGS = "tcpSettings"
        REALITY_SETTINGS = "realitySettings"

    DEFAULT_NETWORK = ENetwork.TCP
    DEFAULT_SECURITY = ESecurity.REALITY


@dataclass(frozen=True)
class TInboundConfig:
    remark: str
    enable: bool
    expiry_time: int
    listen: str
    port: int
    protocol: str
    tag: str
    settings: TInboundSettingsConfig
    sniffing: TSniffingConfig | None
    stream_settings: TStreamSettingsConfig

    class EYamlKey(StrEnum):
        REMARK = "remark"
        ENABLE = "enable"
        EXPIRY_TIME = "expiryTime"
        LISTEN = "listen"
        PORT = "port"
        PROTOCOL = "protocol"
        TAG = "tag"
        SETTINGS = "settings"
        SNIFFING = "sniffing"
        STREAM_SETTINGS = "streamSettings"

    DEFAULT_ENABLE = True
    DEFAULT_EXPIRY_TIME = 0
    DEFAULT_LISTEN = ""
    DEFAULT_PROTOCOL = "vless"
    DEFAULT_REMARK_TEMPLATE = "in-{port}-tcp"
    DEFAULT_TAG_TEMPLATE = "in-{port}-tcp"
