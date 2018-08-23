from unittest import skip, TestCase
from unittest.mock import Mock, patch

from oxygen.gatling import GatlingHandler
from oxygen.errors import GatlingHandlerException
from ..helpers import get_config

class JUnitBasicTests(TestCase):

    def setUp(self):
        self.handler = GatlingHandler(get_config()['oxygen.gatling'])

    def test_initialization(self):
        self.assertEqual(self.handler.keyword, 'run_gatling')
        self.assertEqual(self.handler._tags, ['GATLING'])

    @patch('oxygen.gatling.GatlingHandler._transform_tests')
    def test_parsing(self, mock_transform):
        self.handler.parse_results(('some/file/path.ext',))
        mock_transform.assert_called_once_with('some/file/path.ext')


    @patch('oxygen.utils.subprocess')
    def test_running(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=0)
        self.handler.run_gatling('somefile', 'some', 'command')
        mock_subprocess.run.assert_called_once_with(('some', 'command'),
                                                    capture_output=True)

    @patch('oxygen.utils.subprocess')
    def test_running_fails_correctly(self, mock_subprocess):
        mock_subprocess.run.return_value = Mock(returncode=255)
        with self.assertRaises(GatlingHandlerException):
            self.handler.run_gatling('somefile', 'some', 'command')

    @skip('Reminder to add tests once CLI interface exists')
    def test_cli(self):
        pass
