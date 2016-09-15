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
import mysql.connector as mariadb


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
  'user': settings.get('general', 'dbuser'),
  'password': settings.get('general', 'dbpass'),
  'host': settings.get('general', 'dbhost'),
  'database': settings.get('general', 'dbname'),
  'raise_on_warnings': True,
}

def data_insert(query):

    #add_wardial = ("INSERT INTO wardial (text, digit, %s) VALUES ('%s', '%s', '%s')")
    #data_wardial = (text, clid, digit, digit)                               
    agi.verbose(query)
    try:
        mariadb_connection = mariadb.connect(**config)
        cursor = mariadb_connection.cursor()
        cursor.execute(query)
        record = cursor.lastrowid
        mariadb_connection.commit()
        cursor.close()
        mariadb_connection.close()
    except mariadb.Error as error:
        agi.verbose("Database Error: {0}".format(error))
    #agi.verbose('completed')
    return record

db_insert = ("INSERT INTO `wardial` (`clid`, `%s`) VALUES ('%s', '%s')")
db_update = ("UPDATE `wardial` SET `%s` = '%s' WHERE `id` = '%s'")

agi = AGI()
agi.answer()

clid = agi.env['agi_accountcode']

wombat = agi.get_variable('PHONE_EXTEN')
#agi.verbose('UserEvent','name','UniqueID:%s','P0:0' % uniqueid)
#agi.appexec('UserEvent', 'ATTRIBUTE, UniqueID:%s,Status:Machine' % uniqueid)

amdstatus = agi.env['agi_arg_2']
amdreason = agi.env['agi_arg_3']

if amdstatus == "MACHINE":
    agi.verbose('NOTHING TO SEE HERE')
    #agi.appexec('UserEvent', 'ATTRIBUTE, UniqueID:%s,Status:Machine' % uniqueid)
    data_insert(db_insert % ('note', clid, '%s:%s' % (amdstatus, amdreason)))
    agi.hangup()

session_id = data_insert(db_insert % ('note', clid, '%s:%s' % (amdstatus, amdreason)))

#wombat = agi.appexec('DumpChan')
#agi.verbose('Wombat ID: %s' % wombat)

agi.stream_file('wardial/greeting')

q1 = question('wardial/question1', '12')
data_insert(db_update % ('q1', q1, session_id))
#agi.verbose('RECORD #%s INSERTED' % session_id)
#agi.verbose('this {0} that {1} and this {0} again'.format('a','b'))

q2 = question('wardial/question2', '123')
data_insert(db_update % ('q2', q2, session_id))

q3 = question('wardial/question3', '12345')
data_insert(db_update % ('q3', q3, session_id))

q4 = question('wardial/question4', '123')
data_insert(db_update % ('q4', q4, session_id))

q5 = question('wardial/question5', '123')
data_insert(db_update % ('q5', q5, session_id))

agi.stream_file('wardial/goodby')
agi.hangup()

