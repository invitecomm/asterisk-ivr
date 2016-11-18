.. Asterisk IVR documentation master file, created by
   sphinx-quickstart on Mon Nov 14 16:14:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

****   
Read the Docs
****

Read the Docs isn't just another site to post documentation.  It supports various markup languages, which just provides flexibility.  

The real **power** of Read the Docs is the ability to generate documentation from the docstrings contained within your code.  *The only problem is how to generate this documentation, isn't documented well.*

Banging on the Keyboard
##################

Getting it working, getting Read the Docs to generate documentation using the docstrings was a frustrating experience.  Lot's of *Banging on the Keyboard*, trying different things, and making changes all over the place.

Installing ``sphinx`` locally and running ``sphinx-quickstart`` **may** have been the solution.  *..or helped get closer to making the documentation with ``docstrings``.*

Sphinx Markup
##################

::

This is how code is ``written``.
Good luck!  maybe
		

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
	
	It appears to choke when it reaches ``agi.answer()``
	
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