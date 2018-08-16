from unittest import skip, TestCase
from unittest.mock import patch

from oxygen.gatling import GatlingHandler
from ..helpers import get_config

class JUnitBasicTests(TestCase):

    def setUp(self):
        self.lib = GatlingHandler(get_config()['oxygen.gatling'])

    def test_initialization(self):
        self.assertEqual(self.lib.get_keyword(), 'run_gatling')
        self.assertEqual(self.lib._tags, ['GATLING'])

    @patch('oxygen.gatling.GatlingHandler._transform_tests')
    def test_parsing(self, mock_transform):
        self.lib._parse_results(['some/file/path.ext'])
        mock_transform.assert_called_once_with('some/file/path.ext')


    @patch('oxygen.gatling.subprocess.call')
    @patch('oxygen.gatling.GatlingHandler._transform_tests')
    def test_running(self, mock_transform, mock_subprocess):
        self.lib._parse_results(['doesentmatter', 'some', 'command'])

        mock_subprocess.assert_called_once_with(['some', 'command'])
        mock_transform.assert_called_once_with('doesentmatter')

    @skip('Reminder to add tests once CLI interface exists')
    def test_cli(self):
        pass
