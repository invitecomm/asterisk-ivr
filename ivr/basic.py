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
Nothing to see here yet
######################################################

Need to add text here.
"""
class ExampleError(Exception):
    """Exceptions are documented in the same way as classes.

    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.

    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.

    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

try:
    """
    Check AMD dialplan variable for affirmitive setting.
    Variables evaluated in the dialplan are case-insensitive.
    
    Set(AMD = true)
    
    True values are y, yes, t, true, on and 1; 
    false values are n, no, f, false, off and 0. 
    Raises ValueError if val is anything else.
    
    When the dialpaln variable is not set, ValueError is ignored.
    """
    if(strtobool(agi.get_variable('amd'))):
        agi.appexec('AMD')
        amdstatus = agi.get_variable('AMDSTATUS')
        amdcause = agi.get_variable('AMDCAUSE')
        agi.verbose('AMD Status: {0} Cause: {1}'.format(amdstatus, amdcause))
    else:
        agi.verbose('AMD Disabled')
except ValueError:
    agi.verbose('NOTICE: AMD Dialplan Variable NOT Set!',2)
    pass