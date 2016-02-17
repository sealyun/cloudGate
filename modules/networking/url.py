from handlers import *
from cloudGate.common.define import *

urls = [
    (NETWORKING_BASE_URL, NetworkingBaseHandler),
    (NETWORKING_BASE_URL + r"/v2.0/networks.json", NetworksHandler),
    (NETWORKING_BASE_URL + r"/v2.0/extensions.json", NetworksExtensionsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/networks/(^[a-zA-Z0-9\.@\-_]+$).json", NetworkHandler),
    (NETWORKING_BASE_URL + r"/v2.0/networks/(^[a-zA-Z0-9\.@\-_]+$)/dhcp-agents.json", DHCPAgentsHandler),

    (NETWORKING_BASE_URL + r"/v2.0/subnets.json", SubnetsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/subnets/(^[a-zA-Z0-9\.@\-_]+$).json", SubnetHandler),

    (NETWORKING_BASE_URL + r"/v2.0/ports.json", PortsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/ports/(^[a-zA-Z0-9\.@\-_]+$).json", PortHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/loadbalancers", LoadbalancersHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/loadbalancers/(^[a-zA-Z0-9\.@\-_]+$)", LoadbalancerHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/loadbalancers/(^[a-zA-Z0-9\.@\-_]+$)/statuses", LoadbalancerStatusesHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/listeners", LbaasListenersHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/listeners/(^[a-zA-Z0-9\.@\-_]+$)", LbaasListenerHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools", LbaasPoolsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools/(^[a-zA-Z0-9\.@\-_]+$)", LbaasPoolHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools/(^[a-zA-Z0-9\.@\-_]+$)/members", LbaasPoolMembersHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools/(^[a-zA-Z0-9\.@\-_]+$)/members/(^[a-zA-Z0-9\.@\-_]+$)", LbaasPoolMemberHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/health_monitors", LbaasHealthMonitorsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/health_monitor/(^[a-zA-Z0-9\.@\-_]+$)", LbaasHealthMonitorHandler),
]

