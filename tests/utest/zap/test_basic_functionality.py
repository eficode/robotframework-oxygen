from pathlib import Path
from unittest import TestCase
from unittest.mock import ANY, create_autospec, Mock, mock_open, patch

from testfixtures import compare

from oxygen.errors import ZAProxyHandlerException
from oxygen.oxygen_handler_result import validate_oxygen_suite
from oxygen.zap import ZAProxyHandler

from ..helpers import (example_robot_output,
                       get_config,
                       RESOURCES_PATH,
                       suppress_stdout)

ZAP_EXPECTED_OUTPUT = {
 'name': 'Oxygen ZAProxy Report (2.7.0, Tue, 7 Aug 2018 13:17:56)',
 'suites': [{'name': 'Site: http://192.168.50.56:7272', 'tests': []},
            {'name': 'Site: http://localhost:7272',
             'tests': [{'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: <input '
                                                   'id="password_field" '
                                                   'size="30" '
                                                   'type="password">'],
                                      'name': 'GET http://localhost:7272/: '
                                              'password_field',
                                      'pass': True}],
                        'name': '10012 Password Autocomplete in Browser',
                        'tags': []},
                       {'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://localhost:7272/: '
                                              'X-Frame-Options',
                                      'pass': False}],
                        'name': '10020 X-Frame-Options Header Not Set',
                        'tags': []},
                       {'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://localhost:7272/: '
                                              'X-XSS-Protection',
                                      'pass': True}],
                        'name': '10016 Web Browser XSS Protection Not Enabled',
                        'tags': []},
                       {'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://localhost:7272/: '
                                              'X-Content-Type-Options',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://localhost:7272/demo.css: '
                                              'X-Content-Type-Options',
                                      'pass': True}],
                        'name': '10021 X-Content-Type-Options Header Missing',
                        'tags': []}]},
            {'name': 'Site: http://127.0.0.1:7272',
             'tests': [{'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/demo.css: '
                                              'X-Content-Type-Options',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/welcome.html: '
                                              'X-Content-Type-Options',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://127.0.0.1:7272/: '
                                              'X-Content-Type-Options',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/error.html: '
                                              'X-Content-Type-Options',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://127.0.0.1:7272: '
                                              'X-Content-Type-Options',
                                      'pass': True}],
                        'name': '10021 X-Content-Type-Options Header Missing',
                        'tags': []},
                       {'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/favicon.ico: '
                                              'X-XSS-Protection',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://127.0.0.1:7272/: '
                                              'X-XSS-Protection',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://127.0.0.1:7272: '
                                              'X-XSS-Protection',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/sitemap.xml: '
                                              'X-XSS-Protection',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/welcome.html: '
                                              'X-XSS-Protection',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/error.html: '
                                              'X-XSS-Protection',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/robots.txt: '
                                              'X-XSS-Protection',
                                      'pass': True}],
                        'name': '10016 Web Browser XSS Protection Not Enabled',
                        'tags': []},
                       {'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://127.0.0.1:7272/: '
                                              'X-Frame-Options',
                                      'pass': False},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET http://127.0.0.1:7272: '
                                              'X-Frame-Options',
                                      'pass': False},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/welcome.html: '
                                              'X-Frame-Options',
                                      'pass': False},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://127.0.0.1:7272/error.html: '
                                              'X-Frame-Options',
                                      'pass': False}],
                        'name': '10020 X-Frame-Options Header Not Set',
                        'tags': []},
                       {'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: <input '
                                                   'id="password_field" '
                                                   'size="30" '
                                                   'type="password">'],
                                      'name': 'GET http://127.0.0.1:7272: '
                                              'password_field',
                                      'pass': True},
                                     {'elapsed': 0.0,
                                      'messages': ['Evidence: <input '
                                                   'id="password_field" '
                                                   'size="30" '
                                                   'type="password">'],
                                      'name': 'GET http://127.0.0.1:7272/: '
                                              'password_field',
                                      'pass': True}],
                        'name': '10012 Password Autocomplete in Browser',
                        'tags': []}]},
            {'name': 'Site: http://detectportal.firefox.com',
             'tests': [{'keywords': [{'elapsed': 0.0,
                                      'messages': ['Evidence: [No Evidence '
                                                   'Provided]'],
                                      'name': 'GET '
                                              'http://detectportal.firefox.com/success.txt: '
                                              'X-Content-Type-Options',
                                      'pass': True}],
                        'name': '10021 X-Content-Type-Options Header Missing',
                        'tags': []}]}],
 'tags': ['ZAP']}

