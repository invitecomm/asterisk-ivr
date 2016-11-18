.. Asterisk IVR documentation master file, created by
   sphinx-quickstart on Mon Nov 14 16:14:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

****   
Read the Docs
****

Getting it working::
##################

::

	# -*- coding: utf-8 -*-
	"""
	A Simple Example
	"""
	from asterisk.agi import *

	agi = AGI()
	"""
	Create an AGI Instance 
	"""
	agi.answer()
	"""
	I/O Communications: stdin, stdout, and stderr
	"""

Advanced Settings: Install Project:
*************

setup.py install
*************
setup.py::
   
	# Package dependencies:
	install_requires = ['six>=1.9.0','google-api-python-client==1.5.3','pyst2'],


Sub Title 2
##################

Topic 3
*************

Topic 4
*************




.. toctree::
   :maxdepth: 2
   :glob: