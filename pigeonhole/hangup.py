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
import time
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
  'database': 'wardial',
  'raise_on_warnings': True,
}

#  'database': settings.get('general', 'dbname'),


def data_insert(query):                           
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
    return record

db_insert = ("INSERT INTO `%s` (`id`, `%s`) VALUES ('%s', '%s')")
db_update = ("UPDATE `%s` SET `%s` = '%s' WHERE id = '%s'")
#
# Changed to DID
#

agi = AGI()
#agi.answer()

#clid = agi.env['agi_accountcode']

# Asterisk Dial-plan Application 'DumpChan()'
#Variables:
#WOMBAT_HOPPER_ID=2145573608
#warlist=38418
#NUM=
#SIPCALLID=1583cd9c69daeca70f5a91477e22f3b7@172.17.70.223:5060

#wombat = agi.get_variable('WOMBAT_HOPPER_ID')
dispo = agi.get_variable('CDR(disposition)')
#newTable = agi.get_variable('table')
#warlist = agi.get_variable('warlist')
#warlist = agi.env['agi_accountcode']

#
# Changed to DID
#
agi.verbose("Dispo: {0}".format(dispo))
time.sleep(3)

agi.hangup()

# calltime = agi.get_variable('ANSWEREDTIME')
# data_insert(db_update % ('reply', calltime, warlist))




