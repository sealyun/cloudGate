from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler

class ImageBaseHandler(HttpBaseHandler):   
    #TODO add init processor
    pass
    
    def get(self):
        pass

class ImagesHandler(ImageBaseHandler):
    def get(self):
        pass

    def post(self):
        pass

class ImageHandler(ImageBaseHandler):
    def get(self, image_id):
        pass

    def patch(self, image_id):
        pass

    def delete(self, image_id):
        pass

class ImageActionReactivateHandler(ImageBaseHandler):
    def post(self, image_id):
        pass

class ImageFileHandler(ImageBaseHandler):
    def put(self, image_id):
        pass

    def get(self, image_id):
        pass

