import tornado.web
import json

class HttpBaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(HttpBaseHandler, self).__init__(application, request, **kwargs)
        access_domain = ['http://115.28.143.67:8791', 'http://115.28.143.67:8989', 'http://115.28.143.67:8990',
                         'http://115.28.143.67:8991', 'http://www.immbear.com']
        if 'Origin' in self.request.headers:
            self.add_header("Access-Control-Allow-Origin", self.request.headers['Origin'])
        elif 'Host' in self.request.headers:
            self.add_header("Access-Control-Allow-Origin", self.request.headers['Host'])
        self.add_header("Access-Control-Allow-Credentials", 'true')
        self.add_header("Access-Control-Allow-Methods", 'GET,POST,OPTIONS,PUT,DELETE')
        self.add_header("Access-Control-Allow-Headers",
                        'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')
        self.add_header('Connection', 'keep-alive')
        self.arg = None

    def options(self, *args, **kwargs):
        pass

    def get_current_user(self):
        id = self.get_secure_cookie("id")
        return id

    def send_json(self, resp):
        self.set_header("content-type":"application/json")
        self.write(json.dumps(resp))
