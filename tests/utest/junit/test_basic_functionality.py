from unittest import skip, TestCase
from unittest.mock import Mock, patch

from oxygen.junit import JUnitHandler
from oxygen.errors import JUnitHandlerException
from ..helpers import get_config

class JUnitBasicTests(TestCase):

    def setUp(self):
        self.handler = JUnitHandler(get_config()['oxygen.junit'])

    def test_initialization(self):
        self.assertEqual(self.handler.keyword, 'run_junit')
        self.assertEqual(self.handler._tags, ['JUNIT', 'EXTRA_JUNIT_CASE'])

    @patch('oxygen.junit.JUnitXml')
    @patch('oxygen.junit.JUnitHandler._transform_tests')
    def test_parsing(self, mock_transform, mock_junitxml):
        mock_junitxml.fromfile.return_value = 'some junit'
        self.handler.parse_results(('some/file/path.ext',))

        mock_junitxml.fromfile.assert_called_once_with('some/file/path.ext')
        mock_transform.assert_called_once_with('some junit')

    @patch('oxygen.utils.subprocess')
    def test_running(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)
        self.handler.run_junit('somefile', 'some', 'command')
        mock_subprocess.run.assert_called_once_with(('some', 'command'),
                                                    capture_output=True)

    @patch('oxygen.utils.subprocess')
    def test_running_fails_correctly(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=255)
        with self.assertRaises(JUnitHandlerException):
            self.handler.run_junit('somefile', 'some', 'command')

    @skip('Reminder to add tests once CLI interface exists')
    def test_cli(self):
        pass
