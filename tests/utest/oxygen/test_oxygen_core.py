from unittest import TestCase
from oxygen.oxygen import OxygenCore


class TestOxygenInitialization(TestCase):
    def test_oxygen_core_initializes_without_loading_config(self):
        '''
        OxygenCore and all it's subclasses lazy-load the configuration and,
        consequently, the handlers. This test makes sure that is not
        accidentally changed at some point
        '''
        core = OxygenCore()
        self.assertEqual(core._config, None)
        self.assertEqual(core._handlers, None)

