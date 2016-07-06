# coding:utf-8
__author__ = 'skymaxu'

import tornado.web
import tornado.gen
import traceback
from util.log_helper import MyLogger
class BaseHandler(tornado.web.RequestHandler):
    #db init
    @property
    def db(self):
        return self.application.db
    #log init
    @property
    def write_log(self):
        return MyLogger('mainlog').getlogger()


    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            # MyLogger().getlogger().error(traceback.format_exc())
            # in debug mode, try to send a traceback
            if self.settings.get('debug'):
                for line in traceback.format_exception(*kwargs['exc_info']):
                    self.write(line + '<br />')
            self.finish()
        else:
            self.finish('Bad guy!!!!')

    def get_one_poem(self, name):
        if self.db is None:
            return
        return self.db.get('select * from author where name=%s', str(name))


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write_log.error('this is test log file .....')
        self.write_log.critical('Ileggal intrution!')
        return self.render('index.html')

class ProductsHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('products.html')

class ServicesHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('services.html')

class ContactHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('contact.html')
class InitHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('base\init.html')
