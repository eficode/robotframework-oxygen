from unittest import TestCase
from unittest.mock import patch

from oxygen import BaseHandler, OxygenLibrary

from ..helpers import get_config_as_file

class TestOxygenLibrary(TestCase):
    def test_initialization(self):
        lib = OxygenLibrary()
        for kw in ('run_junit', 'run_gatling', 'run_zap'):
            self.assertIn(kw, lib.get_keyword_names())

    @patch('oxygen.config.CONFIG_FILE')
    def test_config_is_correct(self, mock_config):
        mock_config.return_value = get_config_as_file()
        lib = OxygenLibrary()
        self.assertGreater(len(lib._handlers), 1)
        for handler in lib._handlers.values():
            self.assertTrue(isinstance(handler, BaseHandler))
            self.assertTrue(any(hasattr(handler, kw)
                                for kw in lib.get_keyword_names()),
                            'handler "{}" did not have any of the '
                            'following {}'.format(handler.__class__,
                                                  lib.get_keyword_names()))
