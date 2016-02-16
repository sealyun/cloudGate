from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler
from api_factory import NetworkingProcessorFactory
import json


class NetworkingBaseHandler(HttpBaseHandler):
    def __init__(self):
        token = self.request.headers["X-Auth-Token"]
        print ("-----get token:", token)
        factory = NetworkingProcessorFactory()
        self._processor = factory.getAliyunProcessor(token)

    def get(self):
        pass

class NetworksHandler(NetworkingBaseHandler):
    def get(self):
        networks = self._processor.queryNetwotks()
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

            networks = self.p.createBulkNetworks(network)

            if network:
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
                "device_id": port.device_id,
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
        loadbalancers = self.p.queryLoadbalancers()

        resp = {
            "loadbalancers":[
                {
                    "description": l.destination,
                    "admin_state_up": l.admin_state_up,
                    "tenant_id": l.tenant_id,
                    "provisioning_status": l.provisioning_status,
                    "listeners": l.listeners,
                    "vip_address": l.vip_address,
                    "vip_subnet_id": l.vip_subnet_id,
                    "id": l.id,
                    "operating_status": l.operating_status,
                    "name": l.name
                }
                for l in loadbalancers
            ]
        }

        self.send_json(resp)

    def post(self):
        loadbalancer = json.loads(self.request.body)["loadbalancer"]

        loadbalancer = self.p.createLoadbalancer(loadbalancer["name"],
                loadbalancer["destination"],
                loadbalancer["tenant_id"],
                loadbalancer["vip_subnet_id"],
                loadbalancer["vip_address"],
                loadbalancer["admin_state_up"],
                loadbalancer["provider"])

        if loadbalancer:
            self.set_status(201)
        else:
            self.set_status(400)
            return

        resp = {
            "loadbalancer":{
                "description": loadbalancer.destination,
                "admin_state_up": loadbalancer.admin_state_up,
                "tenant_id": loadbalancer.tenant_id,
                "provisioning_status": loadbalancer.provisioning_status,
                "listeners": loadbalancer.listeners,
                "vip_address": loadbalancer.vip_address,
                "vip_subnet_id": loadbalancer.vip_subnet_id,
                "id": loadbalancer.id,
                "operating_status": loadbalancer.operating_status,
                "name": loadbalancer.name
            }
        }

        self.send_json(resp)

class LoadbalancerHandler(NetworkingBaseHandler):
    def get(self, lbaas_id):
        loadbalancer = self.p.queryLoadbalancer(lbaas_id)

        if loadbalancer:
            self.set_status(200)
        else:
            self.set_status(403)
            return

        resp = {
            "loadbalancer":{
                "description": loadbalancer.destination,
                "admin_state_up": loadbalancer.admin_state_up,
                "tenant_id": loadbalancer.tenant_id,
                "provisioning_status": loadbalancer.provisioning_status,
                "listeners": loadbalancer.listeners,
                "vip_address": loadbalancer.vip_address,
                "vip_subnet_id": loadbalancer.vip_subnet_id,
                "id": loadbalancer.id,
                "operating_status": loadbalancer.operating_status,
                "name": loadbalancer.name
            }
        }

        self.send_json(resp)

    def put(self, lbaas_id):
        loadbalancer = json.loads(self.request.body)["loadbalancer"]

        loadbalancer = self.updateLoadbalancer(lbaas_id, 
                loadbalancer["admin_state_up"],
                loadbalancer["destination"],
                loadbalancer["name"])

        if loadbalancer:
            self.set_status(200)
        else:
            self.set_status(401)
            return

        resp = {
            "loadbalancer":{
                "admin_state_up": loadbalancer.admin_state_up,
                "description": loadbalancer.destination,
                "id": loadbalancer.id,
                "listeners": loadbalancer.listeners,
                "name": loadbalancer.name,
                "operating_status": loadbalancer.operating_status,
                "provisioning_status": loadbalancer.provisioning_status,
                "tenant_id": loadbalancer.tenant_id,
                "vip_address": loadbalancer.vip_address,
                "vip_subnet_id": loadbalancer.vip_subnet_id,
            }
        }

        self.send_json(resp)



    def delete(self, lbaas_id):
        if self.p.deleteLoadbalancer(lbaas_id):
            self.set_status(204)
        else:
            self.set_status(403)
            return

