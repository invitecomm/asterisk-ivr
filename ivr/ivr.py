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
    module: ivr

"""

import ConfigParser
#from test import joke


class IVR:
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

    """
    
    def __init__(self):
        """Load the configuration.
        """
        #       	settings = ConfigParser.RawConfigParser()
        #        settings.read(config)
        #        self.foo = settings.get('metadata', 'description-file')
		
    def f(self):
        """
        agi.say_time(seconds, escape_digits='') --> digit
        Say a given time, returning early if any of the given DTMF digits are
        pressed.  
        The time should be in seconds since the UNIX Epoch (Jan 1, 1970 00:00:00)
        
        Example:
            This is what an example should look like.
            
            for 10 in 20 {
                // Do something
            }
        """
        return self.foo

    def a(self, text):
        """
        Is this what we all want to see?
        """
        return text
    
    def dummy(self):
        return 'nothing to see here'
        """ Testing Read The Docs Content Generation """

    def dtmf(file, valid_digits):
        regexp = re.compile(r'[' + valid_digits + ']')
    
        res = agi.get_data(file, 2000, 1)
        if regexp.search(res) is not None:
            return res

        res = agi.get_data(file, 2000, 1)    
        if regexp.search(res) is not None:
            return res
        
        if not res:
            agi.hangup()        
        
        
