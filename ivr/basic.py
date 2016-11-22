#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
"""
A Simple Example
"""

from asterisk.agi import *

myVar = 'some data'
"""
A Simple Variable
"""

agi = AGI()
"""
Create an AGI Instance 
"""

agi.answer()
"""
I/O Communications: stdin, stdout, and stderr
"""