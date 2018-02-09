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
Asterisk Configuration File
######################################################
This module is used to read the database settings from an Asterisk configuration file.  It uses the Python ConfigParser to load the setting values directly from the specified section (context) of the Asterisk configuration file.

.. note:: You need the `MySQL Connector/Python <https://dev.mysql.com/downloads/connector/python/>`_ installed on your system to connect to the database.

Example:
    Import the module, get the config settings, and pass them to your mysql connection::

        import ivr.connection
        
        config = ivr.connection.config()
         -or-
        config = ivr.connection.config('context')
        
        database = mysql.connect(**config)

"""

asterisk_path = '/etc/asterisk'
"""String: Asterisk Configuration Directory Path

The path to the Asterisk Configuration Files for **your** installation.
"""

asterisk_conf = 'res_config_mysql.conf'
"""String: Name of the configuration file you want to use.

.. warning:: 

    The MySQL Connector/Python does not support DSN configuration options.
    
    **Do not use Asterisk ODBC configuration files!**
    
You can use any Asterisk configration file that contains the host, database, user, and password details.  
*You could create a dedicate configuration file too.*
"""

context = 'general'
"""String: The section (context) of the configration file to use.

The Asterisk configuration file can be read by the Python ConfigParser.  Just specify the section of the configration you would like to use.  The section is contained in square brackets, as shown in the following configuration file example::

    [general]
    dbhost = 127.0.0.1
    dbname = asterisk
    dbuser = myuser
    dbpass = mypass
    dbport = 3306
    dbsock = /tmp/mysql.sock
    dbcharset = utf8
    requirements=warn ; or createclose or createchar
        
"""

import os
import ConfigParser

settings = ConfigParser.RawConfigParser()
settings.read(os.path.join(asterisk_path,asterisk_conf))

def config(*args):
    if not args:
        data = {
            'user' : settings.get(context, 'dbuser'),
            'password' : settings.get(context, 'dbpass'),
            'host' : settings.get(context, 'dbhost'),
            'database' : settings.get(context, 'dbname'),
            'raise_on_warnings' : True,
        }
        return data
    else:
        data = {
            'user' : settings.get(args[0], 'dbuser'),
            'password' : settings.get(args[0], 'dbpass'),
            'host' : settings.get(args[0], 'dbhost'),
            'database' : settings.get(args[0], 'dbname'),
            'raise_on_warnings' : True,
        }
        return data 
   
        
