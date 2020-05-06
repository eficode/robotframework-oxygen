from pathlib import Path
from unittest import skip, TestCase
from unittest.mock import create_autospec, Mock, mock_open, patch

from oxygen.base_handler import BaseHandler
from oxygen.zap import ZAProxyHandler
from oxygen.errors import ZAProxyHandlerException
from ..helpers import get_config

class ZAPBasicTests(TestCase):
    def setUp(self):
        self.handler = ZAProxyHandler(get_config()['oxygen.zap'])

    def test_initialization(self):
        self.assertEqual(self.handler.keyword, 'run_zap')
        self.assertEqual(self.handler._tags, ['ZAP'])

    @patch('oxygen.utils.subprocess')
    def test_running(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)
        self.handler.run_zap('somefile', 'some', 'command')
        mock_subprocess.run.assert_called_once_with(('some', 'command'),
                                                    capture_output=True)

    @patch('oxygen.zap.validate_path')
    @patch('oxygen.utils.subprocess')
    def test_running_fails_correctly(self, mock_subprocess, _):
        mock_subprocess.run.return_value = Mock(returncode=-1)
        with self.assertRaises(ZAProxyHandlerException):
            self.handler.run_zap('somefile', 'some', 'command')

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
            ret = self.handler.parse_results('somefile')
        mock_validate_path.assert_called_once_with('somefile')
        f.assert_called_once_with(m.resolve())
        self.assertNotNoneOrEmpty(ret['name'])
        self.assertEqual(ret['suites'], [])
        self.assertEqual(ret['tags'], ['ZAP'])

    def assertNotNoneOrEmpty(self, str_):
        return str_ is not None and str_ != ''

    def test_cli(self):
        self.assertEqual(self.handler.cli(), BaseHandler.DEFAULT_CLI)
