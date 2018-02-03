#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# Copyright 2016-2018 INVITE Communications Co., Ltd. All Rights Reserved.
# Copyright 2018 Sergei Turukin All Rights Reserved.
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

"""AGI hangup script that updates WombatDialer variables in the DB."""

# [START import_libraries]
from __future__ import print_function

import ConfigParser
import logging
import logging.handlers
import re
import time
from datetime import date, datetime, timedelta

import mysql.connector as mariadb
import retry
from asterisk.agi import *


# Setup logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

settings = ConfigParser.RawConfigParser()
settings.read('/etc/asterisk/res_config_mysql.conf')

config = {
  'user': settings.get('general', 'dbuser'),
  'password': settings.get('general', 'dbpass'),
  'host': settings.get('general', 'dbhost'),
  'database': 'survey',
  'raise_on_warnings': True,
}

#  'database': settings.get('general', 'dbname'),

def verbose(statement):
    agi.verbose(statement)
    log.info(statement)


@retry.retry(tries=3, delay=5)
def data_insert(queries):
    try:
        conn = mariadb.connect(**config)
        cursor = conn.cursor()
        for query in queries:
            #verbose(query)
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except (mariadb.OperationalError) as error:
        verbose("Database Error: {0}".format(error))
        for query in queries:
            verbose(query)
        # initiate retry
        raise
    except mariadb.Error as error:
        verbose("Database Error: {0}".format(error))
        for query in queries:
            verbose(query)
        raise

#db_update = ("UPDATE `%s` SET `%s` = '%s' WHERE id = '%s'")
new_update = ("UPDATE `{0}` SET `{1}` = '{2}' WHERE id = {3}")
"""
Update a specific value in a table.
"""

new_count = ("UPDATE `{0}` SET `{1}` = `{1}` + {2} WHERE id = {3}")
"""
Math increment of a INT value in a table.
"""

agi = AGI()
    
if(agi.get_variable('WOMBAT_HOPPER_ID')):    

    dispo = agi.get_variable('CDR(disposition)')
    billsec = agi.get_variable('CDR(billsec)')
    newTable = agi.get_variable('table')
    warlist = agi.get_variable('warlist')

    data_insert([
        new_count.format(newTable,'billsec',billsec,warlist),
        new_update.format(newTable,'disposition',dispo,warlist)])
