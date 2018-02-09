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
*You could create a dedicated configuration file too.*
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

odbc_context = 'asterisk'
"""String: The section (context) of the ODBC configration file to use.

The Asterisk configuration file can be read by the Python ConfigParser.  Just specify the section of the configration you would like to use.  The section is contained in square brackets, as shown in the following configuration file example::

[asterisk]
enabled => no
dsn => MySQL-asterisk
username => myuser
password => mypass
pre-connect => yes

"""

import os
import ConfigParser


RES_ODBC_CONF = os.path.join(asterisk_path, 'res_odbc.conf')
ODBC_INI = os.environ.get('ODBCINI', '/etc/odbc.ini')

odbc2mysql = {
    'user': 'user',
    'uid':  'user',
    'server': 'host',
    'database': 'database',
    'port': 'port',
    'password': 'password',
    'pwd': 'password',
    'socket': 'unix_socket',
    'sslca': 'ssl_ca',
    'sslcert': 'ssl_cert',
    'sslkey': 'ssl_key',
    'sslverify': 'ssl_verify_cert',
    'charset': 'charset',
}


def load_from(path):
    settings = ConfigParser.RawConfigParser()
    settings.read(path)
    return settings


def dsn_from(path, context='asterisk'):
    return safe_get_from(
        load_from(path), context, ['dsn']).replace('>', '').strip()


def creds_from(path, context='asterisk'):
    odbc_conf = load_from(path)
    user = safe_get_from(odbc_conf, context, ['username'])
    password = safe_get_from(odbc_conf, context, ['password'])
    return user.replace('>', '').strip(), password.replace('>', '').strip()

def discard_comments(value):
    if type(value) == str:
        return value if '#' not in value else value.split('#')[0].strip()
    else:
        return value

def safe_get_from(settings, section, keys):
    for key in keys:
        try:
            return settings.get(section, key)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as err:
            # TODO: replace with logging
            print(err)
    return ''


def load_from_odbc(path, dsn=''):
    settings = load_from(path)

    driver = discard_comments(settings.get(dsn, 'driver'))
    if driver != 'MySQL':
        raise Exception("Expected MySQL driver, found %s", driver)

    items = {}
    for k, v in settings.items(dsn):
        if odbc2mysql.get(k, None):
            items[odbc2mysql[k]] = v

    # careful with iterating dict modification (at least, in py3)
    for k, v in items.items():
        items[k] = discard_comments(v)
    return items


def config_from_odbc(path, context):
    dsn = dsn_from(RES_ODBC_CONF, context=context)
    if not dsn:
        return {}
    return load_from_odbc(ODBC_INI, dsn)


def config(context=odbc_context, override_creds=False):
    data = config_from_odbc(ODBC_INI, context)
    if override_creds:
        data['user'], data['password'] = creds_from(RES_ODBC_CONF, context=context)
    #remove_junk(data)
    return data


def remove_junk(items):
    connector_acceptable_fields = {
        'user',
        'password',
        'database',
        'host',
        'port',
        'unix_socket',
        'auth_plugin',
        'use_unicode',
        'charset',
        'collation',
        'autocommit',
        'time_zone',
        'sql_mode',
        'get_warnings',
        'raise_on_warnings',
        'connection_timeout',
        'client_flags',
        'buffered',
        'raw',
        'consume_results',
        'ssl_ca',
        'ssl_cert',
        'ssl_key',
        'ssl_verify_cert',
        'force_ipv6',
        'dsn',
        'pool_name',
        'pool_size',
        'pool_reset_session',
        'compress',
        'converter_class',
        'failover',
        'option_files',
        'option_groups',
        'allow_local_infile',
        'use_pure'
    }
    # Remove all that is not compatible with MySQL connector API
    # see https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    data = dict((k, v) for k, v in items if k in connector_acceptable_fields)
    return data

