# coding:UTF-8

import os.path
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import tornado.web
import tornado.log

from config import PORT

sys.path.append(os.path.abspath(".."))

from url import *

define("port", default=PORT, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = URL_SETTINGS

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates/"),
            static_path=os.path.join(os.path.dirname(__file__), "static/"),
            debug=True,
            cookie_secret="13skss9845fui2345hsz846fdah848",
            login_url="/login",)
        
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
