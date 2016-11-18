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

	#! /usr/bin/env python
	# -*- coding: utf-8 -*-
	# vim: set et sw=4 fenc=utf-8:
	"""
	A Simple Example
	"""
	import mysql.connector as mariadb
	
	config = {'data': 'ommited'}
	connection = mariadb.connect(**config)
	"""
	Establish Database Connection
	"""

Topic 1
*************

Topic 2
*************

Sub Title 2
##################

Topic 3
*************

Topic 4
*************




.. toctree::
   :maxdepth: 2
   :glob: