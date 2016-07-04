__author__ = 'skymaxu'

import os
from wx_views import *

HANDLERS = []

HANDLERS += [(r'/wx', MainHandler),
             (r'/wx/login', LoginHandler),
             (r'/wx/logout', LogoutHandler),
             (r'/wx/interface', InterfaceMainHandler),
             (r'/wx/view', UserViewHandler)]
