import tornado.web
import json
from cloudGate.config import *

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
        self.set_header("content-type","application/json")
        self.write(json.dumps(resp))

    def create_tocken(self, s):
        return s

    def auth(self, s):
        if s == IDENTITY["aliyun"]["user_name"] + IDENTITY["aliyun"]["passwd"]:
            return True
        else:
            return False

    def parse_token(self, token):
        return {
            "name":IDENTITY["aliyun"]["user_name"],
            "password":IDENTITY["aliyun"]["passwd"]
        }
        #return json.loads(token)
