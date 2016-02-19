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
        servers = self.p.queryServers(tenant_id, changes_since, image, flavor, name, status, host, limit, marker)
        self.send_json(servers)

    def post(self, tenant_id):
        self.get_processor()
        server = json.loads(self.request.body)["server"]

        server = self.p.createServer(tenant_id, server["name"],
                server["imageRef"],
                server["flavorRef"],
                server["metadata"])

        self.send_json(server)

class ServersDetailHandler(ComputeBaseHandler):
    def get(self, tenant_id):
	print "ServersDetailHandler get()"
        self.get_processor()
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
        self.send_json(servers)

class ServerHandler(ComputeBaseHandler):
    def get(self, tenant_id, server_id):
	self.get_processor()
        s = self.p.queryServer(tenant_id, server_id)

        self.send_json(s)

    def put(self, tenant_id, server_id):
        self.get_processor()
        server = json.loads(self.request.body)["server"]
	s = {}
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
            s = self.p.updateServerOSDCFdiskConfig(tenant_id, server_id,
                    server[r"OS-DCF:diskConfig"])

        self.send_json(s)

    def delete(self, tenant_id, server_id):
        self.get_processor()
        self.p.deleteServer(tenant_id, server_id)

class ServerActionHandler(ComputeBaseHandler):
    def post(self, tenant_id, server_id):
	print "ServerActionHandler post()"
        self.get_processor()
        action = json.loads(self.request.body)
        self.p.ServerAction(tenant_id, server_id, action)

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
