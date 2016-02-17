from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler
from api_factory import NetworkingProcessorFactory
import json


class NetworkingBaseHandler(HttpBaseHandler):
    def get_processor(self):
        token = self.request.headers["X-Auth-Token"]
        #print ("token:", token)
        factory = NetworkingProcessorFactory()
        return factory.getAliyunProcessor(token)

    def get(self):
        pass

class NetworksHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------NetworksHandler GET----------]"

        shared = self.get_argument("shared", None)
        tenantID = self.get_argument("tenant_id", None)
        routerExternal = self.get_argument("router:external", None)
        #print "shared: ", shared, ", type: ", type(shared)
        #print "tenant_id: ", tenantID, ", type: ", type(tenantID)
        #print "router:external: ", routerExternal, ", type: ", type(routerExternal)

        processor = self.get_processor()
        networks = processor.getNetwotks(shared, tenantID, routerExternal)
        if networks is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "networks":[
                {
                    "status": network["status"],
                    "subnets": network["subnets"],
                    "name": network["name"],
                    "provider:physical_network": network["provider:physical_network"],
                    "admin_state_up": network["admin_state_up"],
                    "tenant_id": network["tenant_id"],
                    "provider:network_type": network["provider:network_type"],
                    "router:external": network["router:external"],
                    "mtu": network["mtu"],
                    "shared": network["shared"],
                    "id": network["id"],
                    "provider:segmentation_id": network["provider:segmentation_id"],
                }
                for network in networks
            ]
        }

        self.send_json(resp)

    #maybe bulk
    def post(self):
        print "[----------NetworksHandler POST----------]"

        processor = self.get_processor()

        #print self.request.body
        body = json.loads(self.request.body)
        if "network" in body.keys():
            print "create network"
            inNetwork = body["network"]
            outNetwork = processor.createNetwork(inNetwork)
            if outNetwork is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "network":{
                            "status": outNetwork["status"],
                            "subnets": outNetwork["subnets"],
                            "name": outNetwork["name"],
                            "admin_state_up": outNetwork["admin_state_up"],
                            "tenant_id": outNetwork["tenant_id"],
                            "router:external": outNetwork["router:external"],
                            "mtu": outNetwork["mtu"],
                            "shared": outNetwork["shared"],
                            "id": outNetwork["id"]
                        }
                    }
            self.send_json(resp)
            return
        else:
            print "create networks"
            inNetworks = []
            inNetworks.append(body["networks"])
            outNetworks = processor.createNetworks(inNetworks)
            if outNetworks is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "networks":[
                    {
                        "status": network["status"],
                        "subnets": network["subnets"],
                        "name": network["name"],
                        "provider:physical_network": network["provider:physical_network"],
                        "admin_state_up": network["admin_state_up"],
                        "tenant_id": network["tenant_id"],
                        "mtu": network["mtu"],
                        "shared": network["shared"],
                        "id": network["id"],
                        "provider:segmentation_id": network["provider:segmentation_id"],
                    }
                    for network in outNetworks
                ]
            }
            self.send_json(resp)
            return

class NetworksExtensionsHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------NetworksExtensionsHandler GET----------]"

        processor = self.get_processor()
        extensions = processor.getAPIExtensions()
        resp = {
            "extensions":extensions
        }
        self.send_json(resp)

