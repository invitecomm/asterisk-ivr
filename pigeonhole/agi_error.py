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

import sys
from asterisk.agi import *

try:
    agi = AGI()
    agi.answer()
    agi.verbose('Connected')
    agi.appexec('Milliwatt')
    #agi.hangup()
except:
    with open("/tmp/agi.txt", "a") as myfile:
        myfile.write("Unexpected error:", sys.exc_info()[0])
        

