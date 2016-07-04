#!/usr/bin/python
#coding: utf-8

import binascii
import datetime
import httplib 
import json
import logging
import pyDes
import random
import re
import time
import traceback
import urllib 
import network_helper


class PassportService(object):
    def __init__(self, appkey, sysid):  
        """ Initial appkey and sysid which applied from http://tof.oa.com/. """
        self.__appkey = appkey
        self.__sysid = sysid 

    def __desencrypt(self, data, key):
        """ DES encrypt algorithm, to generate signature. """
        ph = '--------'
        key = (key + ph)[:8]  # 8 digits
        des = pyDes.des(key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5)
        d = des.encrypt(data)
        return binascii.hexlify(d)

    def __make_http_header(self):
        """ Make http header of DecryptTicketWithClientIP API request. """
        r = random.randint(1000, 9999)
        timestamp = int(time.time())
        timestamp = str(timestamp)[:10]  # max 10 digits
        data = 'random' + str(r) + 'timestamp' + str(timestamp);
        signature = self.__desencrypt(data, str(self.__sysid))

        header = {}
        header['Content-Type'] = 'application/json;charset=utf-8'

        header['appkey']    = str(self.__appkey)
        header['random']    = str(r)
        header['timestamp'] = str(timestamp)
        header['signature'] = str(signature).upper()
        return header

    def __decrypt_ticket_with_client_ip(self, ticket, browseip):  
        """ Call tof WebApi to decrypt ticket. """
        try:  
            request_url = 'http://api.tof.oa.com/api/v1/Passport/DecryptTicketWithClientIP?appkey=%s&encryptedTicket=%s&browseIP=%s' % (urllib.quote(self.__appkey), urllib.quote(ticket), urllib.quote(browseip))
            header = self.__make_http_header()
            logging.info(str(header))

            ret, data = network_helper.send_url_request(request_url, None, header)
            if ret != 0:
                logging.error('Send url request failed!')

            adict = json.loads(data)
            if adict['Ret'] != 0:
                logging.error('API request failed! Ret:%d, ErrCode:%d, ErrMsg:%s', adict['Ret'], adict['ErrCode'], adict['ErrMsg'])
                return None
            return adict['Data']
        except Exception, e:  
            logging.error(traceback.format_exc())
            return None

    def __str2datetime(self, strtime):
        """ Change datetime str from API response to datetime object. """
        mo = re.match('^(....)-(..)-(..)T(..):(..):(..).*$', strtime)
        if mo:
            g       = mo.groups()
            year    = int(g[0])
            mon     = int(g[1])
            day     = int(g[2])
            hour    = int(g[3])
            min     = int(g[4])
            sec     = int(g[5])
            t = datetime.datetime(year, mon, day, hour, min, sec)
            return t    

    def __has_expired(self, expirationStr):
        """ Whether this ticket is expired. """
        t = datetime.datetime.now()
        expiration = self.__str2datetime(expirationStr)
        if expiration and t < expiration:
            return False
        return True

    def authenticate_with_ticket(self, ticket, browseip):  
        """ 
        Authenticate with ticket.
        If success return username, else return None.
        """
        result = self.__decrypt_ticket_with_client_ip(ticket, browseip)
        if result is None:
            return None

        userid     = result['StaffId']
        username   = result['LoginName']
        expiration = result['Expiration']
        # Whether this ticket is expired.
        if self.__has_expired(expiration):
            return None
        # Return username
        return username

if __name__ == '__main__':
    # example
    APPKEY = 'cef1ff585e1d4b4db51da30be5dd46ae'
    SYSID = '22414'
    BROWSEIP = '10.6.208.239'
    TICKET = '7B8ABA8CD9F6C0FFCC82130A29BAB617719B57C6F9E21842E669AEBED1B841A0675F2D0217FC15A13F603BFC6F2233EE53CB33FDC8F68222B3226EE9D16D811B8350A478A210E98AD80BE41F341A571201B2BA9178301AB426A6D24B5C6634232E397755930C4201B6F5E81C56E0446A81010928A854B05BDC23E1FE6356A0893B96DFBE621C469545240929893BBAC45ACDDF4C7632C3F0F07A7311620AD2EE5CF9EAF39AF7FC4A08BC1675DA29330C7F648D8C99941AEF'

    auth = PassportService(APPKEY, SYSID)
    result = auth.authenticate_with_ticket(TICKET, BROWSEIP)
    print str(result)

