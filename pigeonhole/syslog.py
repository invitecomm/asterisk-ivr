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

import logging
import logging.handlers

syslog = logging.getLogger(__name__)

syslog_handler = logging.handlers.SysLogHandler('/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')

syslog.setLevel(logging.DEBUG)
syslog_handler.setFormatter(formatter)
syslog.addHandler(syslog_handler)

def hello():
    syslog.info('info')
    syslog.warning('warning')
    syslog.error('error')
    syslog.critical('critical')
    try:
        goodbye()
    except:
        syslog.exception('exception')

if __name__ == '__main__':
    hello()

