from unittest import skip, TestCase
from unittest.mock import patch

from oxygen.junit import JUnitHandler
from ..helpers import get_config

class JUnitBasicTests(TestCase):

    def setUp(self):
        self.lib = JUnitHandler(get_config()['oxygen.junit'])

    def test_initialization(self):
        self.assertEqual(self.lib.get_keyword(), 'run_junit')
        self.assertEqual(self.lib._tags, ['JUNIT', 'EXTRA_JUNIT_CASE'])

    @patch('oxygen.junit.JUnitXml')
    @patch('oxygen.junit.JUnitHandler._transform_tests')
    def test_parsing(self, mock_transform, mock_junitxml):
        mock_junitxml.fromfile.return_value = 'some junit'


        self.lib._parse_results(['some/file/path.ext'])

        mock_junitxml.fromfile.assert_called_once_with('some/file/path.ext')
        mock_transform.assert_called_once_with('some junit')

    @patch('oxygen.junit.subprocess.call')
    @patch('oxygen.junit.JUnitXml')
    def test_running(self, mock_junitxml, mock_subprocess):
        self.lib._parse_results(['doesentmatter', 'some', 'command'])

        mock_subprocess.assert_called_once_with(['some', 'command'])
        mock_junitxml.fromfile.assert_called_once_with('doesentmatter')

    @skip('Reminder to add tests once CLI interface exists')
    def test_cli(self):
        pass
