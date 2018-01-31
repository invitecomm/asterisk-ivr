#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# Copyright 2016~2018 INVITE Communications Co., Ltd. All Rights Reserved.
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

"""
AGI Connection with Error Handling
"""
import traceback
from asterisk.agi import *

try:
    agi = AGI()
    agi.answer()
    agi.verbose('Connected')
    d = {'col1': 'val1', 'col2': 'val2'}
    agi.verbose('UPDATE table SET {}'.format(', '.join('{}=%s'.format(k) for k in d)))
    #agi.appexec('Milliwatt')
    agi.stream_file('tt-monty-knights')
    agi.hangup()
    raise AGIAppError('Hangup','Script Complete')
except AGIAppError:
    #sql = 'UPDATE table SET {}'.format(', '.join('{}=%s'.format(k) for k in d))
    with open("/tmp/agi.txt", "a") as myfile:
        myfile.write('UPDATE table SET {}'.format(', '.join('{}=%s'.format(k) for k in d)))
except Exception as e:
    with open("/tmp/agi.txt", "a") as myfile:
        myfile.write(traceback.format_exc())

