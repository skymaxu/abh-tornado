#!/usr/bin/python
#coding: utf-8

import datetime
import json
import os
import sys
import hashlib
import time

from ..wx_business import words
from ..wx_util import msg_helper
from ..wx_util.log_helper import wx_log



def check_signature(signature, timestamp, nonce, token):
    """Check whether the HTTP request is from WeChat by verifying the signature. """
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = "%s%s%s" % tuple(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    if hashstr == signature:
        return True
    else:
        return False

def process_msg(msg):
    """Dispatch msg to handlers."""
    outputmsg = ''
    msgtype = msg_helper.get_value_by_key(msg, 'MsgType')
    tousername = msg_helper.get_value_by_key(msg, 'ToUserName')
    fromusername = msg_helper.get_value_by_key(msg, 'FromUserName')

    # Msg handling.
    if msgtype == 'event':
        event = msg_helper.get_value_by_key(msg, 'Event')
        if event.lower() == 'subscribe':
            return handle_subscribe(msg)
        elif event.lower() == 'unsubscribe':
            return handle_unsubscribe(msg)
        elif event.lower() == 'click':
            eventkey = msg_helper.get_value_by_key(msg, 'EventKey')
            if eventkey == 'V1001_MY_PROFILE':
                pass   # do something
            else:
                wx_log.error('unknown eventkey:%s', eventkey)
        else:
            wx_log.error('unknown event:%s', event)
    elif msgtype == 'text':
        content = msg_helper.get_value_by_key(msg, 'Content')
        content = content.strip() # trim space
        # help 
        if content.lower() == 'h' or content.lower() == 'help':
            return msg_helper.reply_text_msg(fromusername, tousername, words.WORDS_HELP)
        else:
            return msg_helper.reply_text_msg(fromusername, tousername, words.WORDS_HELP)
    else:            
        return None

def handle_subscribe(msg):
    """Handle subscribe event. """
    tousername = msg_helper.get_value_by_key(msg, 'ToUserName')
    fromusername = msg_helper.get_value_by_key(msg, 'FromUserName')
    # Record into log
    wx_log.info('new subscriber:' + fromusername)
    # Reply welcome msg
    return msg_helper.reply_text_msg(fromusername, tousername, words.WORDS_WELCOME)

def handle_unsubscribe(msg):
    """Handle unsubscribe event. """
    fromusername = msg_helper.get_value_by_key(msg, 'FromUserName')
    wx_log.info('unsubscribe:' + fromusername)
    