class NetworkHandler(NetworkingBaseHandler):
    def get(self, networkID):
        print "[----------NetworkHandler GET----------]"

        print "network id: ", networkID
        print "request body: ", self.request.body

        processor = self.get_processor()
        network = processor.getNetwork(networkID)
        if network is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "network":{
                "status": network["status"],
                "subnets": network["subnets"],
                "name": network["name"],
                "router:external": network["router:external"],
                "admin_state_up": network["admin_state_up"],
                "tenant_id": network["tenant_id"],
                "mtu": network["mtu"],
                "shared": network["shared"],
                "port_security_enabled":network["port_security_enabled"],
                "id": network["id"]
            }
        }

        self.send_json(resp)

    #add decorator fill network, if not exit set None
    def put(self, networkID):
        print "[----------NetworkHandler PUT----------]"

        inNetwork = json.loads(self.request.body)["network"]

        processor = self.get_processor()
        outNetwork = processor.updateNetwork(networkID, inNetwork)

        if outNetwork is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "network":{
                "status": outNetwork["status"],
                "subnets": outNetwork["subnets"],
                "name": outNetwork["name"],
                "provider:physical_network": outNetwork["provider:physical_network"],
                "admin_state_up": outNetwork["admin_state_up"],
                "tenant_id": outNetwork["tenant_id"],
                "provider:network_type": outNetwork["provider:network_type"],
                "router:external": outNetwork["router:external"],
                "mtu": outNetwork["mtu"],
                "shared": outNetwork["shared"],
                "port_security_enabled":outNetwork["port_security_enabled"],
                "id": outNetwork["id"],
                "provider:segmentation_id": outNetwork["provider_segmentation_id"]
            }

        }

        self.send_json(resp)

    def delete(self, networkID):
        print "[----------NetworkHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deleteNetwork(networkID):
            self.set_status(200)
            return
        else:
            self.set_status(400)
            return

class DHCPAgentsHandler(NetworkingBaseHandler):
    def get(self, network_id):
        print "[----------DHCPAgentsHandler GET----------]"

        processor = self.get_processor()
        agents = processor.getDHCPAgents(network_id)
        if agents is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "agents": agents
        }
        self.send_json(resp)

class SubnetsHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------SubnetsHandler GET----------]"

        displayName = self.get_argument("display_name", None)
        networkID = self.get_argument("network_id", None)
        gatewayIP = self.get_argument("gateway_ip", None)
        ipVersion = self.get_argument("ip_version", None)
        cidr = self.get_argument("cidr", None)
        id = self.get_argument("id", None)
        enableDHCP = self.get_argument("enable_dhcp", None)
        ipv6RaMode = self.get_argument("ipv6_ra_mode", None)
        ipv6AddressMode = self.get_argument("ipv6_address_mode", None)

        processor = self.get_processor()
        subnets = processor.getSubsets(displayName, networkID, gatewayIP, ipVersion, cidr, id, enableDHCP, ipv6RaMode, ipv6AddressMode)

        if subnets is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "subnets":[
                {
                    "name": s["name"],
                    "enable_dhcp": s["enable_dhcp"],
                    "network_id": s["network_id"],
                    "tenant_id": s["tenant_id"],
                    "dns_nameservers": s["dns_nameservers"],
                    "allocation_pools": s["allocation_pools"],
                    "host_routes": s["host_routes"],
                    "ip_version": s["ip_version"],
                    "gateway_ip": s["gateway_ip"],
                    "cidr": s["cidr"],
                    "id": s["id"]
                }
                for s in subnets
            ]
        }

        self.send_json(resp)

    #support bulk create subnet
    def post(self):
        print "[----------SubnetsHandler POST----------]"

        processor = self.get_processor()

        #print self.request.body
        body = json.loads(self.request.body)
        if "subnet" in body.keys():
            print "create subnet"
            inSubnet = body["subnet"]
            outSubnet = processor.createSubnet(inSubnet)
            if outSubnet is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "subnet":{
                    "name": outSubnet["name"],
                    "enable_dhcp": outSubnet["enable_dhcp"],
                    "network_id": outSubnet["network_id"],
                    "tenant_id": outSubnet["tenant_id"],
                    "dns_nameservers": outSubnet["dns_nameservers"],
                    "allocation_pools": outSubnet["allocation_pools"],
                    "host_routes": outSubnet["host_routes"],
                    "ip_version": outSubnet["ip_version"],
                    "gateway_ip": outSubnet["gateway_ip"],
                    "cidr": outSubnet["cidr"],
                    "id": outSubnet["id"]
                }
            }
            self.send_json(resp)
            return
        else:
            print "create subnets"
            inSubnets = []
            inSubnets.append(body["subnets"])
            outSubnets = processor.createSubnets(inSubnets)
            if outSubnets is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "subnets":[
                    {
                        "name": outSubnet["name"],
                        "enable_dhcp": outSubnet["enable_dhcp"],
                        "network_id": outSubnet["network_id"],
                        "tenant_id": outSubnet["tenant_id"],
                        "dns_nameservers": outSubnet["dns_nameservers"],
                        "allocation_pools": outSubnet["allocation_pools"],
                        "host_routes": outSubnet["host_routes"],
                        "ip_version": outSubnet["ip_version"],
                        "gateway_ip": outSubnet["gateway_ip"],
                        "cidr": outSubnet["cidr"],
                        "id": outSubnet["id"]
                    }
                    for outSubnet in outSubnets
                ]
            }
            self.send_json(resp)
            return

