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

"""Touble with Japanese in the DB.  Testing for a solution."""

# [START import_libraries]
from __future__ import print_function

#from asterisk.agi import *
import re
import ConfigParser
import pprint


from datetime import date, datetime, timedelta
import mysql.connector as mariadb

settings = ConfigParser.RawConfigParser()
settings.read('/etc/asterisk/res_config_mysql.conf')

config = {
  'user': settings.get('general', 'dbuser'),
  'password': settings.get('general', 'dbpass'),
  'host': settings.get('general', 'dbhost'),
  'database': 'kaos_portal_live',
  'raise_on_warnings': True,
}

#settings.get('general', 'dbname'),

def data_insert(query):                           
    try:
        mariadb_connection = mariadb.connect(**config)
        cursor = mariadb_connection.cursor()
        cursor.execute(query)
        record = cursor.lastrowid
        mariadb_connection.commit()
        cursor.close()
        mariadb_connection.close()
    except mariadb.Error as error:
        print("Database Error: {0}".format(error))
    return record

def data_select(query):                           
    try:
        mariadb_connection = mariadb.connect(**config)
        cursor = mariadb_connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        #record = cursor.lastrowid
        #mariadb_connection.commit()
        cursor.close()
        mariadb_connection.close()
    except mariadb.Error as error:
        print("Database Error: {0}".format(error))
    return results

#db_insert = ("INSERT INTO `name` (`did`, `name`, `番号`) VALUES ('0238764234', '日本語', '5')")

#db_insert = ("INSERT INTO `name` (`did`, `name`, `%s`) VALUES ('%s', '%s', '%s')")
#data_insert(db_insert % ('番号', '03-6867-1137', 'カタカナ',  45))

#db_query = ("SELECT * FROM `name`")

db_query = ("SELECT dtmf, dtmf_next FROM `survey_questions_dtmf` WHERE question = 'proj00000520'")


string =  data_select(db_query)
#res = string.encode('utf8', 'replace')

##string.decode('UTF-8')

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(string)

#for x in string:
#    print(x[2].encode('utf8', 'replace'))



#data_insert(db_insert)




