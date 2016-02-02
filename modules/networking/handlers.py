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

        if type(network) is list:
            #bulk create networks

            networks = self.p.createBuklNetworks(network)

            if n:
                self.set_status(201)
            else:
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
            return 

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

    #support bulk create subnet
    def post(self):
        subnet = json.loads(self.request.body)["subnet"]

        if type(subnet) is list:
            #bulk create subnet

            subnets = self.p.createBuklSubnets(subnet)

            if subnets:
                self.set_status(201)
            else:
                return

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
            return

        s = self.p.createSubnet(subnet["network_id"],
                subnet["ip_version"],
                subnet["cidr"])

        if s:
            self.set_status(201)
        else:
            return

        resp = {
            "subnet":{
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
        }

        self.send_json(resp)

class SubnetHandler(NetworkingBaseHandler):
    def get(self, subnet_id):
        s = self.p.querySubnet(subnet_id)

        resp = {
            "subnet":{
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
        }

        self.send_json(resp)

    def put(self, subnet_id):
        subnet = json.loads(self.request.body)["subnet"]

        subnet = self.p.updateSubnet(subnet_id, subnet)

        if subnet:
            self.set_status(200)
        else:
            return

        resp = {
            "subnet":{
                "name": subnet.name,
                "enable_dhcp": subnet.enable_dhcp,
                "network_id": subnet.network_id,
                "tenant_id": subnet.tenant_id,
                "dns_nameservers": subnet.dns_nameservers,
                "allocation_pools": subnet.allocation_pools,
                "host_routes": subnet.host_routes,
                "ip_version": subnet.ip_version,
                "gateway_ip": subnet.gateway_ip,
                "cidr": subnet.cidr,
                "id": subnet.id
            }
        }

        self.send_json(resp)

    def delete(self, subnet_id):
        if self.p.deleteSubnet(subnet_id):
            self.set_status(200)
        else:
            self.set_status(400)

class PortsHandler(NetworkingBaseHandler):
    def get(self):
        status = self.get_argument("status", None)
        display_name = self.get_argument("display_name", None)
        admin_state = self.get_argument("admin_state", None)
        network_id = self.get_argument("network_id", None)
        tenant_id = self.get_argument("tenant_id", None)
        device_owner = self.get_argument("device_owner", None)
        mac_address = self.get_argument("mac_address", None)
        port_id = self.get_argument("port_id", None)
        security_groups = self.get_argument("security_groups", None)
        device_id = self.get_argument("device_id", None)

        ports = self.p.queryPorts(status, display_name, admin_state,
                network_id, tenant_id, device_owner, mac_address,
                port_id, security_groups, device_id)

        if ports:
            self.set_status(200)
        else :
            self.set_status(400)
            return

        resp = {
            "ports":[
                {
                    "status": p.status,
                    "name": p.name,
                    "allowed_address_pairs": p.allowed_address_pairs,
                    "admin_state_up": p.admin_state_up,
                    "network_id": p.network_id,
                    "tenant_id": p.tenant_id,
                    "extra_dhcp_opts": p.extra_dhcp_opts,
                    "device_owner": p.device_owner,
                    "mac_address": p.mac_address,
                    "fixed_ips": p.fixed_ips,
                    "id": p.id,
                    "security_groups": p.security_groups,
                    "device_id": p.device_id
                }
                for p in ports
            ]
        }

        self.send_json(resp)

    def post(self):
        port = json.loads(self.request.body)["port"]

        if type(port) is list:
            ports = self.p.createBulkPorts(port)

            if ports:
                self.set_status(201)
            else:
                self.set_status(400)
                return

            resp = {
                "ports":[
                    {
                        "status": p.status,
                        "name": p.name,
                        "allowed_address_pairs": p.allowed_address_pairs,
                        "admin_state_up": p.admin_state_up,
                        "network_id": p.network_id,
                        "tenant_id": p.tenant_id,
                        "device_owner": p.device_owner,
                        "mac_address": p.mac_address,
                        "fixed_ips": p.fixed_ips,
                        "id": p.id,
                        "security_groups": p.security_groups,
                        "device_id": p.device_id
                    }
                    for p in ports
                ]
            }

            self.send_json(resp)
            return

        port = self.p.createPort(port["network_id"],
                port["name"],
                port["admin_state_up"])

        if port:
            self.set_status(201)
        else:
            self.set_status(400)
            return

        resp = {
            "port" :{
                "status": port.status,
                "name": port.name,
                "allowed_address_pairs": port.allowed_address_pairs,
                "admin_state_up": port.admin_state_up,
                "network_id": port.network_id,
                "tenant_id": port.tenant_id,
                "extra_dhcp_opts": port.extra_dhcp_opts,
                "device_owner": port.device_owner,
                "mac_address": port.mac_address,
                "fixed_ips": port.fixed_ips,
                "id": port.id,
                "security_groups": port.security_groups,
                "device_id": port.device_id
            }
        }

        self.send_json(resp)

class PortHandler(NetworkingBaseHandler):
    def get(self, port_id):
        port = self.queryPort(port_id)

        resp = {
            "port":{
                "status": port.status,
                "name": port.name,
                "allowed_address_pairs": port.allowed_address_pairs,
                "admin_state_up": port.admin_state_up,
                "network_id": port.network_id,
                "tenant_id": port.tenant_id,
                "extra_dhcp_opts": port.extra_dhcp_opts,
                "device_owner": port.device_owner,
                "mac_address": port.mac_address,
                "fixed_ips": port.fixed_ips,
                "id": port.id,
                "security_groups": port.security_groups,
                "device_id": port.device_id
            }
        }
        
        self.send_json(resp)

    def put(self, port_id):
        port = json.loads(self.request.body)

        port = self.p.updatePort(port_id, port)

        resp = {
            "port":{
                "status": port.status,
                "binding:host_id":port.binding_host_id,
                "allowed_address_pairs": port.allowed_address_pairs,
                "extra_dhcp_opts": port.extra_dhcp_opts,
                "device_owner": port.device_owner,
                "binding:profile":port.binding_profile,
                "fixed_ips": port.fixed_ips,
                "id": port.id,
                "security_groups": port.security_groups,
                "device_id": port.device_id
                "name": port.name,
                "admin_state_up": port.admin_state_up,
                "network_id": port.network_id,
                "tenant_id": port.tenant_id,
                "binding:vif_details": port.binding_vif_details,
                "binding:vnic_type": port.binding_vnic_type,
                "binding:vif_type": port.binding_vif_type,
                "mac_address": port.mac_address,
            }
        }

        self.send_json(resp)

    def delete(self, port_id):
        if self.p.deletePort(port_id):
            self.set_status(200)
        else:
            self.set_status(400)

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
