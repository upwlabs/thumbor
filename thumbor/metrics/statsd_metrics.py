#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from statsd import statsd
from thumbor.metrics import BaseMetrics


class Metrics(BaseMetrics):

    def incr(self, metricname, value=1):
        statsd.increment('thumbor.' + metricname, value)

    def timing(self, metricname, value):
        statsd.timing('thumbor.' + metricname, value)
