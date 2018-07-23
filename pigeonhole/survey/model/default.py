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
Database storage layer for the survey

(This module should be imported as just 'survey.model'.)
"""

from __future__ import print_function
import mysql.connector
import logging


logger = logging.getLogger('survey.model')


class SurveyModel(object):
    """Database storage layer for the survey"""

    _schema_version = 'v2'
    """
    This value must be changed with *any* changes in the structure of data or of values that are returned
    by the methods of the model, if those methods existed before.
    
    Used e.g. for caching (see :py:class:`cached.SurveyModelCached`).
    """

    _project = None  # type: str
    """Name of the survey in the source database"""
    _id = None  # type: str|int
    """ID of the survey in the stats table (aka 'warlist')"""

    _source_db = None  # type: mysql.connector.MySQLConnection
    _destination_db = None  # type: mysql.connector.MySQLConnection

    _survey = None  # type: dict
    """The survey record"""

    _details = None  # type: dict
    """Survey details"""

    _user = None  # type: dict
    """Record for the user"""

    _questions = None  # type: list[dict]
    """List of all questions in the survey: records from the 'survey_questions' table"""

    _question_answers = None  # type: list
    """List of DTMF records for all questions"""

    def __init__(self, source_db, destination_db, project, id):
        """
        :param source_db:      Source database connection (read-only)
        :type  source_db:      mysql.connector.MySQLConnection
        :param destination_db: Connection to the database for collected survey stats (writable)
        :type  destination_db: mysql.connector.MySQLConnection
        :param project:        Name of the survey in the source database
        :type  project:        str
        :param id:             ID of the survey in the stats table (aka 'warlist')
        :type  id:             str|int
        """
        self._source_db = source_db
        self._destination_db = destination_db
        self._project = project
        self._id = id

    def get_survey(self):
        """
        Get survey record (from the 'survey' table)
        """
        if self._survey is None:
            self._survey = self._query('SELECT * FROM `survey` WHERE `project` = %s', [self._project])[0]
        return self._survey

    def get_details(self):
        """
        Get survey details (from the 'survey_details' table)
        """
        if self._details is None:
            self._details = self._query('SELECT * FROM `survey_details` WHERE `project` = %s', [self._project])[0]
        return self._details

    def get_user(self):
        """
        Get the user
        """
        if self._user is None:
            self._user = self._query('SELECT * FROM `users` WHERE `id` = %s',
                                     [self.get_survey()['user']])[0]
        return self._user

    def get_question_by_name(self, question_name):
        """
        Get a question record by its 'question' field
        """
        for item in self.get_questions():
            if item['question'] == question_name:
                return item
        raise KeyError('No question with the name "{0}" in the question list'.format(question_name))

    def get_questions(self):
        """
        Gets the list of all questions for the survey

        :return: Dictionary: {question: label}
        :rtype:  list[dict]
        """
        if self._questions is None:
            self._questions = self._query('SELECT * FROM `survey_questions` WHERE `project` = %s', [self._project])
        return self._questions

    def get_valid_digits(self, question_id):
        """
        Get the list of valid digits for a question

        :rtype: List[str]
        """
        return [row['dtmf'] for row in self.get_question_answers() if row['question'] == question_id]

    def get_next_question(self, current_question_id, entered_digit):
        """
        Get ID of the next question based on an entered DTMF

        :rtype: str
        """
        for row in self.get_question_answers():
            if row['question'] == current_question_id and row['dtmf'] == entered_digit:
                return row['dtmf_next']
        raise KeyError(
            'No DTMF record for question "{0}" and entered digit "{1}"'.format(current_question_id, entered_digit))

    def get_question_answers(self):
        """
        Gets the list of valid answers and next questions for all questions in the current survey

        :return: List of DTMF records for all questions
        :rtype:  list
        """
        if self._question_answers is None:
            self._question_answers = self._query('SELECT * FROM `survey_questions_dtmf` WHERE `project` = %s',
                                                 [self._project])
        return self._question_answers

    def update(self, parameters):
        """
        Write survey results in the destination database

        :param parameters: A dictionary of fields to update
        :type  parameters: dict
        """
        # convert unicode keys to strings so the mysql connector finds mappings from fields in the query
        values = dict((str(key), value) for key, value in parameters.items())
        fields_sql = [ '`{0}` = %({0})s'.format(field) for field in values.keys()]
        values['id'] = self._id

        cursor = self._destination_db.cursor()
        try:
            cursor.execute('UPDATE `' + self._project + '` SET ' + ', '.join(fields_sql) + ' WHERE id = %(id)s', values)
            self._destination_db.commit()
        finally:
            logger.debug('Executed MySQL query: %s', cursor._executed)

    def _query(self, query, params=None):
        cursor = self._source_db.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            logger.debug('Executed MySQL query: %s', cursor._executed)
