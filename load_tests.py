#!/usr/bin/env python
import unittest, sys
from waelstow import discover_tests, list_tests

if __name__ == '__main__':
    suite = discover_tests('tests', sys.argv[1:])
    unittest.TextTestRunner(verbosity=1).run(suite)
