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
Database Connection Settings from Asterisk
======================================================

This module is used to read the database settings from an Asterisk configuration file.  It uses the Python ConfigParser to load the setting values directly from the specified section (context) of the Asterisk configuration file.

.. note:: You need the `MySQL Connector/Python <https://dev.mysql.com/downloads/connector/python/>`_ installed on your system to connect to the database.

Example:
    Import the module, get the config settings, and pass them to your mysql connection::

        import ivr.connection
        config = ivr.connection.config
        database = mysql.connect(**config)

"""

asterisk_path = '/etc/asterisk'
"""String: Directory Path

The path to the Asterisk Configuration Files for **your** installation.
"""

asterisk_conf = 'res_config_mysql.conf'
"""String: Name of the configuration file you want to use.

.. warning:: 

    The MySQL Connector/Python does not support DSN configuration options.
    
    **Do not use Asterisk ODBC configuration files!**
    
You can use any Asterisk configration file that contains the host, database, user, and password details.  *You could create a dedicate configuration file too.*
"""

context = 'general'
"""String: The section (context) of the configration file to use.

The Asterisk configuration file can be read by the Python ConfigParser.  Just specify the section of the configration you would like to use, as shown in the following configuration file example::

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

if __name__ == "__main__": 
    config = {
      'user' : settings.get(context, 'dbuser'),
      'password' : settings.get(context, 'dbpass'),
      'host' : settings.get(context, 'dbhost'),
      'database' : settings.get(context, 'dbhost'),
      'raise_on_warnings' : True,
    }
else:
    # Dummy Module for Sphinx AutoDoc
    config = {'user':'myuser', 'password':'mypass', 'host':'127.0.0.1', 'database':'asterisk'}
    """    
    Using the arguments defined in this module, `connection.config`_ will return the settings needed to connect to the database.  
    
    Args:
        param1 (str): `connection.asterisk_path`_
        param2 (str): `connection.asterisk_conf`_
        param3 (str): `connection.context`_

        * `connection.asterisk_path`_
        * `connection.asterisk_conf`_
        * `connection.context`_
        
    Example:
        The following code is used to generate the connection data::
        
            settings = ConfigParser.RawConfigParser()
            settings.read(os.path.join(asterisk_path,asterisk_conf))

            config = {
              'user' : settings.get(context, 'dbuser'),
              'password' : settings.get(context, 'dbpass'),
              'host' : settings.get(context, 'dbhost'),
              'database' : settings.get(context, 'dbhost'),
              'raise_on_warnings' : True,
            }
        
    Returns:
        list: Comma-separated list of elements used to connect to the database.
             
    """

print config