class SubnetHandler(NetworkingBaseHandler):
    def get(self, subnetID):
        print "[----------SubnetsHandler GET----------]"

        processor = self.get_processor()
        subset = processor.getSubnet(subnetID)

        if subset is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "subnet":{
                    "name": subset["name"],
                    "enable_dhcp": subset["enable_dhcp"],
                    "network_id": subset["network_id"],
                    "tenant_id": subset["tenant_id"],
                    "dns_nameservers": subset["dns_nameservers"],
                    "allocation_pools": subset["allocation_pools"],
                    "host_routes": subset["host_routes"],
                    "ip_version": subset["ip_version"],
                    "gateway_ip": subset["gateway_ip"],
                    "cidr": subset["cidr"],
                    "id": subset["id"]
                }
        }

        self.send_json(resp)

    def put(self, subnetID):
        print "[----------SubnetsHandler PUT----------]"

        inSubnet = json.loads(self.request.body)["subnet"]

        processor = self.get_processor()
        outSubnet = processor.updateSubnet(subnetID, inSubnet)

        if outSubnet is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "subnet":{
                "name": outSubnet["name"],
                "enable_dhcp": outSubnet["enable_dhcp"],
                "network_id": outSubnet["network_id"],
                "tenant_id": outSubnet["tenant_id"],
                "dns_nameservers": outSubnet["dns_nameservers"],
                "allocation_pools": outSubnet["allocation_pools"],
                "host_routes": outSubnet["host_routes"],
                "ip_version": outSubnet["ip_version"],
                "gateway_ip": outSubnet["gateway_ip"],
                "cidr": outSubnet["cidr"],
                "id": outSubnet["id"]
            }
        }

        self.send_json(resp)

    def delete(self, subnetID):
        print "[----------SubnetsHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deleteSubnet(subnetID):
            self.set_status(200)
            return
        else:
            self.set_status(400)
            return

