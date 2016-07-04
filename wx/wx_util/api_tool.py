#!/usr/bin/python
#coding: utf-8

import ConfigParser
import datetime
import json
import logging
import os
import time
import traceback
import urllib
import urllib2
import sys  
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')   

from  wx_py3rd import MultipartPostHandler

import singleton
import network_helper

logging.basicConfig(level=logging.INFO, format='<%(levelname)s> %(asctime)s (%(process)d,'
    ' %(thread)d) [%(module)s.%(funcName)s:%(lineno)d] %(message)s')


MAX_RETRY_COUNT = 2

@singleton.singleton
class ApiTool(object):
    def __init__(self, appid, secretkey):
        self.__appid = appid
        self.__secretkey = secretkey
        self.__cp = ConfigParser.SafeConfigParser()
        self.__access_token_file_path = os.path.join(
            os.path.split(os.path.realpath(__file__))[0], 'access_token.ini')
        self.__access_token = self.__get_access_token_from_file()

    def __get_access_token_from_file(self):
        self.__cp.read(self.__access_token_file_path)
        if self.__cp.has_section(self.__appid):
            access_token = self.__cp.get(self.__appid, 'ACCESS_TOKEN')
        else:
            self.__cp.add_section(self.__appid)
            access_token = ''
        return access_token
        
    def __save_access_token_to_file(self):
        self.__cp.set(self.__appid, 'ACCESS_TOKEN', self.__access_token)
        # Write to file
        f = open(self.__access_token_file_path, 'w')
        self.__cp.write(f)
        f.close()

    def __refresh_accesstoken(self):
        logging.info('ENTRANCE: appid:%s, secretkey:%s', self.__appid, self.__secretkey)
        try:
            url = ('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' %
                  (self.__appid, self.__secretkey))
            headers = {'Content-Type':'application/json; encoding=utf-8'}
            resp = network_helper.send_url_request(url=url, headers=headers)
            logging.info(resp)

            # save new access_token
            respdict = json.loads(resp)
            if 'access_token' not in respdict:
                return -2
            self.__access_token = respdict['access_token']
            self.__save_access_token_to_file()
            logging.info('new ACCESS_TOKEN:%s', self.__access_token)
            return 0
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1
                  
    def __handle_errcode(self, respdict):
        # success
        if 'errcode' not in respdict:
            return 0
        if respdict['errcode'] == 0:
            return 0

        # Need to refresh token
        if (respdict['errcode'] == 42001 or 
            respdict['errcode'] == 41001 or 
            respdict['errcode'] == 40001):
            self.__refresh_accesstoken()
            return 1
        else:
            return respdict['errcode']

    def create_menu(self, button_list):			
        logging.info('ENTRANCE: button list:%s', str(button_list))
        create_menu_post_data = {
            'button': button_list
        }
        postdata = json.dumps(create_menu_post_data, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1
			
    def get_menu(self):
        logging.info('ENTRANCE:')
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}

                resp = network_helper.send_url_request(url=url, headers=headers)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return (0, respdict)
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return (ret, {})
        except Exception, e:
            logging.error(traceback.format_exc())
            return (-1, {})
       
    def delete_menu(self):
        logging.info('ENTRANCE:')
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}

                resp = network_helper.send_url_request(url=url, headers=headers)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
        
    def upload_media(self, file_path, media_type):
        logging.info('ENTRANCE: file path:%s, media type:%s', file_path, media_type)
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), 
                    MultipartPostHandler.MultipartPostHandler)
                params = {'media':open(file_path, 'rb')}
                result = opener.open('http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s' % (self.__access_token, media_type), params)
                resp = result.read()
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    if 'media_id' in respdict:
                        return (0, respdict['media_id'])
                    return (0, '')
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return (-1, '')
        
    def get_media(self, media_id):
        logging.info('ENTRANCE: media id:%s', media_id)
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                cookies = urllib2.HTTPCookieProcessor()
                opener = urllib2.build_opener(cookies)
                request = urllib2.Request(
                    url = ('http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % 
                           (self.__access_token, media_id)),
                    headers = {'Content-Type':'application/json; encoding=utf-8'})
                result = opener.open(request)

                # Get real file name.
                if 'Content-Disposition' in result.info():
                    file_name = result.info()['Content-Disposition'].split('filename=')[1]
                    file_name = file_name.replace('"', '').replace("'", "")
                else:
                    # if we were redirected, the real file name we take from the final URL
                    import urlparse
                    file_name = os.path.basename(urlparse.urlsplit(result.url)[2])
                logging.info('file name:%s', file_name)
                resp = result.read()
                if resp.find('errcode') != -1:
                    logging.info(resp)
                    respdict = json.loads(resp)
                    ret = self.__handle_errcode(respdict)
                    if ret == 0:
                        return 0
                    elif ret == 1:
                        count -= 1
                        continue  # access token expired, retry
                    else:
                        return ret
                # Save file.
                f = file(file_name, 'wb')
                f.write(resp)
                f.close()
                return 0
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1

    def get_user_info(self, openid):
        logging.info('ENTRANCE: openid:%s', openid)
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = ('https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s' % 
                       (self.__access_token, openid))
                headers = {'Content-Type':'application/json; encoding=utf-8'}

                resp = network_helper.send_url_request(url=url, headers=headers)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return (0, respdict)
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return (ret, {})
        except Exception, e:
            logging.error(traceback.format_exc())
            return (-1, {})
    
    def get_followers(self):
        logging.info('ENTRANCE:')
        try:
            uinlist = []
            next = ''
            while True:
                count = MAX_RETRY_COUNT
                while count >= 0:
                    url = ('https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % 
                          (self.__access_token, next))
                    headers = {'Content-Type':'application/json; encoding=utf-8'}

                    resp = network_helper.send_url_request(url=url, headers=headers)
                    logging.info(resp)
                    respdict = json.loads(resp)
                    ret = self.__handle_errcode(respdict)
                    if ret == 0:
                        break
                    elif ret == 1:
                        count -= 1
                        continue  # access token expired, retry
                    else:
                        return (ret, [])
                openids = []
                if 'data' in respdict:
                    openids = respdict['data']['openid']
                next = respdict['next_openid']
                uinlist += openids
                # Finish all, break while loop
                if next == '':   
                    break
            return uinlist
        except Exception, e:
            logging.error(traceback.format_exc())
            return (-1, [])
    
    def custom_send_text_msg(self, openid, text):
        logging.info('ENTRANCE: openid:%s, text:%s', openid, text)
        datadict = {
            'touser':openid,
            'msgtype':'text',
            'text':{
                'content': text
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
       
    def custom_send_music_msg(self, openid, title, desc, musicurl, hqmusicurl, thumb_media_id, media_file_path):
        logging.info('ENTRANCE: openid:%s, title:%s, desc:%s, musicurl:%s, hqmusicurl:%s, thumb_media_id:%s, media_file_path:%s', 
            openid, title, desc, musicurl, hqmusicurl, thumb_media_id, media_file_path)
        datadict = {
            'touser':openid,
            'msgtype':'music',
            'music':
            {
                'title':tile,
                'description':desc,
                'musicurl':musicurl,
                'hqmusicurl':hqmusicurl,
                'thumb_media_id':thumb_media_id
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
       
    def custom_send_image_msg(self, openid, media_id):
        logging.info('ENTRANCE: openid:%s, media_id:%s', openid, media_id)
        datadict = {
            'touser':openid,
            'msgtype':'image',
            'image':
            {
                'media_id':media_id
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
        
    def custom_send_voice_msg(self, openid, media_id):
        logging.info('ENTRANCE: openid:%s, media_id:%s', openid, media_id)
        datadict = {
            'touser':openid,
            'msgtype':'voice',
            'voice':
            {
                'media_id':media_id
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
       
    def custom_send_video_msg(self, openid, media_id, title, desc):
        logging.info('ENTRANCE: openid:%s, media_id:%s, title:%s, desc:%s', openid, media_id, title, desc)
        datadict = {
            'touser':openid,
            'msgtype':'video',
            'video':
            {
                'media_id':media_id,
                'title':title,
                'description':desc
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
      
    def custom_send_news_msg(self, openid, news_list):
        logging.info('ENTRANCE: openid:%s, newslist:%s', openid, str(news_list))
        datadict = {
            'touser':openid,
            'msgtype':'news',
            'news':{
                'articles':news_list
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
       
    def template_send_msg(self, openid, template_id, contentdict):
        logging.info('ENTRANCE: openid:%s, template_id:%s, content:%s', openid, template_id, str(contentdict))
        datadict = {
            'touser':openid,
            'template_id':template_id,
            'data':contentdict
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
           
    def active_send_news_msg(self, openid, news_list):
        logging.info('ENTRANCE: openid:%s, news list:%s', openid, str(news_list))
        datadict = {
            'touser':openid,
            'msgtype':'news',
            'news':{
                'articles':news_list 
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/message/send?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    return 0
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return ret
        except Exception, e:
            logging.error(traceback.format_exc())
            return -1	
        
    def create_qrcode(self, sceneid):
        logging.info('ENTRANCE: sceneid:%s', sceneid)
        datadict = {
            'expire_seconds':1800,
            'action_name':'QR_SCENE',
            'action_info':
            {
                'scene':
                {
                    'scene_id':sceneid
                }
            }
        }
        postdata = json.dumps(datadict, ensure_ascii=False).encode('utf-8')  # encode utf-8 manually
        try:
            count = MAX_RETRY_COUNT
            while count >= 0:
                url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=' + self.__access_token
                headers = {'Content-Type':'application/json; encoding=utf-8'}
                post = postdata

                resp = network_helper.send_url_request(url=url, headers=headers, post=post)
                logging.info(resp)
                respdict = json.loads(resp)
                ret = self.__handle_errcode(respdict)
                if ret == 0:
                    if 'ticket' in respdict:
                        return (0, respdict['ticket'])
                    else:
                        return (0, '')
                elif ret == 1:
                    count -= 1
                    continue  # access token expired, retry
                else:
                    return (ret, '')
        except Exception, e:
            logging.error(traceback.format_exc())
            return (-1, '')
    
    def show_qrcode(self, ticket):
        logging.info('ENTRANCE: ticket:%s', ticket)
        new_ticket = urllib.quote(ticket)   # Note: encode ticket here, or will sometimes failed
        logging.info('urlencode ticket: %s', new_ticket)
        try:
            url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + new_ticket

            resp = network_helper.send_url_request(url=url)
            return resp
        except Exception, e:
            logging.error(traceback.format_exc())
            return None

        
        
def main():
    """For test only."""
    HELP = '''
    [1] Create menu
    [2] Get menu
    [3] Delete menu
    [4] Get user info
    [5] Upload media and get media file
    [7] Get followers list
    [8] Custom send text message
    [9] Custom send image message
    [10] Custom send news message
    [11] Send template message
    [12] Active send news message
    [13] Create qrcode and show qrcode
    [-1] Bye!
    '''

    # booksearch
    APPID = 'wx39264df2ba256ed5'
    SECRETKEY = 'c9ac985968682e36d1a33befb28e64b8'
    
    tool = ApiTool(APPID, SECRETKEY)

    print HELP
    while True:
        opt = raw_input()
        if opt == '-1':
            print 'Bye!'
            break
        elif opt == '1':
            button_list = [
                {	
                    "type":"click",
                    "name":"今日歌曲",
                    "key":"V1001_TODAY_MUSIC"
                },
                {
                    "name":"菜单",
                    "sub_button":[
                    {	
                        "type":"view",
                        "name":"搜索",
                        "url":"http://www.soso.com/"
                    }]
                }
            ]
            tool.create_menu(button_list)
        elif opt == '2':
            menu = tool.get_menu()
        elif opt == '3':
            tool.delete_menu()
        elif opt == '4':
            openid = 'o5GO1jj8MRYEz7dU3PHWb3a-x1sg'
            userinfo = tool.get_user_info(openid)
        elif opt == '5':
            media_type = 'image'
            file_path = 'test.jpg'
            ret, media_id = tool.upload_media(file_path, media_type)
            if ret == 0:
                tool.get_media(media_id)
        elif opt == '7':
            follower_list = tool.get_followers()
        elif opt == '8':
            openid = 'o5GO1jj8MRYEz7dU3PHWb3a-x1sg'
            text = 'ping'
            tool.custom_send_text_msg(openid, text)
        elif opt == '9':
            openid = 'o5GO1jj8MRYEz7dU3PHWb3a-x1sg'
            media_id = 'qYJYt6WcOquTqlLOSH0ZTlgRMkuL6KJL7RTtiNo2XqBQcdbRaOLHq7jX3MtczsO6'
            tool.custom_send_image_msg(openid, media_id)
        elif opt == '10':
            openid = 'o5GO1jj8MRYEz7dU3PHWb3a-x1sg'
            newslist = [
                {
                    "title":"Happy Day",
                    "description":"Is Really A Happy Day",
                    "url":"http://www.soso.com",
                    "picurl":"http://www.soso.com/soso/images/logo_index.png"
                },
                {
                    "title":"Happy Day",
                    "description":"Is Really A Happy Day",
                    "url":"http://www.soso.com",
                    "picurl":"http://www.soso.com/soso/images/logo_index.png"
                }
            ]
            tool.custom_send_news_msg(openid, newslist)
        elif opt == '11':
            openid = 'o5GO1jj8MRYEz7dU3PHWb3a-x1sg'
            template_id = 'aygtGTLdrjHJP7Bu4EdkptNfYaeFKi98ygn2kitCJ6fAfdmN88naVvX6V5uIV5x0'
            contentdict = {
                "Goods": "Apple",
                "Unit_price": "$ 20.13",
                "Quantity": "5",
                "Total": "$ 100.65",
                "Source": {
                    "Shop": "Fruit shop",
                    "Recommend": "5 stars"
                }
            }
            tool.template_send_msg(openid, template_id, contentdict)
        elif opt == '12':
            openid = 'o5GO1jj8MRYEz7dU3PHWb3a-x1sg'
            newslist = [
                {
                    "title":"Happy Day",
                    "description":"Is Really A Happy Day",
                    "url":"http://www.soso.com",
                    "picurl":"http://www.soso.com/soso/images/logo_index.png"
                },
                {
                    "title":"Happy Day",
                    "description":"Is Really A Happy Day",
                    "url":"http://www.soso.com",
                    "picurl":"http://www.soso.com/soso/images/logo_index.png"
                }
            ]
            tool.active_send_news_msg(openid, newslist)
        elif opt == '13':
            sceneid = '12345'
            ret, ticket = tool.create_qrcode(sceneid)
            if ret == 0:
                imgdata = tool.show_qrcode(ticket)
        else:
            print 'invalid option' 
            print HELP 



if __name__ == '__main__':
    main()


