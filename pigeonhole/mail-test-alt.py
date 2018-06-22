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

import sys

data = {}

label = '1'
entered = '7'
data[label] = entered

label = 'b'
entered = '3'
data[label] = entered

label = 'a' 
entered = 'vv'
data[label] = entered

#if data:
#    for k, v in data.iteritems():
#        print("UPDATE table SET '{}' = {}".format(k, v))

import smtplib

gmail_user = 'support@invite-comm.jp'  

try:
    gmail_password = sys.argv[1]

    #print(sys.argv)

    sent_from = 'do-not-reply@invite-comm.jp'  
    to = ['brian.lavallee@invite-comm.jp']  
    subject = 'OMG Super Important Message'  
    body = "Hey, what's up?\n\n- You"

    email_text = "Subject: %s\n%s" %  (subject, body)

  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print 'Email sent!'

except:  
    print 'Something went wrong...  Did you include the password?'



