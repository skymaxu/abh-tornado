#!/usr/bin/python
#coding: utf-8

import datetime
import json
import os
import types
import traceback
import sys
import time
from util import singleton
from views import BaseHandler
from ..wx_util import time_helper


@singleton.singleton
class UserModel(BaseHandler):
    """Model class. """

    __table_name = 'user'
    __table_fields = ['id', 'nickname', 'headimg', 'create_time']
    
    def __init__(self):
        """ Init db handler. """
        pass

    def get_one(self, id):
        """ Get one record. """
        query = 'SELECT * FROM user WHERE id=%s'
        result = self._db.get(query, id)
        if result and 'create_time' in result:
            result['create_time'] = time.mktime(result['create_time'].timetuple())        
        return result

    def add_one(self, id, nickname, headimg):
        """ Add one record. """
        query = 'INSERT INTO user VALUES (%s, %s, %s, %s)'
        rowId = self._db.execute_lastrowid(query, None, nickname, headimg, time_helper.timenow2str())
        return rowId

    def update_one(self, id, nickname, headimg, create_time):
        """ Update one record. """
        query = 'UPDATE user SET nickname=%s, headimg=%s, create_time=%s WHERE id=%s'
        rowCount = self._db.execute_rowcount(query, nickname, headimg, create_time, id)
        return rowCount

    def del_one(self, id):
        """ Delete one record. """
        query = 'DELETE FROM user WHERE id=%s'
        result = self._db.execute_rowcount(query, id)
        return result

    def get_all(self):
        """ Get all records. """
        query = 'SELECT * FROM user'
        result = self._db.query(query)
        if result:            
		    for it in result:                
			    if 'create_time' in it:                    
				    it['create_time'] = time.mktime(it['create_time'].timetuple())
        return result

    def get_count(self):
        """ Get records count. """
        query = 'SELECT COUNT(*) FROM user'
        result = self._db.query(query)
        return result

