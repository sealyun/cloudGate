from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler

class NetworkingBaseHandler(HttpBaseHandler):   
    #TODO init a processor
    def get(self):
        pass

class NetworksHandler(NetworkingBaseHandler):
    def get(self):
        pass

    def post(self):
        pass

class NetworkHandler(NetworkingBaseHandler):
    def get(self, network_id):
        pass

    def put(self, network_id):
        pass

    def delete(self, network_id):
        pass

class SubnetsHandler(NetworkingBaseHandler):
    def get(self):
        pass

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
