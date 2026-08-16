from enum import StrEnum


class EInboundEndpoint(StrEnum):
    ADD = "/inbounds/add"
    LIST = "/inbounds/list"


class ENodeEndpoint(StrEnum):
    ADD = "/nodes/add"
    LIST = "/nodes/list"

class EServerEndpoint(StrEnum):
    GET_NEW_X25519_CERT = "/server/getNewX25519Cert"
