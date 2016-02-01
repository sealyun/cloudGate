from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler

class ObjectStorageBaseHandler(HttpBaseHandler):   
    #TODO add init a processor
    def get(self):
        pass

class ContainerHandler(ObjectStorageBaseHandler):
    def get(self, account, container):
        pass

    def put(self, account, container):
        pass

    def delete(self, account, container):
        pass

class ObjectHandler(ObjectStorageBaseHandler):
    def put(self, account, container, object_):
        pass

    #????HTTP have no copy method, but openstack api define it!
    def copy(self, account, container, object_):
        pass

    def delete(self, account, container, object_):
        pass
