# -*- coding: utf-8 -*-
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
Creates an email from an HTML template and sends it.

Jinja2 is used for the HTML and plain text templates. The subject is also a template.
Arbitrary parameters can be supplied, to be substituted in all three templates.

Images can be attached to the message. They must be referenced in the HTML in the "content-id" format,
as e.g. ``<img src="cid:img1.gif">``. Basename of each file is used as the ID. Right now, it's assumed
that each file is an image, so "image/something" MIME types are used.
"""


import smtplib
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
import jinja2


def send(send_from, send_to,
         subject_template, text_template_file_name, html_template_file_name, image_files, template_params,
         smtp_server, smtp_port, smtp_user, smtp_password):
    """
    :type  send_from:               str
    :type  send_to:                 str
    :type  subject_template:        str
    :type  text_template_file_name: str
    :type  html_template_file_name: str
    :param image_files:             List of files to attach to the message
    :type  image_files:             list[str]
    :param template_params:         Parameters to substitute in the template
    :type  template_params:         dict
    :type  smtp_server:             str
    :type  smtp_port:               int
    :type  smtp_user:               str
    :type  smtp_password:           str
    """
    message = _construct_message(send_from, send_to,
                                 subject_template, text_template_file_name, html_template_file_name, image_files,
                                 template_params)
    _send(send_from, send_to, message, smtp_server, smtp_port, smtp_user, smtp_password)


def _construct_message(send_from, send_to,
                       subject_template, text_template_file_name, html_template_file_name, image_files,
                       template_params):
    """
    :type  send_from:               str
    :type  send_to:                 str
    :type  subject_template:        str
    :type  text_template_file_name: str
    :type  html_template_file_name: str
    :param image_files:             List of files to attach to the message
    :type  image_files:             list[str]
    :param template_params:         Parameters to substitute in the template
    :type  template_params:         dict
    :return: Formatted message as a string
    :rtype:  str
    """
    # multipart/related is required to attach images
    message = MIMEMultipart('related', charset='utf-8')
    message['From'] = send_from
    message['To'] = send_to
    message['Date'] = formatdate()
    message['Subject'] = _parse_template_string(subject_template, template_params)

    # multipart/alternative is used to supply both HTML and plain text versions
    inner_message = MIMEMultipart('alternative')
    inner_message.attach(MIMEText(_parse_template(text_template_file_name, template_params), 'plain', 'utf-8'))
    inner_message.attach(MIMEText(_parse_template(html_template_file_name, template_params), 'html', 'utf-8'))
    message.attach(inner_message)

    for image_filename in image_files:
        with open(image_filename, "rb") as image_file:
            image_basename = os.path.basename(image_filename)
            part = MIMEImage(
                image_file.read(),
                Name=image_basename
            )
            part['Content-Disposition'] = 'inline; filename="{0}"'.format(image_basename)
            part['Content-ID'] = '<{0}>'.format(image_basename)
            message.attach(part)

    return message.as_string()


def _parse_template(template_file_name, params):
    """
    :type template_file_name: str
    :type params:             dict
    :rtype: str
    """
    with open(template_file_name, 'r') as template_file:
        return _parse_template_string(template_file.read().decode('utf-8'), params)


def _parse_template_string(template, params):
    """
    :type template: unicode
    :type params:   dict
    :rtype: str
    """
    return jinja2.Template(template).render(params)


def _send(send_from, send_to, message,
          smtp_server, smtp_port, smtp_user, smtp_password):
    """
    :type send_from:     str
    :type send_to:       str
    :type message:       str
    :type smtp_server:   str
    :type smtp_port:     int
    :type smtp_user:     str
    :type smtp_password: str
    """
    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)  # TODO support sending without SSL?
    if smtp_user:
        smtp.login(smtp_user, smtp_password)
    smtp.sendmail(send_from, send_to, message)
    smtp.close()
