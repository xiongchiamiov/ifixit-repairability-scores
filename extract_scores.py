#!/usr/bin/env python
# -*- coding: utf-8 -*-

# May you recognize your weaknesses and share your strengths.
# May you share freely, never taking more than you give.
# May you find love and love everyone you find.

import codecs
import re
import signal
import sys

from jinja2 import Environment, FileSystemLoader
from pyfixit.guide import Guide

# Stack traces are ugly; why would we want to print one on ctrl-c?
def nice_sigint(signal, frame):
   print('')
   sys.exit(0)
signal.signal(signal.SIGINT, nice_sigint)

# Unicode is a bitch when redirecting stdout.
# http://stackoverflow.com/a/1169209/120999
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

scores = []

teardowns = Guide.all(filter='teardown')
for teardown in teardowns:
   #print('=' * 80)
   #print(teardown.title)
   #print('=' * 80)
   # Guess that a repairability score, if it exists, will be in the last step.
   if teardown.steps:
      for line in teardown.steps[-1].lines:
         #print(unicode(line.text))
         match = re.match(r".*Repairability( Score)?: '''(\d+)", unicode(line.text))
         if match:
            (_, score) = match.groups()
            score = int(score)
            #print('%s: %d' % (teardown.title, score))
            scores.append((teardown, score))
   #sys.stdout.flush()

env = Environment(loader=FileSystemLoader('.'))
print(env.get_template('scores.html').render(scores=scores))

