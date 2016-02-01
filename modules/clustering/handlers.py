from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler

class Test(HttpBaseHandler):   
    pass

class Client(Test):
    def get(self):
        pass

    @coroutine
    def post(self):
        pass

