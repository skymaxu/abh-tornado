__author__ = 'skymaxu'

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import torndb
import tornado.autoreload
from handlers import HANDLERS, STATIC_PATH, TEMPLATE_PATH
import config
import os

from tornado.options import options, define

define('port', default=9000, help='this run port..', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = HANDLERS

        setting = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            login_url=r'/wx/login',
            xrsf_cookies=False,
            cookie_secret='this is test...',
            debug=True
        )
        print "setting:",setting
        tornado.web.Application.__init__(self, handlers=handlers, **setting)
        if config.MYSQL_ENABLE:
            self.db = torndb.Connection(config.MYSQL_DB_HOST, config.MYSQL_DB_DBNAME, config.MYSQL_DB_USER,
                                        config.MYSQL_DB_PASSWD)
        else:
            self.db = None


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
