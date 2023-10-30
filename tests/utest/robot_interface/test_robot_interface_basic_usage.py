from time import time
from unittest import TestCase

from robot.result.model import (Keyword as RobotKeyword,
                                Message as RobotMessage,
                                TestCase as RobotTest,
                                TestSuite as RobotSuite)

from robot.running.model import TestSuite as RobotRunningSuite

from oxygen.robot_interface import RobotInterface, get_keywords_from

EXAMPLE_SUITES = [{
  'name': 'suite1',
  'setup': [],
  'metadata': {'metadata-key': 'metadata-value'},
  'suites': [{'name': 'suite2',
              'setup': {'elapsed': 0.0,
                        'keywords': [],
                        'messages': [],
                        'name': 'Suite Setup keyword',
                        'pass': True,
                        'tags': [],
                        'teardown': []},
              'suites': [],
              'tags': [],
              'teardown': {'elapsed': 0.0,
                           'keywords': [],
                           'messages': [],
                           'name': 'Suite Teardown keyword',
                           'pass': True,
                           'tags': [],
                           'teardown': []},
              'tests': [{'keywords': [{'elapsed': 0.0,
                                       'keywords': [],
                                       'messages': [],
                                       'name': 'casea (Execution)',
                                       'pass': True,
                                       'tags': [],
                                       'teardown': []}],
                         'name': 'casea',
                         'setup': {'elapsed': 0.0,
                                   'keywords': [],
                                   'messages': [],
                                   'name': 'Test Setup keyword',
                                   'pass': True,
                                   'tags': [],
                                   'teardown': []},
                         'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
                         'teardown': {'elapsed': 0.0,
                                      'keywords': [],
                                      'messages': [],
                                      'name': 'Suite Teardown keyword',
                                      'pass': True,
                                      'tags': [],
                                      'teardown': []}},
                        {'keywords': [{'elapsed': 0.0,
                                       'keywords': [],
                                       'messages': [],
                                       'name': 'caseb (Execution)',
                                       'pass': True,
                                       'tags': [],
                                       'teardown': []}],
                         'name': 'caseb',
                         'setup': [],
                         'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
                         'teardown': []}]}],
  'tags': [],
  'teardown': [],
  'tests': [{'keywords': [{'elapsed': 0.0,
                           'keywords': [],
                           'messages': [],
                           'name': 'case1 (Execution)',
                           'pass': True,
                           'tags': [],
                           'teardown': []}],
             'name': 'case1',
             'setup': [],
             'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
             'teardown': []},
            {'keywords': [{'elapsed': 0.0,
                           'keywords': [],
                           'messages': ['ERROR: Example error message '
                                        '(the_error_type)'],
                           'name': 'case2 (Execution)',
                           'pass': False,
                           'tags': [],
                           'teardown': []}],
             'name': 'case2',
             'setup': [],
             'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
             'teardown': []},
            {'keywords': [{'elapsed': 0.0,
                           'keywords': [],
                           'messages': ['FAIL: Example failure message '
                                        '(the_failure_type)'],
                           'name': 'case3 (Execution)',
                           'pass': False,
                           'tags': [],
                           'teardown': []}],
             'name': 'case3',
             'setup': [],
             'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
             'teardown': []},
            {'keywords': [{'elapsed': 0.0,
                           'keywords': [],
                           'messages': ['*HTML* <a href="http://robotframework.org">Robot Framework</a>'],
                           'name': 'case3 (Execution)',
                           'pass': False,
                           'tags': [],
                           'teardown': []}],
             'name': 'case3',
             'setup': [],
             'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
             'teardown': []}]
}, {
  'name': 'suite2',
  'setup': [],
  'suites': [],
  'tags': [],
  'teardown': [],
  'tests': [{'keywords': [{'elapsed': 0.0,
                           'keywords': [],
                           'messages': [],
                           'name': 'casea (Execution)',
                           'pass': True,
                           'tags': [],
                           'teardown': []}],
             'name': 'casea',
             'setup': [],
             'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
             'teardown': []},
            {'keywords': [{'elapsed': 0.0,
                           'keywords': [],
                           'messages': [],
                           'name': 'caseb (Execution)',
                           'pass': False,
                           'tags': [],
                           'teardown': []}],
             'name': 'caseb',
             'setup': [],
             'tags': ['OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME'],
             'teardown': []}]
}]


