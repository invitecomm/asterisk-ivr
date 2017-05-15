#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# Copyright 2016 INVITE Communications Co., Ltd. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""General Database Interaction with Survey Data"""

from __future__ import print_function

import ConfigParser
import sys
import random
import ivr.connection
from asterisk.agi import *
from distutils.util import strtobool

import time


reload(sys)
sys.setdefaultencoding("utf-8")

from datetime import date, datetime, timedelta
import mysql.connector as mariadb

config = ivr.connection.config('general')
#results = ivr.connection.config('survey')

print(config)

def database(query, *vars):                           
    try:
        mariadb_connection = mariadb.connect(**config)
        cursor = mariadb_connection.cursor(dictionary=True, buffered=True)
        #cursor = mariadb_connection.cursor(dictionary=True)
        #cursor = mariadb_connection.cursor(named_tuple=True)        
        
        cursor.execute('SELECT NOW()')
        print(cursor.fetchall())
        time.sleep(2) 
        cursor.execute('SELECT NOW()')
        print(cursor.fetchall())
        
        cursor.execute(query, (list(vars)))
        data = cursor.fetchall()
        #data = dict(zip(cursor.column_names, cursor.fetchone()))
        mariadb_connection.close()
    except mariadb.Error as error:
        print("MySQL Connector/Python: {0}".format(mariadb.__version__))
        print("Database Error: {0}".format(error))
        data = ''
    return data

project = 'R170200001000'

#project_select = ('SELECT * FROM survey_details WHERE project = %s')
project_select = ('SELECT * FROM survey_details')
    

#results = database(query, (lcc))
results = database('SELECT NOW()')

#for row in results:
#    if row['last_name'] == 'LaVallee':
#        print("{last_name}: {password}".format(**row))


        
      
#find_index(results, 'response_tracking_question', 8)
#print(df.loc[project])
#print(results['hangup_id'])
#print(mariadb.__version__)


















