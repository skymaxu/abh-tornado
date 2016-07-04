#!/usr/bin/python
#coding: utf-8

import datetime
import hashlib
import json 
import os
import time
import sys

from ..wx_business import retcode
from ..wx_util.log_helper import wx_log
from ..wx_model import user_model


def view_user(id):
    """"""
    wx_log.info("ENTRANCE id: %d", id)
    
    result = user_model.UserModel().get_one(id)    
    if result is None:        
        ret = retcode.USER_ID_NOT_EXIST        
        data = {}        
        wx_log.error("player not exist:%d", id)        
        return (ret, data)

    ret = 0
    data = result

    wx_log.info("RETURN ret:%s, data:%s", ret, str(data))
    return (ret, data)
    

