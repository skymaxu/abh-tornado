#!/usr/bin/python
#coding: utf-8

import json
import os
import sys
import time
import traceback

import tornado.ioloop
import tornado.options
import tornado.web
from views import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        return  self.render('wx/index.html')

# class LoginHandler(BaseHandler):
#     def get(self):
#         self.set_secure_cookie('user', 'xxxxxxxx')
#         resp = {}
#         resp['ret'] = retcode.OK
#         resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
#         jsonstr = json.dumps(resp)
#         self.set_header('Content-Type', 'application/json')
#         self.write(jsonstr)
#
# class LogoutHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         self.clear_cookie('user')
#         ret = 0
#         resp = {}
#         resp['ret'] = ret
#         resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
#         jsonstr = json.dumps(resp)
#         self.set_header('Content-Type', 'application/json')
#         self.write(jsonstr)
#
# class InterfaceMainHandler(BaseHandler):
#     def get(self):
#         self.write_log.critical('Ileggal intrution!')
#         if ('signature' not in self.request.arguments or
#            'timestamp' not in self.request.arguments or
#            'nonce' not in self.request.arguments or
#            'echostr' not in self.request.arguments):
#             return
#
#         # check signature
#         signature = self.get_argument('signature')
#         timestamp = self.get_argument('timestamp')
#         nonce = self.get_argument('nonce')
#         echostr = self.get_argument('echostr')
#         if not interface_logic.check_signature(signature, timestamp, nonce, config.OA_TOKEN):
#             self.write_log.critical('Ileggal intrution!')
#             return
#
#         self.write(echostr)
#
#     def post(self):
#         if ('signature' not in self.request.arguments or
#            'timestamp' not in self.request.arguments or
#            'nonce' not in self.request.arguments):
#             return
#
#         # check signature
#         signature = self.get_argument('signature')
#         timestamp = self.get_argument('timestamp')
#         nonce = self.get_argument('nonce')
#         if not interface_logic.check_signature(signature, timestamp, nonce, config.OA_TOKEN):
#             self.write_log.critical('Ileggal intrution!')
#             return
#
#         # parse msg
#         msg = self.request.body
#         self.write_log.info('Recv msg: ' + msg)
#         msgdict = msg_helper.parse_input_msg(msg)
#
#         # check if send to the right oa
#         to_user_name = msg_helper.get_value_by_key(msgdict, 'ToUserName')
#         if to_user_name != config.OA_USERNAME:
#             self.write_log.critical('Send to the wrong official account!')
#             return
#
#         # process msg
#         reply_msg = interface_logic.process_msg(msgdict)
#         if reply_msg != None:
#             self.write_log.info('Reply msg: ' + reply_msg)
#             self.write(reply_msg)
#             return
#
# class UserViewHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         if ('id' not in self.request.arguments):
#             resp = {}
#             resp['ret'] = retcode.MISS_ARGUMENT
#             resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
#             jsonstr = json.dumps(resp)
#             self.set_header('Content-Type', 'application/json')
#             self.write(jsonstr)
#             return
#
#         id = int(self.get_argument('id'))
#
#         if (id < 0):
#             resp = {}
#             resp['ret'] = retcode.INVALID_ARGUMENT_VALUE
#             resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
#             jsonstr = json.dumps(resp)
#             self.set_header('Content-Type', 'application/json')
#             self.write(jsonstr)
#             return
#
#         ret, data = admin_logic.view_user(id)
#
#         resp = {}
#         resp['ret'] = ret
#         resp['ret_msg'] = retcode.get_ret_msg(resp['ret'])
#         resp['data'] = data
#         jsonstr = json.dumps(resp)
#         self.set_header('Content-Type', 'application/json')
#         self.write(jsonstr)


class WxHandler(BaseHandler):
    def parse_request_xml(self, rootElem):
        msg = {}
        if rootElem.tag == 'xml':
            for child in rootElem:
                msg[child.tag] = child.text  # 获得内容
        return msg

    def get(self):
        # 获取输入参数
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echostr = self.get_argument('echostr', '')
        # 自己的token
        token = "abhweixin"  # 这里改写你在微信公众平台里输入的token
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法
        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            self.write(echostr)

    def post(self):
        rawstr = self.request.body
        msg = self.parse_request_xml(ET.fromstring(rawstr))
        MsgType = tornado.escape.utf8(msg.get("MsgType"))
        Content = tornado.escape.utf8(msg.get("Content"))
        FromUserName = tornado.escape.utf8(msg.get("FromUserName"))
        CreateTime = tornado.escape.utf8(msg.get("CreateTime"))
        ToUserName = tornado.escape.utf8(msg.get("ToUserName"))
        if MsgType != "text":
            Content = "Sorry，亲，你的style我不懂！"
        if not Content:
            Content = "感谢您关注爱博华科技有限公司！我们拥有专业的技术团队，为您提供专业的项目外包服务！如果您有什么需要，可以随时联系我们，我们竭诚为您服务！"
        data = '''<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
        </xml> ''' % (FromUserName, ToUserName, int(time.time()), 'text', Content)
        self.write(data)  # 提交信息
