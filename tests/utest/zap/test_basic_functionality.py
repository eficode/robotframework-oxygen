from unittest import skip, TestCase
from unittest.mock import Mock, mock_open, patch

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

    @patch('oxygen.utils.subprocess')
    def test_running_fails_correctly(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=-1)
        with self.assertRaises(ZAProxyHandlerException):
            self.handler.run_zap('somefile', 'some', 'command')

    @patch('oxygen.zap.ZAProxyHandler._read_results')
    @patch('oxygen.zap.ZAProxyHandler._parse_zap_dict')
    def test_parsing(self, mock_parse_zap_dict, mock_read_results):
        mock_read_results.return_value = {'hello': 'world'}
        mock_parse_zap_dict.return_value = {'goodbye': 'universe'}

        ret = self.handler.parse_results(('some file'), )

        mock_parse_zap_dict.assert_called_once_with({'hello': 'world'})
        self.assertEqual(ret, {'goodbye': 'universe'})


    def test_parsing_xml(self):
        with patch('builtins.open', mock_open(read_data='<xml />')) as f:
            ret = self.handler.parse_results(('somefile',))
        f.assert_called_once_with('somefile')
        self.assertNotNoneOrEmpty(ret['name'])
        self.assertEqual(ret['suites'], [])
        self.assertEqual(ret['tags'], ['ZAP'])

    def test_parsing_json(self):
        with patch('builtins.open',
                   mock_open(read_data='{"some": "json"}')) as f:
            ret = self.handler.parse_results(('somefile',))
        f.assert_called_once_with('somefile')
        self.assertNotNoneOrEmpty(ret['name'])
        self.assertEqual(ret['suites'], [])
        self.assertEqual(ret['tags'], ['ZAP'])

    def assertNotNoneOrEmpty(self, str_):
        return str_ is not None and str_ != ''

    @skip('Reminder to add tests once CLI interface exists')
    def test_cli(self):
        pass