class RobotInterfaceBasicTests(TestCase):
    '''
    This tests only two methods of RobotInterface, but since they internally use
    all the other functions, pretty much everything is covered.
    '''

    def setUp(self):
        self.iface = RobotInterface()

    def now(self):
        return int(round(time() * 1000))

    def test_result_build_suites(self):
        _, converted = self.iface.result.build_suites(self.now(),
                                                      *EXAMPLE_SUITES)

        self.assertIsInstance(converted, list)
        self.assertEqual(len(converted), 2)

        for converted_suite in converted:
            self.assertIsInstance(converted_suite, RobotSuite)

        for subsuite in converted[0].suites:
            self.assertIsInstance(subsuite, RobotSuite)

        for test in converted[1].tests:
            self.assertIsInstance(test, RobotTest)

        for kw in get_keywords_from(converted[0].tests[1]):
            self.assertIsInstance(kw, RobotKeyword)

        for message in get_keywords_from(converted[0].tests[1])[0].messages:
            self.assertIsInstance(message, RobotMessage)
        self.assertEqual(get_keywords_from(converted[0].tests[3])[0].messages[0].html, True)
        self.assertEqual(get_keywords_from(converted[0].tests[3])[0].messages[0].message, ' <a href="http://robotframework.org">Robot Framework</a>')
        self.assertEqual(get_keywords_from(converted[0].tests[2])[0].messages[0].message,'FAIL: Example failure message '
                         '(the_failure_type)')
        self.assertEqual(get_keywords_from(converted[0].tests[2])[0].messages[0].html, False)

    def test_result_create_wrapper_keyword_for_setup(self):
        ret = self.iface.result.create_wrapper_keyword('My Wrapper',
                                                       '20200507 13:42:50.001',
                                                       '20200507 14:59:01.999',
                                                       True,
                                                       RobotKeyword(),
                                                       RobotKeyword())

        self.assertIsInstance(ret, RobotKeyword)
        self.assertEqual(ret.name, 'My Wrapper')
        self.assertEqual(len(get_keywords_from(ret)), 2)
        try:
            # Robot Framework < 4.0
            from robot.result.model import Keyword
            self.assertEqual(ret.type, Keyword.SETUP_TYPE)
        except AttributeError:
            # Robot Framework >= 4.0
            from robot.model import BodyItem
            self.assertEqual(ret.type, BodyItem.SETUP)

    def validate_metadata(self, actual):
        self.assertEqual(actual.name, EXAMPLE_SUITES[0]['name'])
        self.assertEqual(dict(actual.metadata), EXAMPLE_SUITES[0]['metadata'])

    def test_result_build_suite_with_metadata(self):
        _, ret = self.iface.result.build_suite(self.now(), EXAMPLE_SUITES[0])
        self.validate_metadata(ret)

    def test_result_create_wrapper_keyword_for_teardown(self):
        ret = self.iface.result.create_wrapper_keyword('My Wrapper',
                                                       '20200507 13:42:50.001',
                                                       '20200507 14:59:01.999',
                                                       False,
                                                       RobotKeyword())
        try:
            # Robot Framework < 4.0
            from robot.result.model import Keyword
            self.assertEqual(ret.type, Keyword.TEARDOWN_TYPE)
        except AttributeError:
            # Robot Framework >= 4.0
            from robot.model import BodyItem
            self.assertEqual(ret.type, BodyItem.TEARDOWN)

    def test_running_build_suite(self):
        ret = self.iface.running.build_suite(EXAMPLE_SUITES[1])

        self.assertIsInstance(ret, RobotRunningSuite)
        self.assertEqual(ret.name, EXAMPLE_SUITES[1]['name'])

    def test_running_build_suite_with_metadata(self):
        ret = self.iface.running.build_suite(EXAMPLE_SUITES[0])
        self.validate_metadata(ret)
