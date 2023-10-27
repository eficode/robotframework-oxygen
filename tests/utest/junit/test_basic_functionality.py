from pathlib import Path
from unittest import skip, TestCase
from unittest.mock import ANY, create_autospec, Mock, patch

from junitparser import JUnitXml
from testfixtures import compare

from oxygen.base_handler import BaseHandler
from oxygen.errors import JUnitHandlerException, ResultFileIsNotAFileException
from oxygen.junit import JUnitHandler
from oxygen.oxygen_handler_result import validate_oxygen_suite
from ..helpers import example_robot_output, get_config, RESOURCES_PATH

class JUnitBasicTests(TestCase):

    def setUp(self):
        self.handler = JUnitHandler(get_config()['oxygen.junit'])

    def test_initialization(self):
        self.assertEqual(self.handler.keyword, 'run_junit')
        self.assertEqual(self.handler._tags, ['JUNIT', 'EXTRA_JUNIT_CASE'])

    @patch('oxygen.junit.JUnitXml')
    @patch('oxygen.junit.JUnitHandler._transform_tests')
    @patch('oxygen.junit.validate_path')
    def test_parsing(self, mock_validate_path, mock_transform, mock_junitxml):
        m = create_autospec(Path)
        mock_validate_path.return_value = m
        mock_junitxml.fromfile.return_value = 'some junit'

        self.handler.parse_results('some/file/path.ext')

        mock_validate_path.assert_called_once_with('some/file/path.ext')
        mock_junitxml.fromfile.assert_called_once_with(m)
        mock_transform.assert_called_once_with('some junit')

    def test_result_file_is_not_a_string(self):
        with self.assertRaises(ResultFileIsNotAFileException) as ex:
            self.handler.parse_results(None)

        ex = str(ex.exception)
        self.assertIn('File "None" is not a file', ex)

    @patch('oxygen.utils.subprocess')
    def test_running(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)
        self.handler.run_junit('somefile', 'some command')
        mock_subprocess.run.assert_called_once_with('some command',
                                                    capture_output=True,
                                                    shell=True,
                                                    env=ANY)

    def subdict_in_parent_dict(self, parent_dict, subdict):
        return all(
            subitem in parent_dict.items() for subitem in subdict.items())

    @patch('oxygen.utils.subprocess')
    def test_running_with_passing_environment_variables(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)
        self.handler.run_junit('somefile', 'some command', env_var='value')
        mock_subprocess.run.assert_called_once_with('some command',
                                                    capture_output=True,
                                                    shell=True,
                                                    env=ANY)
        passed_full_env = mock_subprocess.run.call_args[-1]['env']
        self.assertTrue(self.subdict_in_parent_dict(passed_full_env,
                                                    {'env_var': 'value'}))

    @patch('oxygen.utils.subprocess')
    def test_running_fails_correctly(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=255)
        with self.assertRaises(JUnitHandlerException):
            self.handler.run_junit('somefile',
                                   'some command',
                                   check_return_code=True)

    @patch('oxygen.utils.subprocess')
    def test_running_does_not_fail_by_default(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=255)
        retval = self.handler.run_junit('somefile', 'some command')
        self.assertEqual(retval, 'somefile')

    def test_cli(self):
        self.assertEqual(self.handler.cli(), BaseHandler.DEFAULT_CLI)

    @patch('oxygen.junit.JUnitHandler._report_oxygen_run')
    def test_check_for_keyword(self, mock_report):
        fake_test = example_robot_output().suite.suites[0].tests[0]
        expected_data = {'Atest.Test.My First Test': '/some/path/to.ext'}

        self.handler.check_for_keyword(fake_test, expected_data)

        self.assertEqual(mock_report.call_args[0][0].name,
                         'oxygen.OxygenLibrary.Run Junit')
        self.assertEqual(self.handler.run_time_data, '/some/path/to.ext')

    def test_transform_tests_with_single_test_suite(self):
        expected_output = {
            'name': 'JUnit Execution',
            'suites': [{'name': 'com.example.demo.DemoApplicationTests',
                'suites': [],
                'tags': [],
                'tests': [{'keywords': [{'elapsed': 454.0,
                                         'keywords': [],
                                         'messages': [],
                                         'name': 'contextLoads() (Execution)',
                                         'pass': True}],
                            'name': 'contextLoads()',
                            'tags': []}]}],
            'tags': ['JUNIT', 'EXTRA_JUNIT_CASE'],
        }
        xml = JUnitXml.fromfile(str(RESOURCES_PATH / 'junit-single-testsuite.xml'))
        retval = self.handler._transform_tests(xml)
        compare(retval, expected_output)

    def test_transform_tests_with_multiple_suites(self):
        expected_output = {
            'name': 'JUnit Execution',
            'tags': ['JUNIT', 'EXTRA_JUNIT_CASE'],
            'suites': [{
                'name': 'suite1',
                'tags': [],
                'suites': [{
                    'name': 'suite2',
                     'tags': [],
                     'suites': [],
                     'tests': [{
                        'name': 'casea',
                        'tags': ['oxygen-junit-unknown-execution-time'],
                        'keywords': [{'name': 'casea (Execution)',
                                      'pass': True,
                                      'messages': [],
                                      'keywords': [],
                                      'elapsed': 0.0}]
                        }, {
                        'name': 'caseb',
                        'tags': ['oxygen-junit-unknown-execution-time'],
                        'keywords': [{
                            'name': 'caseb (Execution)',
                            'pass': True,
                            'messages': [],
                            'elapsed': 0.0,
                            'keywords': []
                        }]
                    }]
                }],
                'tests': [{
                    'name': 'case1',
                    'tags': ['oxygen-junit-unknown-execution-time'],
                    'keywords': [{
                        'name': 'case1 (Execution)',
                        'pass': True,
                        'messages': [],
                        'keywords': [],
                        'elapsed': 0.0
                    }]
                }, {
                    'name': 'case2',
                    'tags': ['oxygen-junit-unknown-execution-time'],
                    'keywords': [{
                        'name': 'case2 (Execution)',
                        'pass': False,
                        'messages': [
                            'ERROR: Example error message (the_error_type)'
                        ],
                        'keywords': [],
                        'elapsed': 0.0
                    }]
                }, {
                    'name': 'case3',
                    'tags': ['oxygen-junit-unknown-execution-time'],
                    'keywords': [{
                        'name': 'case3 (Execution)',
                        'pass': False,
                        'messages': [
                            'FAIL: Example failure message (the_failure_type)'
                        ],
                        'keywords': [],
                        'elapsed': 0.0
                    }]
                }]
            }],
        }
        xml = JUnitXml.fromfile(RESOURCES_PATH / 'junit.xml')
        retval = self.handler._transform_tests(xml)
        compare(retval, expected_output)
        self.assertTrue(validate_oxygen_suite(retval))
