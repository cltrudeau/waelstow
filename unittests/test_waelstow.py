import os, shutil, tempfile, sys
from unittest import TestCase, TestSuite

from waelstow import (list_tests, discover_tests, capture_stdout, 
    capture_stderr, replaced_directory, pprint)

# =============================================================================

class WaelstowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        current = os.path.dirname(__file__)
        cls.start_dir = os.path.abspath(os.path.join(current, 'data'))
        cls.pattern = 'fake_testcases.py'

        cls.all_cases = {
            'ac':'test_common (fake_testcases.ATestCase)',
            'aa':'test_a (fake_testcases.ATestCase)',
            'bc':'test_common (fake_testcases.BTestCase)',
            'bb':'test_b (fake_testcases.BTestCase)',
            'cc':'test_common (fake_testcases.CTestCase)',
        }

    def _get_expected(self, names):
        keys = names.split(',')
        return [self.all_cases[key] for key in keys]

    def _get_suite_groupings(self):
        suite = discover_tests(self.start_dir, labels=['=ATest'], 
            pattern=self.pattern)
        group = TestSuite(suite)
        suite = discover_tests(self.start_dir, labels=['=BTest'], 
            pattern=self.pattern)
        group.addTests(suite)

        suite = discover_tests(self.start_dir, labels=['=CTest'], 
            pattern=self.pattern)
        return TestSuite([suite, group])

    def assert_test_strings(self, expected, tests):
        expected_names = self._get_expected(expected)
        names = [str(test) for test in tests]
        self.assertEqual(set(expected_names), set(names))

    def test_list_tests(self):
        class ModuleImportFailure(TestSuite):
            pass

        # get out test suite and add in our mock of python's failure module to
        # make sure list_tests skips it
        suite = self._get_suite_groupings()
        suite.addTest(ModuleImportFailure())

        tests = list(list_tests(suite))
        self.assert_test_strings('aa,ac,bb,bc,cc', tests)

    def _check_discover(self, labels, expected):
        suite = discover_tests(self.start_dir, labels=labels, 
            pattern=self.pattern)
        tests = list_tests(suite)
        self.assert_test_strings(expected, tests)

    def test_discover_and_shortcuts(self):
        # -- find all
        self._check_discover([], 'ac,aa,bc,bb,cc')

        # -- test shortcuts
        labels = ['=common']
        self._check_discover(labels, 'ac,bc,cc')

        labels = ['=_a', '=_b']
        self._check_discover(labels, 'aa,bb')

        labels = ['=ATest']
        self._check_discover(labels, 'aa,ac')

        # -- test full labels
        labels = [
            'fake_testcases.ATestCase.test_a',
            'fake_testcases.BTestCase.test_b',
        ]
        self._check_discover(labels, 'aa,bb')

        # -- test mix
        labels = ['=ATestCase', 'fake_testcases.BTestCase.test_b', ]
        self._check_discover(labels, 'aa,ac,bb')

    def test_misc(self):
        # misc stuff to hit our 100% coverage 
        suite = discover_tests(self.start_dir, pattern=self.pattern)
        for t in list_tests(suite):
            t.run()

    def test_replace_dir(self):
        # create a temp directory and put something in it which is to be
        # replaced
        test_dir = tempfile.mkdtemp()
        orig_file = os.path.join(test_dir, 'a.txt')
        replace_file = os.path.join(test_dir, 'b.txt')

        with open(orig_file, 'w') as f:
            f.write('foo')

        # test not a dir handling
        with self.assertRaises(AttributeError):
            # call context manager by hand as putting it in a "with" will
            # result in unreachable code which blows our testing coverage
            rd = replaced_directory(orig_file)
            rd.__enter__()

        # replace_directory should handle trailing slashes
        test_dir += '/'

        created_td = ''
        with replaced_directory(test_dir) as td:
            created_td = td

            # put something in the replaced directory
            with open(replace_file, 'w') as f:
                f.write('bar')

            # original should be moved out of path, replaced should exist
            self.assertFalse(os.path.exists(orig_file))
            self.assertTrue(os.path.exists(replace_file))

        # original should be back, replaced should be gone
        self.assertTrue(os.path.exists(orig_file))
        self.assertFalse(os.path.exists(replace_file))
        self.assertFalse(os.path.exists(created_td))

        # -- test failure still cleans up
        try:
            with replaced_directory(test_dir) as td:
                created_td = td
                raise RuntimeError()
        except:
            pass

        self.assertTrue(os.path.exists(orig_file))
        self.assertFalse(os.path.exists(created_td))

        # -- cleanup testcase
        shutil.rmtree(test_dir)

    def test_capture_stdout(self):
        with capture_stdout() as capture:
            sys.stdout.write('foo\n')

        self.assertEqual(capture.getvalue(), 'foo\n')

    def test_capture_stderr(self):
        with capture_stderr() as capture:
            sys.stderr.write('foo\n')

        self.assertEqual(capture.getvalue(), 'foo\n')

    def test_pprint(self):
        d = {
            'foo':'bar',
            'thing':3,
        }

        expected = """{\n    "foo": "bar",\n    "thing": 3\n}\n"""

        with capture_stdout() as output:
            pprint(d)

        self.assertEqual(expected, output.getvalue())
