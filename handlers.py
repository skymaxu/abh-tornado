__author__ = 'skymaxu'

import os
from views import *
import wx.wx_handlers

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
HANDLERS = []
# (r'/(.+)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static')}),
HANDLERS += [(r'/', IndexHandler),
             (r'/index', IndexHandler),
             (r'/products',ProductsHandler),
             (r'/services',ServicesHandler),
             (r'/contact',ContactHandler)
             ]

# add other model handlers
HANDLERS += wx.wx_handlers.HANDLERS
print HANDLERS