class LoadbalancerStatusesHandler(NetworkingBaseHandler):
    def get(self, lbaas_id):
        #TODO
        """
        loadbalancer
            |___listener1
            |       |_____pool1                   
            |       |       |_____member1
            |       |       |_____member2
            |       |______pool2
            |___listener2
        """
        pass

class LbaasListenersHandler(NetworkingBaseHandler):
    def get(self):
        listeners = self.p.queryListeners()

        resp = {
            "listeners":[
                {
                    "admin_state_up":l.admin_state_up,
                    "connection_limit":l.connection_limit,
                    "default_pool_id":l.default_pool_id,
                    "description":l.description,
                    "id":l.id,
                    "loadbalancers":l.loadbalancers,
                    "name":l.name,
                    "protocol":l.protocol,
                    "protocol_port":l.port,
                    "tenant_id":l.tenant_id,
                    "default_tls_container_ref":l.default_tls_container_ref,
                    "sni_container_refs":l.sni_container_refs,
                }
                for l in listeners
            ]
        }

        self.send_json(resp)

    def post(self):
        listener = json.loads(self.request.body)["listener"]

        listener = self.p.createListener(listener["admin_state_up"],
                listener["connection_limit"],
                listener["description"],
                listener["loadbalancer_id"],
                listener["name"],
                listener["protocol"],
                listener["protocol_port"],
                listener["default_tls_container_ref"],
                listener["sni_container_refs"])

        if listener:
            self.set_status(201)
        else:
            self.set_status(400)
            return

        resp = {
            "listener":{
                "admin_state_up":listener.admin_state_up,
                "connection_limit":listener.connection_limit,
                "default_pool_id":listener.default_pool_id,
                "description":listener.description,
                "id":listener.id,
                "loadbalancers":listener.loadbalancers,
                "name":listener.name,
                "protocol":listener.protocol,
                "protocol_port":listener.port,
                "tenant_id":listener.tenant_id,
                "default_tls_container_ref":listener.default_tls_container_ref,
                "sni_container_refs":listener.sni_container_refs,
            }
        }

        self.send_json(resp)

class LbaasListenerHandler(NetworkingBaseHandler):
    def get(self, listener_id):
        listener = self.queryListener(listener_id)

        if listener:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "listener":{
                "admin_state_up":listener.admin_state_up,
                "connection_limit":listener.connection_limit,
                "default_pool_id":listener.default_pool_id,
                "description":listener.description,
                "id":listener.id,
                "loadbalancers":listener.loadbalancers,
                "name":listener.name,
                "protocol":listener.protocol,
                "protocol_port":listener.port,
                "tenant_id":listener.tenant_id,
                "default_tls_container_ref":listener.default_tls_container_ref,
                "sni_container_refs":listener.sni_container_refs,
            }
        }

        self.send_json(resp)

    def put(self, listener_id):
        listener = json.loads(self.request.body)["listener"]

        listener = self.p.updateListener(listener_id,
                listener["admin_state_up"],
                listener["connection_limit"],
                listener["description"],
                listener["name"],
                listener["default_tls_container_ref"],
                listener["sni_container_refs"])

        if listener:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "listener":{
                "admin_state_up":listener.admin_state_up,
                "connection_limit":listener.connection_limit,
                "default_pool_id":listener.default_pool_id,
                "description":listener.description,
                "id":listener.id,
                "loadbalancers":listener.loadbalancers,
                "name":listener.name,
                "protocol":listener.protocol,
                "protocol_port":listener.port,
                "tenant_id":listener.tenant_id,
                "default_tls_container_ref":listener.default_tls_container_ref,
                "sni_container_refs":listener.sni_container_refs,
            }
        }

        self.send_json(resp)

    def delete(self, listener_id):
        if self.p.deleteListener(listener_id):
            self.set_status(204)
        else:
            self.set_status(400)

