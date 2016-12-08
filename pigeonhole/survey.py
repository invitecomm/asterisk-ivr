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


reload(sys)
sys.setdefaultencoding("utf-8")

from datetime import date, datetime, timedelta
import mysql.connector as mariadb

config = ivr.connection.config('portal')
results = ivr.connection.config('wardial')

def database(query):                           
    try:
        mariadb_connection = mariadb.connect(**config)
        cursor = mariadb_connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        mariadb_connection.close()
    except mariadb.Error as error:
        print("Database Error: {0}".format(error))
    return data

def update(query):                           
    try:
        mariadb_connection = mariadb.connect(**results)
        cursor = mariadb_connection.cursor()
        cursor.execute(query)
        record = cursor.lastrowid
        mariadb_connection.commit()
        cursor.close()
        mariadb_connection.close()
    except mariadb.Error as error:
        print("Database Error: {0}".format(error))
    return record
    
#question_id = 'blue00000041'

survey_questions_dtmf = ('SELECT * FROM survey_questions_dtmf WHERE question = "%s"')

#
#   DTMF Functions
#

"""Get Concatinated List of Valid Digits"""
def digits(question_id):
    db_select = survey_questions_dtmf
    results = database(db_select % (question_id))
    data = ''
    for values in results:
        data += str(values[5])
    return data 
#print (digits(question_id))

"""Get Next Questions Based on Entered DTMF"""
def next_question(question_id, dtmf):
    db_select = ('SELECT dtmf_next FROM survey_questions_dtmf WHERE question = "%s" AND dtmf = "%s"')
    results = database(db_select % (question_id, dtmf))
    data = results[0]
    return ''.join(data)    # Use JOIN to fix UTF8
#print (next_question(question_id, 2))

"""Get Label used by the DB"""
def label_question(question_id):
    db_select = ('SELECT question_label FROM survey_questions WHERE question = "%s"')
    results = database(db_select % (question_id))
    data = results[0]
    return ''.join(data)    # Use JOIN to fix UTF8
#print (next_question(question_id, 2))

"""Get Next Questions Based on Entered DTMF"""
def test(col, val):
    db_select = ('SELECT * FROM name WHERE `%s` = "%s"')
    results = database(db_select % (col, val))
    for values in results:
        foo = str(values[2])    
        print (foo)
#print (test('番号', 45))


#
#   Survey Start
#

"""

sighup.handle()

for data in survey:

    playback.greeting()

    if data.next not in basic:
        ask.next.question()

    playback.thanks() 

push.billsec()
    
"""



db_update = ("UPDATE `%s` SET `%s` = '%s' WHERE id = '%s'")



"""Recursive Function"""
def prompt(project_next):
    dtmf = digits(project_next)
    label = (label_question(project_next))
    
    agi.verbose('Prompt: {0}, Label: {1} Digits: {2}'.format((project_next), label, dtmf))
    
    entered = question('wardial/' + project_next, dtmf)
    
    #entered = random.choice(dtmf)
    agi.verbose('Tabel: {0}, Col: {1} Data: {2}'.format(project, label, entered))
    
    update(db_update % (project_next, label, entered, '3'))

    
    next = (next_question(project_next, entered))
    
    # Check for end of questions
    if next not in listData:
        prompt(next)


def question(file, valid_digits):
    regexp = re.compile(r'[' + valid_digits + ']')
    
    res = agi.get_data(file, 2000, 1)
    if regexp.search(res) is not None:
        return res

    res = agi.get_data(file, 2000, 1)    
    if regexp.search(res) is not None:
        return res
        
    if not res:
        agi.hangup()

#print ('Playback: {0}'.format((project_start)))    
#prompt(project_next)    
#print ('Playback: {0}'.format((project_finish)))
#print ('Done')

agi = AGI()
agi.answer()

try:
    """
    Check AMD dialplan variable for affirmitive setting.
    Variables evaluated in the dialplan are case-insensitive.
    
    Set(AMD = true)
    
    True values are y, yes, t, true, on and 1; 
    false values are n, no, f, false, off and 0. 
    Raises ValueError if val is anything else.
    
    When the dialpaln variable is not set, ValueError is ignored.
    """
    if(strtobool(agi.get_variable('amd'))):
        agi.appexec('AMD')
        amdstatus = agi.get_variable('AMDSTATUS')
        amdcause = agi.get_variable('AMDCAUSE')
        agi.verbose('AMD Status: {0} Cause: {1}'.format(amdstatus, amdcause))
        if amdstatus == "MACHINE":
            agi.verbose('Machine detected, hanging up')
            agi.hangup()
    else:
        agi.verbose('AMD Disabled')
except ValueError:
    agi.verbose('NOTICE: AMD Dialplan Variable NOT Set!',2)
    pass
    

project = agi.env['agi_arg_1']
agi.verbose('Processing campaign: {0}'.format(project))

#global project
#project = 'blue00000080'

project_select = ('SELECT intro_id, hangup_id, next FROM survey_details WHERE project = "%s"')

project_data = database(project_select % (project))

# Set Basic Project Details
project_start = project_data[0][0]
project_finish = project_data[0][1]
project_next = project_data[0][2]

# Define List Data (To compare start and end)
listData = list(project_data[0])
listData.pop()  # Remove project_next from end of list

#variable = agi.get_variable('variable')
#env = agi.env['agi_arg_1']
#agi.appexec('DumpChan')

agi.verbose('Playback: {0}'.format((project_start)))
agi.stream_file('wardial/' + project_start)
prompt(project_next)    
agi.verbose('Playback: {0}'.format((project_finish)))
agi.stream_file('wardial/' + project_finish)
agi.verbose('Done')

#agi.stream_file('tt-monty-knights')

agi.hangup()








    
    
    
    

