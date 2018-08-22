from unittest import TestCase
from unittest.mock import patch

from oxygen import BaseHandler, OxygenLibrary

from ..helpers import get_config_as_file

class TestOxygenLibrary(TestCase):
    EXPECTED_KEYWORDS = ('run_junit', 'run_gatling', 'run_zap')
    def test_initialization(self):
        lib = OxygenLibrary()
        for kw in self.EXPECTED_KEYWORDS:
            self.assertIn(kw, lib.get_keyword_names())

    @patch('oxygen.config.CONFIG_FILE')
    def test_config_is_correct(self, mock_config):
        mock_config.return_value = get_config_as_file()
        lib = OxygenLibrary()
        self.assertGreater(len(lib._handlers), 1)
        for handler in lib._handlers.values():
            self.assertTrue(isinstance(handler, BaseHandler))
            self.assertTrue(any(hasattr(handler, kw)
                                for kw in self.EXPECTED_KEYWORDS),
                            'handler "{}" did not have any of the '
                            'following {}'.format(handler.__class__,
                                                  self.EXPECTED_KEYWORDS))

    def test_documentation(self):
        lib = OxygenLibrary()
        for kw in self.EXPECTED_KEYWORDS:
            self.assertNotNoneOrEmpty(lib.get_keyword_documentation(kw))
        # Libdoc specific values
        self.assertNotNoneOrEmpty(lib.get_keyword_documentation('__intro__'))
        self.assertNotNoneOrEmpty(lib.get_keyword_documentation('__init__'))

    def assertNotNoneOrEmpty(self, value):
        assert (value != None or value == '',
                'Value "{}" is None or empty'.format(value))


    def test_arguments(self):
        lib = OxygenLibrary()
        for kw in self.EXPECTED_KEYWORDS:
            args = lib.get_keyword_arguments(kw)
            self.assertIsInstance(args, list)
            self.assertGreater(len(args), 0)
