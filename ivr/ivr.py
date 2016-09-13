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

"""
    module: ivr

"""

import ConfigParser
#from test import joke


class IVR:
    """A simple example class"""
    def __init__(self, config='settings.conf'):
       	settings = ConfigParser.RawConfigParser()
        settings.read(config)
        self.foo = settings.get('metadata', 'description-file')
		
    def f(self):
        """
        agi.say_time(seconds, escape_digits='') --> digit
        Say a given time, returning early if any of the given DTMF digits are
        pressed.  
        The time should be in seconds since the UNIX Epoch (Jan 1, 1970 00:00:00)
        """

        settings = ConfigParser.RawConfigParser()
        settings.read('test/settings.conf')
        return self.foo

    def a(self):
        """
        Is this what we all want to see?
        """
        #settings = ConfigParser.RawConfigParser()
        #settings.read('test/settings.conf')
        return self.foo
        #return os.path.abspath(__file__)
        
    #def j(self):
    #    return joke()