from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler

class ComputeBaseHandler(HttpBaseHandler):
    #the ProcessorFac return the real processor.
    p = ComputeProcessorFac()

    def get(self):
        #TODO
        pass

class ServersHandler(ComputeBaseHandler):
    def get(self, tenant_id):
        changes_since = self.get_argument("changes_since", None)
        image = self.get_argument("image", None)
        flavor = self.get_argument("flavor", None)
        name = self.get_argument("name", None)
        status = self.get_argument("status", None)
        host = self.get_argument("host", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)

        servers = self.p.queryServers(tenant_id, changes_since, image, flavor, name, status, host, limit, marker)

        resp = {
            "servers":[
                {
                    "id":s.id,
                    "links":[
                        {
                            "href":"http://",
                            "rel":"self"
                        },
                        {
                            "href":"http://",
                            "rel":"self"
                        }
                    ],
                    "name":s.name
                }
                for s in servers
            ]
        }

    def post(self, tenant_id):
        server = json.loads(self.request.body)["server"]

        server = self.p.createServer(tenant_id, server["name"],
                server["imageRef"],
                server["flavorRef"],
                server["metadata"])

        resp = {
            "server": {
                "OS-DCF:diskConfig": server.diskConfig,
                "adminPass": server.adminPass,
                "id": server.id,
                "links": [
                    {
                        "href": "http://",
                        "rel": "self"
                    }, 
                    {
                        "href": "http://",
                        "rel": "bookmark"
                    }
                ],
                "security_groups": server.security_groups
            } 
        }

        self.send_json(resp)

class ServersDetailHandler(ComputeBaseHandler):
    def get(self, tenant_id):
        changes_since = self.get_argument("changes_since", None)
        image = self.get_argument("image", None)
        flavor = self.get_argument("flavor", None)
        name = self.get_argument("name", None)
        status = self.get_argument("status", None)
        host = self.get_argument("host", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)

        servers = self.p.queryServersDetails(tenant_id, changes_since, image, 
                flavor, name, status, host, limit, marker)

        resp = {
            "servers":[
                {
                    "addresses":s.addresses,
                    "created":s.created,
                    "flavor":s.flavor,
                    "hostId":s.hostId,
                    "id":s.id,
                    "image":s.image,
                    "key_name":s.key_name,
                    "links": [
                        {
                            "href": "http://",
                            "rel": "self"
                        }, 
                        {
                            "href": "http://",
                            "rel": "bookmark"
                        }
                    ],
                    "metadata":s.metadata,
                    "name":s.name,
                    "accessIPv4":s.accessIPv4,
                    "accessIPv6":s.accessIPv6,
                    "config_drive":s.config_drive,
                    "OS-DCF:diskConfig":s.OS_DCF_diskConfig,
                    "OS-EXT-Az:availability_zone":s.OS_EXT_Az_availability_zone,
                    "OS-EXT-SRV-ATTR:host": s.OS_EXT_SRV_ATTR_host,
                    "OS-EXT-SRV-ATTR:hypervisor_hostname": s.OS_EXT_SRV_ATTR_hypervisor_hostname,
                    "OS-EXT-SRV-ATTR:instance_name": s.OS_EXT_SRV_ATTR_instance_name,
                    "OS-EXT-STS:power_state": s.OS_EXT_STS_power_state,
                    "OS-EXT-STS:task_state": s.OS_EXT_STS_task_state,
                    "OS-EXT-STS:vm_state": s.OS_EXT_STS_vm_state,
                    "os-extended-volumes:volumes_attached": s.os_extended_volumes_volumes_attached,
                    "OS-SRV-USG:launched_at": s.OS_SRV_USG_launched_at,
                    "OS-SRV-USG:terminated_at": s.OS_SRV_USG_terminated_at,
                    "progress":s.progress,
                    "security_groups":s.security_groups,
                    "status":s.status,
                    "host_status":s.host_status,
                    "tenant_id":s.tenant_id,
                    "updated":s.updated,
                    "user_id":s.user_id
                }
                for s in servers
            ]
        }

        self.send_json(resp)

