from handlers import *

urls = [
    (NETWORKING_BASE_URL, NetworkingBaseHandler),
    (NETWORKING_BASE_URL + "/v2/networks", NetworksHandler),
    (NETWORKING_BASE_URL + "/v2/networks/(.*)", NetworkHandler),

    (NETWORKING_BASE_URL + "/v2.0/subnets", SubnetsHandler),
    (NETWORKING_BASE_URL + "/v2.0/subnet", SubnetHandler),

    (NETWORKING_BASE_URL + "/v2.0/ports", PortsHandler),
    (NETWORKING_BASE_URL + "/v2.0/ports/(.*)", PortHandler), 

    (NETWORKING_BASE_URL + "/v2.0/lbaas/loadbalancers", LoadbalancersHandler), 
    (NETWORKING_BASE_URL + "/v2.0/lbaas/loadbalancers/(.*)", LoadbalancerHandler), 
    (NETWORKING_BASE_URL + "/v2.0/lbaas/loadbalancers/(.*)/statuses", LoadbalancerStatusesHandler), 

    (NETWORKING_BASE_URL + "/v2.0/lbaas/listeners", LbaasListenersHandler), 
    (NETWORKING_BASE_URL + "/v2.0/lbaas/listeners/(.*)", LbaasListenerHandler), 

    (NETWORKING_BASE_URL + "/v2.0/lbaas/pools", LbaasPoolsHandler), 
    (NETWORKING_BASE_URL + "/v2.0/lbaas/pools/(.*)", LbaasPoolHandler), 
    (NETWORKING_BASE_URL + "/v2.0/lbaas/pools/(.*)/members", LbaasPoolMembersHandler), 
    (NETWORKING_BASE_URL + "/v2.0/lbaas/pools/(.*)/members/(.*)", LbaasPoolMemberHandler), 

    (NETWORKING_BASE_URL + "/v2.0/lbaas/health_monitors", LbaasHealthMonitorsHandler), 
    (NETWORKING_BASE_URL + "/v2.0/lbaas/health_monitor/(.*)", LbaasHealthMonitorHandler),  
]

