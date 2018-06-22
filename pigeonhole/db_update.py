#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# Copyright 2018 INVITE Communications Co., Ltd. All Rights Reserved.
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
Dictionary to MySQL UPDATE. 
Uses set of key: value pairs
"""

data = {}

data['white'] = 'two'
data['green'] = 'three'
data['red'] = 'four'

db_update = ("UPDATE `%s` SET %s WHERE id = '%s'")

def fields(data):
    SEPERATOR = ', '
    return SEPERATOR.join("`{}` = '{}'".format(k,v) for (k,v) in data.items())

print(db_update % ('my_table', fields(data), '12345' ))