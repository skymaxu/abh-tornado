#!/usr/bin/python
#coding: utf-8

import time
import xml.etree.ElementTree as ET


def _none2str(text):
    """Convert None to ''. """
    if text == None:
        return ''
    return text

def get_value_by_key(msg, key):
    """Get value by key, if key doesn't exist, return ''. """
    if key in msg:
        return _none2str(msg[key]).encode('utf-8')
    else:
        return ''
    
def parse_input_msg(inputstr):
    """Parse xml input data to a dict. """
    root = ET.fromstring(inputstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def reply_text_msg(tousername, fromusername, content):
    TEXT_MSG_TMPL = (
        "<xml>\n"
        "<ToUserName><![CDATA[%s]]></ToUserName>\n"
        "<FromUserName><![CDATA[%s]]></FromUserName>\n"
        "<CreateTime>%s</CreateTime>\n"
        "<MsgType><![CDATA[text]]></MsgType>\n"
        "<Content><![CDATA[%s]]></Content>\n"
        "</xml>"
    )

    xmloutput = TEXT_MSG_TMPL % (tousername, fromusername, int(time.time()), content)
    return xmloutput

def reply_image_msg(tousername, fromusername, media_id):
    IMAGE_MSG_TMPL = (
        "<xml>\n"
        "<ToUserName><![CDATA[%s]]></ToUserName>\n"
        "<FromUserName><![CDATA[%s]]></FromUserName>\n"
        "<CreateTime>%s</CreateTime>\n"
        "<MsgType><![CDATA[image]]></MsgType>\n"
        "<Image>\n"
        "<MediaId><![CDATA[%s]]></MediaId>\n"
        "</Image>\n"
        "</xml>"
    )

    xmloutput = IMAGE_MSG_TMPL % (tousername, fromusername, int(time.time()), media_id)
    return xmloutput

def reply_voice_msg(tousername, fromusername, media_id):
    VOICE_MSG_TMPL = (
        "<xml>\n"
        "<ToUserName><![CDATA[%s]]></ToUserName>\n"
        "<FromUserName><![CDATA[%s]]></FromUserName>\n"
        "<CreateTime>%s</CreateTime>\n"
        "<MsgType><![CDATA[voice]]></MsgType>\n"
        "<Voice>\n"
        "<MediaId><![CDATA[%s]]></MediaId>\n"
        "</Voice>\n"
        "</xml>"
    )

    xmloutput = VOICE_MSG_TMPL % (tousername, fromusername, int(time.time()), media_id)
    return xmloutput

def reply_video_msg(tousername, fromusername, media_id, title, desc):
    VIDEO_MSG_TMPL = (
        "<xml>\n"
        "<ToUserName><![CDATA[%s]]></ToUserName>\n"
        "<FromUserName><![CDATA[%s]]></FromUserName>\n"
        "<CreateTime>%s</CreateTime>\n"
        "<MsgType><![CDATA[video]]></MsgType>\n"
        "<Video>\n"
        "<MediaId><![CDATA[%s]]></MediaId>\n"
        "<Title><![CDATA[%s]]></Title>\n"
        "<Description><![CDATA[%s]]></Description>\n"
        "</Video>\n"
        "</xml>"
    )

    xmloutput = VIDEO_MSG_TMPL % (tousername, fromusername, int(time.time()), media_id, title, desc)
    return xmloutput

def reply_music_msg(tousername, fromusername, title, desc, musicurl, hqmusicurl, thumbmediaid):
    MUSIC_MSG_TMPL = (
        "<xml>\n"
        "<ToUserName><![CDATA[%s]]></ToUserName>\n"
        "<FromUserName><![CDATA[%s]]></FromUserName>\n"
        "<CreateTime>%s</CreateTime>\n"
        "<MsgType><![CDATA[music]]></MsgType>\n"
        "<Music>\n"
        "<Title><![CDATA[%s]]></Title>\n"
        "<Description><![CDATA[%s]]></Description>\n"
        "<MusicUrl><![CDATA[%s]]></MusicUrl>\n"
        "<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>\n"
        "<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>\n"
        "</Music>\n"
        "</xml>"
    )

    xmloutput = MUSIC_MSG_TMPL % (tousername, fromusername, int(time.time()), title, desc, musicurl, hqmusicurl, thumbmediaid)
    return xmloutput

def reply_news_msg(tousername, fromusername, news_list):
    NEWS_MSG_TMPL = (
        "<xml>\n"
        "<ToUserName><![CDATA[%s]]></ToUserName>\n"
        "<FromUserName><![CDATA[%s]]></FromUserName>\n"
        "<CreateTime>%s</CreateTime>\n"
        "<MsgType><![CDATA[news]]></MsgType>\n"
        "<ArticleCount>%s</ArticleCount>\n"
        "<Articles>\n"
        "%s\n"
        "</Articles>\n"
        "</xml>"
    )
    NEWS_MSG_INNER_TMPL = (
        "<item>\n"
        "<Title><![CDATA[%s]]></Title>\n" 
        "<Description><![CDATA[%s]]></Description>\n"
        "<PicUrl><![CDATA[%s]]></PicUrl>\n"
        "<Url><![CDATA[%s]]></Url>\n"
        "</item>\n"
    )

    if not news_list:
        return None

    innerstr = ''
    for news in news_list:
        innerstr += NEWS_MSG_INNER_TMPL % (news['title'], news['description'], news['picurl'], news['url'])
    
    xmloutput = NEWS_MSG_TMPL % (tousername, fromusername, int(time.time()), len(news_list), innerstr)
    return xmloutput

