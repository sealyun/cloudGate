from handlers import *
from cloudGate.common.define import OBJECT_STORAGE_BASE_URL

urls = [
    (OBJECT_STORAGE_BASE_URL + r"/v1/([\w\-\_\d]+)", ObjectStorageBaseHandler),
    (OBJECT_STORAGE_BASE_URL + r"/v1/([^/]+)/([^/]+)", ContainerHandler), 
    (OBJECT_STORAGE_BASE_URL + r"/v1/([^/]+)/([^/]+)/([^/]+)", ObjectHandler),
]
