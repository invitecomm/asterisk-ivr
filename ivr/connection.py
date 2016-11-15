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
Database Connection Using Asterisk Settings
======================================================

This module is used to read the database settings from an Asterisk configuration file.  It uses the Python ConfigParser to load the setting values directly from the specified section (context) of the Asterisk configuration file.

.. note:: You need the `MySQL Connector/Python <https://dev.mysql.com/downloads/connector/python/>`_ installed on your system to connect to the database.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        import ivr.connection
        config = ivr.connection.config
        database = mysql.connect(**config)

"""

asterisk_path = '/etc/asterisk'
"""String: Directory Path

The path to the Asterisk Configuration Files.
"""

asterisk_conf = 'res_config_mysql.conf'
"""String: Name of the configuration file you want to use.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""

context = 'general'
"""String: Section (context) of the configration file to use.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon::

    [general]
    dbhost = localhost
    dbname = myDatabase
    dbuser = myUsername
    dbpass = mySecretPassword
    dbport = 3306
    ;dbsock = /tmp/mysql.sock
    dbcharset = utf8
    requirements=warn ; or createclose or createchar
        
"""

