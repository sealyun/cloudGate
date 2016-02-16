from handlers import *
from cloudGate.common.define import IMAGE_SERVICE_BASE_URL

urls = [
    (IMAGE_SERVICE_BASE_URL, ImageBaseHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images", ImagesHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images/(.*)", ImageHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images/(.*)/actions/reactivate", ImageActionReactivateHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images/(.*)/actions/deactivate", ImageActionDeactivateHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images/(.*)/file", ImageFileHandler),

    (IMAGE_SERVICE_BASE_URL + r"/v1/images", ImagesHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v1/images/detail", ImagesHandler),
]
