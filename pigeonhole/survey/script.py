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

"""General Database Interaction with Survey Data"""

import re
import sys
import ivr.connection
import asterisk.agi as agi
from distutils.util import strtobool
import model
import model.cached
import logging

reload(sys)
sys.setdefaultencoding("utf-8")

from datetime import datetime
import mysql.connector as mariadb


if sys.stdout.isatty():
    # colorizing exception in console for better readability
    try:
        import colored_traceback.auto
    except ImportError:
        pass

logging.basicConfig(level=logging.INFO)  # logging.DEBUG to print SQL queries

source_db_config = ivr.connection.config('portal')
destination_db_config = ivr.connection.config('survey')

use_redis_cache = True
# XXX should receive these from the config
redis_config = {'host': 'localhost', 'port': 6379}
redis_ttl = 300


class NoAnswerError(Exception):
    """
    Signifies that no valid answer was received in the allotted time
    """
    pass


class AsteriskConnectionLostError(Exception):
    """
    Raised when there's a problem communicating with Asterisk while getting callee input
    """
    pass


class Script:

    """
    sighup.handle()

    for data in survey:
        playback.greeting()

        if data.next not in basic:
            ask.next.question()

        playback.thanks()

    push.billsec()
    """

    _agi = None  # type: agi.AGI

    _model = None  # type: model.SurveyModel

    def run(self):
        self._agi = agi.AGI()

        # XXX 'env' is not in the pyst docs ~Roman Dudin
        project = self._agi.env['agi_arg_1']
        if not project:
            raise ValueError('No project specified')
        warlist = self._agi.get_variable('warlist')

        self._agi.verbose('Processing campaign: {0}'.format(project))

        if use_redis_cache:
            self._model = model.cached.SurveyModelCached(mariadb.connect(**source_db_config),
                                                                mariadb.connect(**destination_db_config),
                                                                project, warlist,
                                                                redis_config, redis_ttl)
        else:
            self._model = model.SurveyModel(mariadb.connect(**source_db_config),
                                                   mariadb.connect(**destination_db_config),
                                                   project, warlist)

        call_result = {'calldate': datetime.now()}

        try:
            self._agi.answer()

            # update("UPDATE `{0}` SET `{1}` = `{1}` + {2} WHERE id = {3}".format(project, 'attempts', 1, warlist))

            project_data = self._model.get_details()

            # set basic project details
            project_start = project_data['intro_id']
            project_finish = project_data['hangup_id']
            project_next = project_data['next']

            try:
                # Check AMD dialplan variable for affirmative setting.
                # Variables evaluated in the dialplan are case-insensitive.
                #
                # Set(AMD = true)
                #
                # True values are y, yes, t, true, on and 1;
                # false values are n, no, f, false, off and 0.
                # Raises ValueError if val is anything else.
                #
                # When the dialplan variable is not set, ValueError is ignored.
                if strtobool(self._agi.get_variable('amd')):
                    self._agi.appexec('AMD')
                    amd_status = self._agi.get_variable('AMDSTATUS')
                    amd_cause = self._agi.get_variable('AMDCAUSE')
                    self._agi.verbose('AMD Status: {0} Cause: {1}'.format(amd_status, amd_cause))
                    call_result['amdstatus'] = amd_status
                    call_result['amdreason'] = amd_cause
                    if amd_status == 'MACHINE':
                        self._agi.verbose('Machine detected, hanging up')
                        self._model.update(call_result)
                        self._agi.hangup()
                        return
                else:
                    self._agi.verbose('AMD Disabled')
            except ValueError:
                self._agi.verbose('NOTICE: AMD Dialplan Variable NOT Set!', 2)

            self.play_file(project_start)
            self.prompt(project, project_next, [project_start, project_finish], warlist, call_result)
            self.play_file(project_finish)
            self._agi.verbose('Done')

            self._agi.hangup()

            self._model.update(call_result)
        except NoAnswerError:
            self._model.update(call_result)
            self._agi.hangup()
        except (agi.AGIHangup, agi.AGIAppError, AsteriskConnectionLostError):
            # if the callee hangs up, the results are still written
            self._model.update(call_result)
            raise

    def play_file(self, file_name):
        try:
            self._agi.verbose('Playback: {0}'.format(file_name))
            self._agi.stream_file('wardial/' + file_name)
        except IOError:
            raise AsteriskConnectionLostError()

    def prompt(self, project, question_id, exit_questions, warlist, call_result):
        """
        Prompts for digits in a loop and receives the dialed digits,
        saves the result in the destination database

        :param question_id:    ID of the first question for the survey
        :type  question_id:    str
        :param warlist:        ID for the record in the destination database
        :type  warlist:        str
        :param exit_questions: List of question IDs which terminate the survey
        :type  exit_questions: List[string]
        :param project:        ID of the survey
        :type  project:        string
        :param call_result:    Aggregated parameters to update in the destination database—
                               this variable will be MODIFIED.
        :type  call_result:    dict
        """
        while True:
            valid_digits = self._model.get_valid_digits(question_id)
            question_label = self._model.get_question_label(question_id)

            self._agi.verbose('Prompt: {0}, Label: {1} Digits: {2}'.format(question_id, question_label, valid_digits))

            entered_digit = self.question('wardial/' + question_id, valid_digits)

            #entered = random.choice(dtmf)
            #self._agi.verbose('Tabel: {0}, Col: {1} Data: {2}'.format(project, label, entered))

            if entered_digit:
                call_result[question_label] = entered_digit

            question_id = self._model.get_next_question(question_id, entered_digit)
            self._agi.verbose('NEXT')

            # check for end of questions
            if question_id in exit_questions:
                break

    def question(self, prompt_file, valid_digits):
        """
        Prompts for a digit to dial and returns the received digit

        Hangs up if no valid digits are received.

        :param prompt_file: File to stream, prompting for a digit
        :type prompt_file: str
        :param valid_digits: Digits that will be accepted if dialed
        :type valid_digits: List[int|str]
        :return: Dialed digit, if valid
        :rtype: str
        """
        regexp = re.compile(r'[' + ''.join(valid_digits) + ']')

        # two attempts at receiving a valid digit
        for i in xrange(2):
            # XXX check if the result should be converted to unicode,
            #     for compatibility with other data in the script
            try:
                result = self._agi.get_data(prompt_file, 2000, 1)
                if regexp.search(result) is not None:
                    return result
            except IOError:
                raise AsteriskConnectionLostError()

        raise NoAnswerError()
