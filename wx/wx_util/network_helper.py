#!/usr/bin/python
#coding: utf-8

import logging
import traceback
import urllib
import urllib2

def send_url_request(url, headers=None, post=None, timeout=None):
    """Send http request.
    
    If `post` is None, it's a GET request, else a POST request.
    You may set `headers` and `timeout` of this request.
    You should catch exceptions at the caller.
    """
    logging.info("url:%s, post data:%s", url, str(post))
    # Set default timeout.
    if timeout is None:
        timeout = 5
    
    # Set default headers.
    if headers is None:
        headers = {'Content-Type':'text/plain', 'srcarset':'UTF-8'}

    # Send request.
    request = urllib2.Request(
        url = url,
        headers = headers,
        data = post
    )
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    result = opener.open(request, timeout=timeout)
    data = result.read()

    logging.info(data)
    return data