class ServerHandler(ComputeBaseHandler):
    def get(self, tenant_id, server_id):
        s = self.p.queryServer(tenant_id, server_id)
        resp = {
            "servers":{
                "addresses":s.addresses,
                "created":s.created,
                "flavor":s.flavor,
                "hostId":s.hostId,
                "id":s.id,
                "image":s.image,
                "key_name":s.key_name,
                "links": [
                    {
                        "href": "http://",
                        "rel": "self"
                    }, 
                    {
                        "href": "http://",
                        "rel": "bookmark"
                    }
                ],
                "metadata":s.metadata,
                "name":s.name,
                "accessIPv4":s.accessIPv4,
                "accessIPv6":s.accessIPv6,
                "config_drive":s.config_drive,
                "OS-DCF:diskConfig":s.OS_DCF_diskConfig,
                "OS-EXT-Az:availability_zone":s.OS_EXT_Az_availability_zone,
                "OS-EXT-SRV-ATTR:host": s.OS_EXT_SRV_ATTR_host,
                "OS-EXT-SRV-ATTR:hypervisor_hostname": s.OS_EXT_SRV_ATTR_hypervisor_hostname,
                "OS-EXT-SRV-ATTR:instance_name": s.OS_EXT_SRV_ATTR_instance_name,
                "OS-EXT-STS:power_state": s.OS_EXT_STS_power_state,
                "OS-EXT-STS:task_state": s.OS_EXT_STS_task_state,
                "OS-EXT-STS:vm_state": s.OS_EXT_STS_vm_state,
                "os-extended-volumes:volumes_attached": s.os_extended_volumes_volumes_attached,
                "OS-SRV-USG:launched_at": s.OS_SRV_USG_launched_at,
                "OS-SRV-USG:terminated_at": s.OS_SRV_USG_terminated_at,
                "progress":s.progress,
                "security_groups":s.security_groups,
                "status":s.status,
                "host_status":s.host_status,
                "tenant_id":s.tenant_id,
                "updated":s.updated,
                "user_id":s.user_id
            }
        }

        self.send_json(resp)
    
    def put(self, tenant_id, server_id):
        server = json.loads(self.request.body)["server"]

        if "name" in server:
            s = self.p.updateServerName(tenant_id, server_id,
                    server["name"],
                    server["imageRef"],
                    server["flavorRef"],
                    server["metadata"])

        if "accessIPv4" in server or "accessIPv6" in server:
            s = self.p.updateServerIP(tenant_id, server_id,
                    server["accessIPv4"],
                    server["accessIPv6"])

        if r"OS-DCF:diskConfig" in server:
            s = self.p.updateServerOS_DCF_diskConfig(tenant_id, server_id,
                    server[r"OS-DCF:diskConfig"])

        resp = {
            "id":s.id,
            "tenant_id":tenant_id,
            "user_id":s.user_id,
            "name":s.name,
            "created":s.created,
            "updated":s.updated,
            "hostId":s.hostId,
            "accessIPv4":s.accessIPv4,
            "accessIPv6":s.accessIPv6,
            "progress":s.progress,
            "status":s.status,
            "image":s.image,
            "flavor":s.flavor,
            "metadata":s.metadata,
            "addresses":s.addresses,
            "links":[
                {
                    "rel":"self",
                    "href":"http://"
                },
                {
                    "rel":"bookmark",
                    "href":"http://"
                },
            ]
        }

        self.send_json(resp)

    def delete(self, tenant_id, server_id):
        self.p.deleteServer(tenant_id, server_id)

class ServerActionHandler(ComputeBaseHandler):
    def post(self, tenant_id, server_id):
        action = json.loads(self.request.body)
        self.p.ServerAction(tenant_id, server_id, action)
