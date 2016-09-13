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
    synopsis: This module contains functions and classes to implment IVR scripts.
   
pyvr

{'agi_callerid' : 'mars.putland.int',
 'agi_channel'  : 'IAX[kputland@kputland]/119',
 'agi_context'  : 'default',
 'agi_dnid'     : '1000',
 'agi_enhanced' : '0.0',
 'agi_extension': '1000',
 'agi_language' : 'en',
 'agi_priority' : '1',
 'agi_rdnis'    : '',
 'agi_request'  : 'pyst',
 'agi_type'     : 'IAX'}

Specification
-------------
"""

import ConfigParser
#from test import joke


class IVR:
    """A simple example class"""
    def __init__(self):
       	settings = ConfigParser.RawConfigParser()
        settings.read('test/settings.conf')
        self.foo = settings.get('metadata', 'description-file')
		
    def f(self):
        """ Nothing to see here"""
        settings = ConfigParser.RawConfigParser()
        settings.read('test/settings.conf')
        return self.foo
        #return os.path.abspath(__file__)
        
    #def j(self):
    #    return joke()