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

from asterisk.agi import *
import re

def question(file, valid_digits):
    regexp = re.compile(r'[' + valid_digits + ']')
    
    counter = 0
    while counter:
    
        res = agi.get_data(file, 20000, 1)
        if regexp.search(res) is not None:
            agi.verbose('Entry Was %s' % res)
            return res
        if not res:
            agi.hangup()
        counter = counter + 1    
        if counter = 2:
            agi.hangup()
            
    
agi = AGI()
agi.answer()
agi.verbose("python agi started")
#agi.stream_file('wardial/greeting')

q1 = question('wardial/question1', '12')
#digits='12'
#regexp = re.compile(r'[' + digits + ']')
#if not q1:
#    agi.hangup()
##if regexp.search(q1) is None:
#    agi.verbose('Entry Was %s' % q1)
#    agi.stream_file('invalid')
    
agi.get_data('wardial/question2', 20000, 1)
agi.get_data('wardial/question3', 20000, 1)
agi.get_data('wardial/question4', 20000, 1)
agi.get_data('wardial/question5', 20000, 1)
agi.stream_file('wardial/goodby')
agi.hangup()




