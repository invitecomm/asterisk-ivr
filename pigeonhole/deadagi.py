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

import signal, os

def handler(signum, frame):
    agi.verbose('SIGHUP')
    raise agi.verbose('SIGHUP')

signal.signal(signal.SIGHUP, handler)

agi = AGI()
agi.answer()

clid = agi.env['agi_accountcode']

agi.verbose('Playback Started')
agi.stream_file('tt-codezone')
agi.verbose('playback ended')

foo = agi.get_variable('CDR(billsec)')
agi.verbose(foo)

agi.stream_file('tt-codezone')
agi.verbose('playback ended')

foo = agi.get_variable('CDR(billsec)')
agi.verbose(foo)


agi.hangup()