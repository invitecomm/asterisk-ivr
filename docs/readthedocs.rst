.. Asterisk IVR documentation master file, created by
   sphinx-quickstart on Mon Nov 14 16:14:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

****   
Read the Docs
****

Read the Docs isn't just another site to post documentation.  It supports various markup languages, which just provides flexibility.  

The real **power** of Read the Docs is the ability to generate documentation from the docstrings contained within the code.  *The only problem is HOW TO generate this documentation, isn't documented well.*

Banging on the Keyboard
##################

Importing Python Docstrings
*************

::

	# -*- coding: utf-8 -*-
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

.. warning:: 

	This does not work.  `Read the Docs <https://readthedocs.org/>`_  doesn't display anything.
	
	It appears to choke when it reaches agi.answer()
	
Advanced Settings: Install Project:
*************

setup.py install
*************
setup.py::
   
	# Package dependencies:
	install_requires = ['pyst2'],


Sub Title 2
##################

Topic 3
*************

Topic 4
*************




.. toctree::
   :maxdepth: 2
   :glob: