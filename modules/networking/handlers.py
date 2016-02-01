from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler

class NetworkingBaseHandler(HttpBaseHandler):   
    #TODO init a processor
    def get(self):
        pass

class NetworksHandler(NetworkingBaseHandler):
    def get(self):
        networks = self.p.queryNetworks()
        if networks:
            self.set_status(200)
        else:
            self.set_status(401)
            return 

        resp = {
            "networks":[
                {
                    "status": n.status,
                    "subnets": n.subnets,
                    "name": n.name,
                    "provider:physical_network": n.provider_physical_network,
                    "admin_state_up": n.admin_state_up,
                    "tenant_id": n.tenant_id,
                    "provider:network_type": n.provider_network_type,
                    "router:external": n.router_external,
                    "mtu": n.mtu,
                    "shared": n.shared,
                    "id": n.id,
                    "provider:segmentation_id": n.provider_segmentation_id
                }
                for n in networks
            ]
        }

        self.send_json(resp)

    #maybe bulk
    def post(self):
        network = json.loads(self.request.body)["network"]

        network = self.p.createNetwork(network)

        if network:
            self.set_status(201)
        else:
            self.set_status(400)
            return

        resp = {
            "network":{
                "status": network.status,
                "subnets": network.subnets,
                "name": network.name,
                "admin_state_up": network.admin_state_up,
                "tenant_id": network.tenant_id,
                "router:external": network.router_external,
                "mtu": network.mtu,
                "shared": network.shared,
                "id": network.id
            }
        }

        self.send_json(resp)

class NetworkHandler(NetworkingBaseHandler):
    def get(self, network_id):
        network = self.p.getNetwork(network_id)

        resp = {
            "network":{
                "status": network.status,
                "subnets": network.subnets,
                "name": network.name,
                "router:external": network.router_external,
                "admin_state_up": network.admin_state_up,
                "tenant_id": network.tenant_id,
                "mtu": network.mtu,
                "shared": network.shared,
                "port_security_enabled":network.port_security_enabled,
                "id": network.id
            }
        }

        self.send_json(resp)

    #add decorator fill network, if not exit set None
    def put(self, network_id):
        network = json.loads(self.request.body)
        network = self.p.updateNetwork(network_id, network)

        resp = {
            "network":{
                "status": network.status,
                "subnets": network.subnets,
                "name": network.name,
                "provider:physical_network": network.provider_physical_network,
                "admin_state_up": network.admin_state_up,
                "tenant_id": network.tenant_id,
                "provider:network_type": network.provider_network_type,
                "router:external": network.router_external,
                "mtu": network.mtu,
                "shared": network.shared,
                "port_security_enabled":network.port_security_enabled,
                "id": network.id,
                "provider:segmentation_id": network.provider_segmentation_id
            }
        }

        self.send_json(resp)

    def delete(self, network_id):
        if self.p.deleteNetwork(network_id):
            self.set_status(204)
        else:
            self.set_status(409)
            return

class SubnetsHandler(NetworkingBaseHandler):
    def get(self):
        display_name = self.get_argument("display_name", None)
        network_id = self.get_argument("network_id", None)
        gateway_ip = self.get_argument("gateway_ip", None)
        ip_version = self.get_argument("ip_version", None)
        cidr = self.get_argument("cidr", None)
        id = self.get_argument("id", None)
        enable_dhcp = self.get_argument("enable_dhcp", None)
        ipv6_ra_mode = self.get_argument("ipv6_ra_mode", None)
        ipv6_address_mode = self.get_argument("ipv6_address_mode", None)

        subnets = self.p.querySubnets(display_name, network_id,
                gateway_ip, ip_version, cidr, id, enable_dhcp,
                ipv6_ra_mode, ipv6_address_mode)

        resp = {
            "subnets":[
                {
                    "name": s.name,
                    "enable_dhcp": s.enable_dhcp,
                    "network_id": s.network_id,
                    "tenant_id": s.tenant_id,
                    "dns_nameservers": s.dns_nameservers,
                    "allocation_pools": s.allocation_pools,
                    "host_routes": s.host_routes,
                    "ip_version": s.ip_version,
                    "gateway_ip": s.gateway_ip,
                    "cidr": s.cidr,
                    "id": s.id
                }
                for s in subnets
            ]
        }

        self.send_json(resp)

    def post(self):
        pass

class SubnetHandler(NetworkingBaseHandler):
    def get(self, subnet_id):
        pass

    def put(self, subnet_id):
        pass

    def delete(self, subnet_id):
        pass

class PortsHandler(NetworkingBaseHandler):
    def get(self):
        pass

    def post(self):
        pass

class PortHandler(NetworkingBaseHandler):
    def get(self, port_id):
        pass

    def put(self, port_id):
        pass

    def delete(self, port_id):
        pass

class LoadbalancersHandler(NetworkingBaseHandler):
    def get(self):
        pass

    def post(self):
        pass

class LoadbalancerHandler(NetworkingBaseHandler):
    def get(self, lbaas_id):
        pass

    def put(self, lbaas_id):
        pass

    def delete(self, lbaas_id):
        pass

class LoadbalancerStatusesHandler(NetworkingBaseHandler):
    def get(self, lbaas_id):
        pass

class LbaasListenersHandler(NetworkingBaseHandler):
    def get(self):
        pass

    def post(self):
        pass

class LbaasListenerHandler(NetworkingBaseHandler):
    def get(self, listener_id):
        pass

    def put(self, listener_id):
        pass

    def delete(self, listener_id):
        pass

class LbaasPoolsHandler(NetworkingBaseHandler):
    def get(self):
        pass

    def post(self):
        pass

class LbaasPoolHandler(NetworkingBaseHandler):
    def get(self, pool_id):
        pass

    def put(self, pool_id):
        pass

    def delete(self, pool_id):
        pass

class LbaasPoolMembersHandler(NetworkingBaseHandler):
    def get(self, pool_id):
        pass

    def post(self, pool_id):
        pass

class LbaasPoolMemberHandler(NetworkingBaseHandler):
    def get(self, pool_id, member_id):
        pass

    def put(self, pool_id, member_id):
        pass

    def delete(self, pool_id, member_id):
        pass

class LbaasHealthMonitorsHandler(NetworkingBaseHandler):
    def post(self):
        pass

class LbaasHealthMonitorHandler(NetworkingBaseHandler):
    def get(self, health_moniter_id):
        pass

    def put(self, health_moniter_id):
        pass

    def delete(self, health_moniter_id):
        pass
