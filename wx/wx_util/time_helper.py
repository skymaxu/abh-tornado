#!/usr/bin/python
#coding: utf-8

import datetime

def timenow2str():
    """ Get now datetime str. """ 
    d = datetime.datetime.now()
    return d.strftime("%Y-%m-%d %H:%M:%S")