class PortsHandler(NetworkingBaseHandler):
    def get(self):
        status = self.get_argument("status", None)
        displayName = self.get_argument("display_name", None)
        adminState = self.get_argument("admin_state", None)
        networkID = self.get_argument("network_id", None)
        tenantID = self.get_argument("tenant_id", None)
        deviceOwner = self.get_argument("device_owner", None)
        macAddress = self.get_argument("mac_address", None)
        portID = self.get_argument("port_id", None)
        securityGroups = self.get_argument("security_groups", None)
        deviceID = self.get_argument("device_id", None)

        processor = self.get_processor()
        ports = processor.getPorts(status, displayName, adminState, networkID, tenantID, deviceOwner, macAddress, portID, securityGroups, deviceID)
        if ports is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "ports":[
                {
                    "status": p["status"],
                    "name": p["name"],
                    "allowed_address_pairs": p["allowed_address_pairs"],
                    "admin_state_up": p["admin_state_up"],
                    "network_id": p["network_id"],
                    "tenant_id": p["tenant_id"],
                    "extra_dhcp_opts": p["extra_dhcp_opts"],
                    "device_owner": p["device_owner"],
                    "mac_address": p["mac_address"],
                    "fixed_ips": p["fixed_ips"],
                    "id": p["id"],
                    "security_groups": p["security_groups"],
                    "device_id": p["device_id"]
                }
                for p in ports
            ]
        }

        self.send_json(resp)

    def post(self):
        print "[----------PortsHandler POST----------]"

        processor = self.get_processor()

        #print self.request.body
        body = json.loads(self.request.body)
        if "port" in body.keys():
            print "create port"
            inPort = body["port"]
            outPort = processor.createPort(inPort)
            if outPort is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "port" :{
                    "status": outPort["status"],
                    "name": outPort["name"],
                    "allowed_address_pairs": outPort["allowed_address_pairs"],
                    "admin_state_up": outPort["admin_state_up"],
                    "network_id": outPort["network_id"],
                    "tenant_id": outPort["tenant_id"],
                    "extra_dhcp_opts": outPort["extra_dhcp_opts"],
                    "device_owner": outPort["device_owner"],
                    "mac_address": outPort["mac_address"],
                    "fixed_ips": outPort["fixed_ips"],
                    "id": outPort["id"],
                    "security_groups": outPort["security_groups"],
                    "device_id": outPort["device_id"]
                }
            }
            self.send_json(resp)
            return
        else:
            print "create ports"
            inPorts = []
            inPorts.append(body["ports"])
            outPorts = processor.createPorts(inPorts)
            if outPorts is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "ports":[
                    {
                        "status": outPort["status"],
                        "name": outPort["name"],
                        "allowed_address_pairs": outPort["allowed_address_pairs"],
                        "admin_state_up": outPort["admin_state_up"],
                        "network_id": outPort["network_id"],
                        "tenant_id": outPort["tenant_id"],
                        "extra_dhcp_opts": outPort["extra_dhcp_opts"],
                        "device_owner": outPort["device_owner"],
                        "mac_address": outPort["mac_address"],
                        "fixed_ips": outPort["fixed_ips"],
                        "id": outPort["id"],
                        "security_groups": outPort["security_groups"],
                        "device_id": outPort["device_id"]
                    }
                    for outPort in outPorts
                ]
            }
            self.send_json(resp)
            return

class PortHandler(NetworkingBaseHandler):
    def get(self, portID):
        print "[----------PortHandler GET----------]"

        processor = self.get_processor()
        port = processor.getPort(portID)

        if port is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "port":{
                "status": port["status"],
                "name": port["name"],
                "allowed_address_pairs": port["allowed_address_pairs"],
                "admin_state_up": port["admin_state_up"],
                "network_id": port["network_id"],
                "tenant_id": port["tenant_id"],
                "extra_dhcp_opts": port["extra_dhcp_opts"],
                "device_owner": port["device_owner"],
                "mac_address": port["mac_address"],
                "fixed_ips": port["fixed_ips"],
                "id": port["id"],
                "security_groups": port["security_groups"],
                "device_id": port["device_id"]
                }
        }

        self.send_json(resp)

    def put(self, portID):
        print "[----------PortHandler PUT----------]"

        inPort = json.loads(self.request.body)["port"]

        processor = self.get_processor()
        outPort = processor.updatePort(portID, inPort)

        if outPort is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "port":{
                "status": outPort["status"],
                "binding:host_id":outPort["binding:host_id"],
                "allowed_address_pairs": outPort["allowed_address_pairs"],
                "extra_dhcp_opts": outPort["extra_dhcp_opts"],
                "device_owner": outPort["device_owner"],
                "binding:profile":outPort["binding:profile"],
                "fixed_ips": outPort["fixed_ips"],
                "id": outPort["id"],
                "security_groups": outPort["security_groups"],
                "device_id": outPort["device_id"],
                "name": outPort["name"],
                "admin_state_up": outPort["admin_state_up"],
                "network_id": outPort["network_id"],
                "tenant_id": outPort["tenant_id"],
                "binding:vif_details": outPort["binding:vif_details"],
                "binding:vnic_type": outPort["binding:vnic_type"],
                "binding:vif_type": outPort["binding:vif_type"],
                "mac_address": outPort["mac_address"],
            }
        }

        self.send_json(resp)

    def delete(self, portID):
        print "[----------PortHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deletePort(portID):
            self.set_status(200)
            return
        else:
            self.set_status(400)
            return

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
