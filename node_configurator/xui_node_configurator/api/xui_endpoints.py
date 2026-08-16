from enum import StrEnum


class EInboundEndpoint(StrEnum):
    ADD = "/inbounds/add"


class ENodeEndpoint(StrEnum):
    ADD = "/nodes/add"

class EServerEndpoint(StrEnum):
    GET_NEW_X25519_CERT = "/server/getNewX25519Cert"
