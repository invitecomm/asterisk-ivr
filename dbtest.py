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

"""AGI script that renders speech to text using Google Cloud Speech API
 using the REST API."""

# [START import_libraries]
from __future__ import print_function

from asterisk.agi import *
import re
import ConfigParser


from datetime import date, datetime, timedelta
import mysql.connector


def question(file, valid_digits):
    regexp = re.compile(r'[' + valid_digits + ']')
    
    res = agi.get_data(file, 20000, 1)
    
    if regexp.search(res) is not None:
        return res

    res = agi.get_data(file, 20000, 1)
    
    if regexp.search(res) is not None:
        return res
    if not res:
        agi.hangup()


settings = ConfigParser.RawConfigParser()
settings.read('/etc/asterisk/res_config_mysql.conf')

config = {
  #'user': settings.get('general', 'dbuser'),
  'user': 'needfullthings',
  'password': settings.get('general', 'dbpass'),
  'host': settings.get('general', 'dbhost'),
  'database': settings.get('general', 'dbname'),
  'raise_on_warnings': True,
}

def data_insert(clid, text, digit):

    add_wardial = ("INSERT INTO wardial (text, %s) VALUES (%s, %s)")
    data_wardial = (text, clid, digit)                               
    print(add_wardial % data_wardial)
    try:
        cnx = mysql.connector.connect(user='scott', database='employees')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FORM employees")   # Syntax error in query
        cnx.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

data_insert('this is text','q1','7')



#agi = AGI()
#agi.answer()

#clid = agi.env['agi_callerid']
#print(clid)

#data_insert(agi.env['agi_callerid'],agi.env['agi_extension'])

#agi.stream_file('wardial/greeting')

#q1 = question('wardial/question1', '12')
#data_insert(clid,'q1',q1)

#q2 = question('wardial/question2', '123')
#data_insert(clid,'q2',q2)

#q3 = question('wardial/question3', '12345')
#q4 = question('wardial/question4', '123')
#q5 = question('wardial/question5', '123')

#agi.stream_file('wardial/goodby')
#agi.hangup()