class LbaasPoolsHandler(NetworkingBaseHandler):
    def get(self):
        pools = self.p.getLbaasPools()

        if pools:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "pools":[
                {
                    "status": p.status,
                    "lb_method": p.lb_method,
                    "protocol": p.protocol,
                    "description": p.description,
                    "health_monitors": p.health_moniters,
                    "subnet_id": p.subnet_id,
                    "tenant_id": p.tenant_id,
                    "admin_state_up": p.admin_state_up,
                    "name": p.name,
                    "members": p.members,
                    "id": p.id,
                    "vip_id": p.vip_id
                }
                for p in pools
            ]
        }

        self.send_json(resp)

    def post(self):
        pool = json.loads(self.request.body)["pool"]

        pool = self.p.createPool(pool["admin_state_up"],
                pool["description"],
                pool["lb_algorithm"],
                pool["listener_id"],
                pool["name"],
                pool["protocol"],
                pool["session_persistence"])

        if pool:
            self.set_status(201)
        else:
            self.set_status(409)
            return

        resp = {
            "pool":{
                "admin_state_up": pool.admin_state_up,
                "description": pool.description,
                "healthmonitor_id": pool.healthmoniter_id,
                "id": pool.id,
                "lb_algorithm": pool.lb_algorithm,
                "listeners": pool.listeners,
                "members": pool.members,
                "name": pool.name,
                "protocol": pool.protocol,
                "session_persistence": pool.session_persistence,
                "tenant_id": pool.tenant_id 
            }
        }

        self.send_json(resp)

class LbaasPoolHandler(NetworkingBaseHandler):
    def get(self, pool_id):
        pool = self.p.queryLbaasPool(pool_id)

        resp = {
            "pool":{
                "admin_state_up": pool.admin_state_up,
                "description": pool.description,
                "healthmonitor_id": pool.healthmoniter_id,
                "id": pool.id,
                "lb_algorithm": pool.lb_algorithm,
                "listeners": pool.listeners,
                "members": pool.members,
                "name": pool.name,
                "protocol": pool.protocol,
                "tenant_id": pool.tenant_id 
            }
        }

        self.send_json(resp)

    def put(self, pool_id):
        pool = json.loads(self.request.body)["pool"]

        pool = self.p.updateLbaasPool(pool_id, pool["name"],
                pool["description"],
                pool["admin_state_up"],
                pool["lb_algorithm"],
                pool["session_persistence"])

        if pool:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "pool":{
                "status": pool.status,
                "lb_method": pool.lb_method,
                "protocol": pool.protocol,
                "description": pool.description,
                "health_monitors": pool.health_moniters,
                "subnet_id": pool.subnet_id,
                "tenant_id": pool.tenant_id,
                "admin_state_up": pool.admin_state_up,
                "name": pool.name,
                "members": pool.members,
                "id": pool.id,
                "vip_id": pool.vip_id 
            }
        }

        self.send_json(resp)

    def delete(self, pool_id):
        if self.p.deleteLbaasPool(pool_id):
            self.set_status(204)
        else:
            self.set_status(400)
            return

class LbaasPoolMembersHandler(NetworkingBaseHandler):
    def get(self, pool_id):
        members = self.p.queryLbaasPoolMembers(pool_id)

        resp = {
            "members":[
                {
                    "address": m.address,
                    "admin_state_up": m.admin_state_up,
                    "id": m.id,
                    "protocol_port": m.protocol_port,
                    "subnet_id": m.subnet_id,
                    "tenant_id": m.tenant_id,
                    "weight": m.weight
                }
                for m in members
            ]
        }

        self.send_json(resp)

    def post(self, pool_id):
        member = json.loads(self.request.body)["member"]

        member = self.p.addMemberToPool(pool_id,
                member["address"],
                member["admin_state_up"],
                member["protocol_port"],
                member["subnet_id"],
                member["weight"])

        if member:
            self.set_status(201)
        else:
            self.set_status(400)
            return

        resp = {
            "member":{
                "address": member.address,
                "admin_state_up": member.admin_state_up,
                "id": member.id,
                "protocol_port": member.protocol_port,
                "subnet_id": member.subnet_id,
                "tenant_id": member.tenant_id,
                "weight": member.weight
            }
        }

        self.send_json(resp)

