from unittest import TestCase
from unittest.mock import patch, Mock

from oxygen import BaseHandler, OxygenLibrary
from oxygen.errors import OxygenException

from ..helpers import get_config_as_file

class TestOxygenLibrary(TestCase):
    EXPECTED_KEYWORDS = ('run_junit', 'run_gatling', 'run_zap')

    def setUp(self):
        self.lib = OxygenLibrary()


    def test_initialization(self):
        for kw in self.EXPECTED_KEYWORDS:
            self.assertIn(kw, self.lib.get_keyword_names())

    @patch('oxygen.config.CONFIG_FILE')
    def test_config_is_correct(self, mock_config):
        mock_config.return_value = get_config_as_file()

        self.assertGreater(len(self.lib.handlers), 1)
        for handler in self.lib.handlers.values():
            self.assertTrue(isinstance(handler, BaseHandler))
            self.assertTrue(any(hasattr(handler, kw)
                                for kw in self.EXPECTED_KEYWORDS),
                            'handler "{}" did not have any of the '
                            'following {}'.format(handler.__class__,
                                                  self.EXPECTED_KEYWORDS))

    def test_documentation(self):
        for kw in self.EXPECTED_KEYWORDS:
            self.assertNotNoneOrEmpty(self.lib.get_keyword_documentation(kw))
        # Libdoc specific values
        self.assertNotNoneOrEmpty(self.lib.get_keyword_documentation('__intro__'))

    def assertNotNoneOrEmpty(self, value):
        assert value != None or value == '', \
               'Value "{}" is None or empty'.format(value)

    def test_arguments(self):
        for kw in self.EXPECTED_KEYWORDS:
            args = self.lib.get_keyword_arguments(kw)
            self.assertIsInstance(args, list)
            self.assertGreater(len(args), 0)

    @patch('oxygen.OxygenLibrary._fetch_handler')
    def test_run_keyword(self, mock_fetch_handler):
        expected_data = {f'{attr}.return_value': 'somefile.ext'
                         for attr in self.EXPECTED_KEYWORDS}
        m = Mock()
        m.configure_mock(**expected_data)
        mock_fetch_handler.side_effect = [m]*3

        for kw in self.EXPECTED_KEYWORDS:
            ret = self.lib.run_keyword(kw, ['somefile.ext'], {})
            self.assertEqual(ret, 'somefile.ext')
            self.assertNotNoneOrEmpty(self.lib.data)

    def test_run_keyword_should_fail_if_nonexistent_kw_is_called(self):
        with self.assertRaises(OxygenException) as ex:
            self.lib.run_keyword('nonexistent', [], {})

        self.assertIn('No handler for keyword', str(ex.exception))
