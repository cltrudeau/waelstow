#!/usr/bin/env python

import sys
from waelstow import discover_tests, list_tests

where = str.strip(sys.argv[1])
if where[-1] == '/':
    where = where[0:-1]

if len(sys.argv) == 1:
    labels = []
else:
    labels = sys.argv[2:]

print('Found tests:')
suite = discover_tests(where, labels)
for test in list_tests(suite):
    print('  ', test)
