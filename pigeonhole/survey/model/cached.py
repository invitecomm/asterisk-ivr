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
This module implements a cache for the survey model.

Use a Redis instance configured to serve as a cache, see `Redis docs`_.

.. _Redis docs: https://redis.io/topics/lru-cache

E.g.::

  maxmemory 100mb
  maxmemory-policy allkeys-lru
  # or: maxmemory-policy volatile-lru  # if you have other data in the same Redis instance
  # or allkeys-lfu or volatile-lfu to have an LFU cache

Supply the ``ttl`` parameter to the SurveyModelCached constructor to enable TTL for the records in Redis
(especially necessary if using volatile-lru or volatile-lfu). If TTL is not specified, the lifetime
of records will not be limited, and they will expire only when memory is needed for new records.

All keys created in Redis will begin with 'survey_'.

To have the cache update all data when schema is changed, you'll need to edit the field
:py:attr:`default.SurveyModel._schema_version`. Note that this will invalidate *all* keys in the cache,
so for more granular invalidation you might want to edit individual keys in the methods of
:py:class:`SurveyModelCached`.

(For proper consistency, records in Redis caches should be purged when original data is updated.)
"""

from __future__ import print_function
import default
import redis
import json
import logging


logger = logging.getLogger('survey.model_cached')


class SurveyModelCached(default.SurveyModel):

    _redis_config = None  # type: dict
    _redis_connection = None  # type: redis.StrictRedis

    _ttl = None  # type: int

    @property
    def _redis(self):
        if self._redis_connection is None:
            self._redis_connection = redis.StrictRedis(**self._redis_config)
        return self._redis_connection

    def __init__(self, source_db_config, destination_db_config, project, id, redis_config, ttl=None):
        """
        :param redis_config: Connection parameters for redis.StrictRedis — host, port, etc (see redis-py's docs)
        :type  redis_config: dict
        :param ttl:          TTL for records written in Redis, in seconds, or None/0/False to not set the TTL
        :type  ttl:          int|None
        """
        super(SurveyModelCached, self).__init__(source_db_config, destination_db_config, project, id)
        self._redis_config = redis_config
        self._ttl = ttl

    def get_details(self):
        if self._details is None:
            self._details = self._get_cached(
                'survey_details_' + self._project,
                super(SurveyModelCached, self).get_details,
                'Got survey details from the cache for the survey ' + self._project
            )
        return self._details

    def get_questions(self):
        if self._questions is None:
            self._questions = self._get_cached(
                'survey_questions_' + self._project,
                super(SurveyModelCached, self).get_questions,
                'Got question labels from the cache for the survey ' + self._project
            )
        return self._questions

    def get_question_answers(self):
        if self._question_answers is None:
            self._question_answers = self._get_cached(
                'survey_question_answers_' + self._project,
                super(SurveyModelCached, self).get_question_answers,
                'Got question answers from the cache for the survey ' + self._project
            )
        return self._question_answers

    # TODO add caching for other methods

    def _get_cached(self, cache_key, fetch_func, log_message):
        """
        :type cache_key: str
        :type fetch_func: callable
        :type log_message: str
        """
        cache_key = cache_key + '_' + self._schema_version
        result = self._get(cache_key)
        if result is None:
            result = fetch_func()
            self._set(cache_key, result)
        else:
            logger.debug(log_message)
        return result

    def _set(self, key, value):
        self._redis.set(key, json.dumps(value), ex=(self._ttl if self._ttl else None))

    def _get(self, key):
        result = self._redis.get(key)
        return None if result is None else json.loads(result)
