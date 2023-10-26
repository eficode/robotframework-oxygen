from pathlib import Path
from unittest import skip, TestCase
from unittest.mock import ANY, create_autospec, Mock, patch

from testfixtures import compare

from oxygen.base_handler import BaseHandler
from oxygen.gatling import GatlingHandler
from oxygen.errors import GatlingHandlerException
from oxygen.oxygen_handler_result import validate_oxygen_suite
from ..helpers import (example_robot_output,
                       GATLING_EXPECTED_OUTPUT,
                       get_config,
                       RESOURCES_PATH)

class GatlingBasicTests(TestCase):

    def setUp(self):
        self.handler = GatlingHandler(get_config()['oxygen.gatling'])

    def test_initialization(self):
        self.assertEqual(self.handler.keyword, 'run_gatling')
        self.assertEqual(self.handler._tags, ['GATLING'])

    @patch('oxygen.gatling.GatlingHandler._transform_tests')
    @patch('oxygen.gatling.validate_path')
    def test_parsing(self, mock_validate_path, mock_transform):
        m = create_autospec(Path)
        mock_validate_path.return_value = m
        self.handler.parse_results('some/file/path.ext')
        mock_validate_path.assert_called_once_with('some/file/path.ext')
        mock_transform.assert_called_once_with(m.resolve())

    @patch('oxygen.utils.subprocess')
    def test_running(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)
        self.handler.run_gatling('somefile', 'some command')
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
        self.handler.run_gatling('somefile', 'some command', ENV_VAR='hello')
        mock_subprocess.run.assert_called_once_with('some command',
                                                    capture_output=True,
                                                    shell=True,
                                                    env=ANY)
        passed_full_env = mock_subprocess.run.call_args[-1]['env']
        self.assertTrue(self.subdict_in_parent_dict(passed_full_env,
                                                    {'ENV_VAR': 'hello'}))

    @patch('oxygen.utils.subprocess')
    def test_running_fails_correctly(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=255)
        with self.assertRaises(GatlingHandlerException):
            self.handler.run_gatling('somefile',
                                     'some command',
                                     check_return_code=True)

    @patch('oxygen.utils.subprocess')
    def test_running_does_not_fail_by_default(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=255)
        retval = self.handler.run_gatling('somefile', 'some command')
        self.assertEqual(retval, 'somefile')

    def test_cli(self):
        self.assertEqual(self.handler.cli(), BaseHandler.DEFAULT_CLI)

    @patch('oxygen.gatling.GatlingHandler._report_oxygen_run')
    def test_check_for_keyword(self, mock_report):
        fake_test = example_robot_output().suite.suites[0].tests[2]
        expected_data = {'Atest.Test.My Second Test': 'somefile.lol'}

        self.handler.check_for_keyword(fake_test, expected_data)

        self.assertEqual(mock_report.call_args[0][0].name,
                         'oxygen.OxygenLibrary.Run Gatling')
        self.assertEqual(self.handler.run_time_data, 'somefile.lol')

    def test_gatling_parsing(self):
        example_file = RESOURCES_PATH / 'gatling-example-simulation.log'
        retval = self.handler._transform_tests(example_file)
        compare(retval, GATLING_EXPECTED_OUTPUT)
        self.assertTrue(validate_oxygen_suite(retval))
