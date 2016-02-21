from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler
from api_factory import ComputeProcessorFac


class ComputeBaseHandler(HttpBaseHandler):
    def get_processor(self):
        token = self.request.headers["X-Auth-Token"]
        i = ComputeProcessorFac()
        self.p = i.create_processor(None, token)
        return self.p

    def get(self):
        #TODO
        pass


class ServersHandler(ComputeBaseHandler):
    def get(self, tenant_id):
        self.get_processor()
        changes_since = self.get_argument("changes_since", None)
        image = self.get_argument("image", None)
        flavor = self.get_argument("flavor", None)
        name = self.get_argument("name", None)
        status = self.get_argument("status", None)
        host = self.get_argument("host", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)
	
        print "ServersHandler get()"
        headers, body = self.p.queryServers(tenant_id, changes_since, image, flavor, name, status, host, limit, marker)

        if "x-openstack-request-id" in headers:
            self.set_header("x-openstack-request-id", headers["x-openstack-request-id"])

        self.send_json(body)

    def post(self, tenant_id):
        self.get_processor()
        server = json.loads(self.request.body)["server"]

        headers, body = self.p.createServer(tenant_id, server["name"],
                server["imageRef"],
                server["flavorRef"],
                server["metadata"])

        if "security_groups" in headers:
            self.set_header("security_groups", headers["security_groups"])
        if "user_data" in headers:
            self.set_header("user_data", headers["user_data"])
        if "os-availability-zone:availability_zone" in headers:
            self.set_header("os-availability-zone:availability_zone", headers["os-availability-zone:availability_zone"])

        self.send_json(body)


class ServersDetailHandler(ComputeBaseHandler):
    def get(self, tenant_id):
        self.get_processor()
        changes_since = self.get_argument("changes_since", None)
        image = self.get_argument("image", None)
        flavor = self.get_argument("flavor", None)
        name = self.get_argument("name", None)
        status = self.get_argument("status", None)
        host = self.get_argument("host", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)

        headers, body = self.p.queryServersDetails(tenant_id, changes_since, image,
                flavor, name, status, host, limit, marker)

        self.send_json(body)


class ServerHandler(ComputeBaseHandler):
    def get(self, tenant_id, server_id):
        self.get_processor()
        headers, body = self.p.queryServer(tenant_id, server_id)
        
        if "x-openstack-request-id" in headers:
            self.set_header("x-openstack-request-id", headers["x-openstack-request-id"])

        self.send_json(body)

    def put(self, tenant_id, server_id):
        self.get_processor()
        server = json.loads(self.request.body)["server"]
        body = {}
        if "name" in server:
            headers, body = self.p.updateServerName(tenant_id, server_id,
                    server["name"],
                    server["imageRef"],
                    server["flavorRef"],
                    server["metadata"])

        if "accessIPv4" in server or "accessIPv6" in server:
            headers, body = self.p.updateServerIP(tenant_id, server_id,
                    server["accessIPv4"],
                    server["accessIPv6"])

        if r"OS-DCF:diskConfig" in server:
            headers, body = self.p.updateServerOSDCFdiskConfig(tenant_id, server_id,
                    server[r"OS-DCF:diskConfig"])

        self.send_json(body)

    def delete(self, tenant_id, server_id):
        self.get_processor()
        self.p.deleteServer(tenant_id, server_id)


class ServerActionHandler(ComputeBaseHandler):
    def post(self, tenant_id, server_id):
        self.get_processor()
        action = json.loads(self.request.body)
        self.p.ServerAction(tenant_id, server_id, action)


class ServerVolumeHandler(ComputeBaseHandler):
    def post(self, tenant_id, server_id, volumeAttachment, volumeId, device):
        self.get_processor()
        headers, body = self.p.serverAttachVolume(tenant_id, server_id, volumeAttachment, volumeId, device)
        self.send_json(body)

    def get(self, tenant_id, server_id):
        self.get_processor()
        headers, body = self.p.serverListVolumes(tenant_id, server_id)
        self.send_json(body)

class VolumeAttachmentHandler(ComputeBaseHandler):
    def get(self, tenant_id, server_id, volumeAttachment, volumeId, device):
        self.get_processor()
        headers, body = self.p.volumeAttachmentDetail(tenant_id, server_id, attachment_id)
        self.send_json(body)

    def delete(self, tenant_id, server_id):
        self.get_processor()
        self.p.volumeAttachmentDetach(tenant_id, server_id)


class FlavorsHandler(ComputeBaseHandler):
    def get(self, tenant_id):
        self.get_processor()
        headers, body = self.p.queryFlavors(tenant_id)
        if "x-openstack-request-id" in headers:
            self.set_header("x-openstack-request-id", headers["x-openstack-request-id"])
        self.send_json(body)

    def post(self, tenant_id):
        self.get_processor()
        headers, body = self.p.createFlavor(tenant_id)
        self.send_json(body)


class FlavorHandler(ComputeBaseHandler):
    def get(self, tenant_id, flavor_id):
        self.get_processor()
        headers, body = self.p.queryFlavor(tenant_id, flavor_id)
        self.p.queryFlavor(tenant_id, flavor_id)
        if "x-openstack-request-id" in headers:
            self.set_header("x-openstack-request-id", headers["x-openstack-request-id"])
        self.send_json(body)

    def delete(self, tenant_id, flavor_id):
        self.get_processor()
        self.p.deleteFlavor(tenant_id, flavor_id)


class FlavorsDetailHandler(ComputeBaseHandler):
    def get(self, tenant_id):
        self.get_processor()
        headers, body = self.p.queryFlavorsDetail(tenant_id)
        if "x-openstack-request-id" in headers:
            self.set_header("x-openstack-request-id", headers["x-openstack-request-id"])
        self.send_json(body)


class ExtensionsHandler(ComputeBaseHandler):
    def get(self, ob):
        print "ExtensionsHandler get()"
        self.get_processor()
        processor = self.get_processor()
        extensions = processor.getExtensions()
        resp = {
            "extensions":extensions
        }
        self.send_json(resp)
