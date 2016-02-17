from handlers import *
from cloudGate.common.define import *

urls = [
    (NETWORKING_BASE_URL, NetworkingBaseHandler),
    (NETWORKING_BASE_URL + r"/v2.0/networks.json", NetworksHandler),
    (NETWORKING_BASE_URL + r"/v2.0/extensions.json", NetworksExtensionsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/networks/([a-z0-9A-Z\-]+).json", NetworkHandler),
    (NETWORKING_BASE_URL + r"/v2.0/networks/([a-z0-9A-Z\-]+)/dhcp-agents.json", DHCPAgentsHandler),

    (NETWORKING_BASE_URL + r"/v2.0/subnets.json", SubnetsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/subnets/([a-z0-9A-Z\-]+).json", SubnetHandler),

    (NETWORKING_BASE_URL + r"/v2.0/ports.json", PortsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/ports/([a-z0-9A-Z\-]+).json", PortHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/loadbalancers", LoadbalancersHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/loadbalancers/([a-z0-9A-Z\-]+)", LoadbalancerHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/loadbalancers/([a-z0-9A-Z\-]+)/statuses", LoadbalancerStatusesHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/listeners", LbaasListenersHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/listeners/([a-z0-9A-Z\-]+)", LbaasListenerHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools", LbaasPoolsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools/([a-z0-9A-Z\-]+)", LbaasPoolHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools/([a-z0-9A-Z\-]+)/members", LbaasPoolMembersHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/pools/([a-z0-9A-Z\-]+)/members/([a-z0-9A-Z\-]+)", LbaasPoolMemberHandler),

    (NETWORKING_BASE_URL + r"/v2.0/lbaas/health_monitors", LbaasHealthMonitorsHandler),
    (NETWORKING_BASE_URL + r"/v2.0/lbaas/health_monitor/([a-z0-9A-Z\-]+)", LbaasHealthMonitorHandler),
]

