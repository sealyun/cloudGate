from handlers import *

urls = [
    (IMAGE_SERVICE_BASE_URL, ImageBaseHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images", ImagesHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images/(.*)", ImageHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images/(.*)/action/reactivate", ImageActionReactivateHandler),
    (IMAGE_SERVICE_BASE_URL + r"/v2/images/(.*)/file", ImageFileHandler), 
]