class ZAPBasicTests(TestCase):
    def setUp(self):
        self.handler = ZAProxyHandler(get_config()['oxygen.zap'])

    def test_initialization(self):
        self.assertEqual(self.handler.keyword, 'run_zap')
        self.assertEqual(self.handler._tags, ['ZAP'])

    @patch('oxygen.utils.subprocess')
    def test_running(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)
        self.handler.run_zap('somefile', 'some command')
        mock_subprocess.run.assert_called_once_with('some command',
                                                    capture_output=True,
                                                    shell=True,
                                                    env=ANY)

    def subdict_in_parent_dict(self, parent_dict, subdict):
        return all(
            subitem in parent_dict.items() for subitem in subdict.items())

    @patch('oxygen.utils.subprocess')
    def test_running_with_passing_environment_values(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)

        self.handler.run_zap('somefile', 'some command', ENV_VAR='value')

        mock_subprocess.run.assert_called_once_with('some command',
                                                    capture_output=True,
                                                    shell=True,
                                                    env=ANY)
        passed_full_env = mock_subprocess.run.call_args[-1]['env']
        self.assertTrue(self.subdict_in_parent_dict(passed_full_env,
                                                    {'ENV_VAR': 'value'}))

    @patch('oxygen.utils.subprocess')
    def test_running_fails_correctly(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=-1)
        with self.assertRaises(ZAProxyHandlerException):
            self.handler.run_zap('somefile',
                                 'some command',
                                 check_return_code=True)

    @patch('oxygen.utils.subprocess')
    def test_running_does_not_fail_by_default(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=-1)
        retval = self.handler.run_zap('somefile', 'some command')
        self.assertEqual(retval, 'somefile')

    @patch('oxygen.zap.ZAProxyHandler._read_results')
    @patch('oxygen.zap.ZAProxyHandler._parse_zap_dict')
    @patch('oxygen.zap.validate_path')
    def test_parsing(self,
                     mock_validate_path,
                     mock_parse_zap_dict,
                     mock_read_results):
        m = create_autospec(Path)
        mock_validate_path.return_value = m
        mock_read_results.return_value = {'hello': 'world'}
        mock_parse_zap_dict.return_value = {'goodbye': 'universe'}

        ret = self.handler.parse_results('some file')

        mock_validate_path.assert_called_once_with('some file')
        mock_parse_zap_dict.assert_called_once_with({'hello': 'world'})
        self.assertEqual(ret, {'goodbye': 'universe'})


    def test_parsing_xml(self):
        with patch('builtins.open', mock_open(read_data='<xml />')) as f, \
            patch('oxygen.zap.validate_path') as mock_validate_path:
            m = create_autospec(Path)
            mock_validate_path.return_value = m
            ret = self.handler.parse_results('somefile')
        mock_validate_path.assert_called_once_with('somefile')
        f.assert_called_once_with(m.resolve())
        self.assertNotNoneOrEmpty(ret['name'])
        self.assertEqual(ret['suites'], [])
        self.assertEqual(ret['tags'], ['ZAP'])

    def test_parsing_json(self):
        with patch('builtins.open',
                   mock_open(read_data='{"some": "json"}')) as f, \
            patch('oxygen.zap.validate_path') as mock_validate_path:

            m = create_autospec(Path)
            mock_validate_path.return_value = m

            with suppress_stdout():
                ret = self.handler.parse_results('somefile')
        mock_validate_path.assert_called_once_with('somefile')
        f.assert_called_once_with(m.resolve())
        self.assertNotNoneOrEmpty(ret['name'])
        self.assertEqual(ret['suites'], [])
        self.assertEqual(ret['tags'], ['ZAP'])

    def assertNotNoneOrEmpty(self, str_):
        return str_ is not None and str_ != ''

    @patch('oxygen.zap.ZAProxyHandler._report_oxygen_run')
    def test_check_for_keyword(self, mock_report):
        fake_test = example_robot_output().suite.suites[0].tests[4]
        expected_data = {'Atest.Test.My Three Point Fifth Test': 'afile.ext'}

        self.handler.check_for_keyword(fake_test, expected_data)

        self.assertEqual(mock_report.call_args[0][0].name,
                         'oxygen.OxygenLibrary.Run Zap')
        self.assertEqual(self.handler.run_time_data, 'afile.ext')

    def test_zap_parsing(self):
        retval = self.handler.parse_results(RESOURCES_PATH / 'zap' / 'zap.xml')
        compare(retval, ZAP_EXPECTED_OUTPUT)
        self.assertTrue(validate_oxygen_suite(retval))
