id: "__NODE_ID__"
role: "slave"

panel:
  api_url: "__SLAVE_API_URL__"
  token: "__SLAVE_API_TOKEN__"
  verify_ssl: false
  timeout: 30

parent_master:
  id: "__MASTER_ID__"

  panel:
    api_url: "__MASTER_API_URL__"
    token: "__MASTER_API_TOKEN__"
    verify_ssl: false
    timeout: 30

  node_registration:
    name: "__NODE_ID__"
    remark: "__NODE_REMARK__"
    verify_ssl: false

children: []

inbounds:
  - remark: "__INBOUND_REMARK__"
    enable: true
    expiryTime: 0
    listen: ""
    port: __INBOUND_PORT__
    protocol: "vless"
    tag: "in-__INBOUND_PORT__-tcp"

    settings:
      clients: []
      decryption: "none"
      encryption: "none"

    sniffing:
      enabled: false

    streamSettings:
      network: "tcp"
      security: "reality"

      tcpSettings:
        acceptProxyProtocol: false
        header:
          type: "none"

      realitySettings:
        show: false
        xver: 0
        target: "__REALITY_TARGET__"

        serverNames:
__REALITY_SERVER_NAMES__

        minClientVer: ""
        maxClientVer: ""
        maxTimediff: 0

        shortIdsCount: __SHORT_IDS_COUNT__
        spiderXLength: __SPIDER_X_LENGTH__

        settings:
          fingerprint: "__REALITY_FINGERPRINT__"
          serverName: ""
