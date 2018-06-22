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
Nothing to see here yet
"""

from string import strip
data = {}

#data = {'purple': 'zero', 'blue': 'one', 'blue': 'nine', 'red': 'two', 'green': 'three', 'yellow': 'four'}

data['green'] = 'three'
data['red'] = 'four'

sql = "UPDATE table SET ({columns}) VALUES ({values})"
db_update = ("UPDATE `%s` SET %s WHERE id = '%s'")


#print(data.keys())
#print(data.values())


def fields(data):
    SEPERATOR = ', '
    return SEPERATOR.join("`{}` = '{}'".format(k,v) for (k,v) in data.items())

def entries(data):
    SEPERATOR = ', '
    return SEPERATOR.join("'{}'".format(x) for x in data)


#print(SEPERATOR.join(["'{}'".format(v) for v in data])
#print(SEPERATOR.join("'{}'".format(v) for v in data.values()))

#print(flatten(data.keys()))
#print(flatten(data.values()))


print(db_update % ('my_table', fields(data), '12345' ))