class LbaasPoolMemberHandler(NetworkingBaseHandler):
    def get(self, pool_id, member_id):
        member = self.p.queryLbaasPoolMember(pool_id, member_id)

        if member:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "member":{
                "address": member.address,
                "admin_state_up": member.admin_state_up,
                "id": member.id,
                "protocol_port": member.protocol_port,
                "subnet_id": member.subnet_id,
                "tenant_id": member.tenant_id,
                "weight": member.weight
            }
        }

        self.send_json(resp)

    def put(self, pool_id, member_id):
        member = json.loads(self.request.body)["member"]

        if member:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "member":{
                "address": member.address,
                "admin_state_up": member.admin_state_up,
                "id": member.id,
                "protocol_port": member.protocol_port,
                "subnet_id": member.subnet_id,
                "tenant_id": member.tenant_id,
                "weight": member.weight
            }
        }

        self.send_json(resp)

    def delete(self, pool_id, member_id):
        if self.p.deleteLbaasPoolMember(pool_id, member_id):
            self.set_status(204)
        else:
            self.set_status(400)

class LbaasHealthMonitorsHandler(NetworkingBaseHandler):
    def post(self):
        health_moniter = json.loads(self.request.body)["health_moniter"]

        health_moniter = self.p.createLbaasHealthMonitor(health_moniter["admin_state_up"],
                health_moniter["delay"],
                health_moniter["expected_codes"],
                health_moniter["http_method"],
                health_moniter["max_retries"],
                health_moniter["pool_id"],
                health_moniter["timeout"],
                health_moniter["type"],
                health_moniter["url_path"])

        if health_moniter:
            self.set_status(201)
        else:
            self.set_status(400)
            return

        resp = {
            "health_moniter":{
                "admin_state_up": health_moniter.admin_state_up,
                "delay": health_moniter.delay,
                "expected_codes": health_moniter.expected_codes,
                "http_method": health_moniter.http_method,
                "id": health_moniter.id,
                "max_retries": health_moniter.max_retries,
                "pools": health_moniter.pools,
                "tenant_id": health_moniter.tenant_id,
                "timeout": health_moniter.timeout,
                "type": health_moniter.type,
                "url_path": health_moniter.url_path 
            }
        }

        self.send_json(resp)

class LbaasHealthMonitorHandler(NetworkingBaseHandler):
    def get(self, health_moniter_id):
        health_moniter = self.p.queryLbaasHealthMonitor(health_moniter_id)

        if health_moniter:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "health_moniter":{
                "admin_state_up": health_moniter.admin_state_up,
                "delay": health_moniter.delay,
                "expected_codes": health_moniter.expected_codes,
                "http_method": health_moniter.http_method,
                "id": health_moniter.id,
                "max_retries": health_moniter.max_retries,
                "pools": health_moniter.pools,
                "tenant_id": health_moniter.tenant_id,
                "timeout": health_moniter.timeout,
                "type": health_moniter.type,
                "url_path": health_moniter.url_path 
            }
        }

        self.send_json(resp)

    def put(self, health_moniter_id):
        health_moniter = json.loads(self.request.body)["health_moniter"]

        health_moniter = self.p.updateLbaasHealthMoniter(health_moniter_id,
                health_moniter["admin_state_up"],
                health_moniter["delay"],
                health_moniter["expected_codes"],
                health_moniter["http_method"],
                health_moniter["max_retries"],
                health_moniter["timeout"],
                health_moniter["url_path"])

        if health_moniter:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "health_moniter":{
                "admin_state_up": health_moniter.admin_state_up,
                "delay": health_moniter.delay,
                "expected_codes": health_moniter.expected_codes,
                "http_method": health_moniter.http_method,
                "id": health_moniter.id,
                "max_retries": health_moniter.max_retries,
                "pools": health_moniter.pools,
                "tenant_id": health_moniter.tenant_id,
                "timeout": health_moniter.timeout,
                "type": health_moniter.type,
                "url_path": health_moniter.url_path 
            }
        }

        self.send_json(resp)

    def delete(self, health_moniter_id):
        if self.p.deleteLbaasHealthMonitor(health_moniter_id):
            self.set_status(204)
        else:
            self.set_status(400)
