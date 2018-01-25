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


"""Packaging files and information."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from ivr import __version__ as version

setup(
    name = 'ivr',
    packages = ['ivr'], # this must be the same as the name above
    version = version,
    description = 'AGI Controlled IVR for Asterisk',
    author = 'Brian LaVallee',
    author_email = 'brian.lavallee@invite-comm.jp',
    url = 'https://github.com/invitecomm/asterisk-ivr', # use the URL to the github repo
    download_url = 'https://github.com/invitecomm/asterisk-ivr/tarball/' + version, # I'll explain this in a second
    keywords = 'python asterisk agi ivr telephony telephony sip voip',
    classifiers = [
        #'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
    ],
    license = 'GNU General Public License',

    # Package dependencies:
    install_requires = [
        'six>=1.9.0',
        'google-api-python-client==1.5.3',
        'pyst2',
        'mysql-connector-python>=2.1.0',
        'retry',
    ],
    
)