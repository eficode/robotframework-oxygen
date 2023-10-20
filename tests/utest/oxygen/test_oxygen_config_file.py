from unittest import TestCase

from oxygen.config import CONFIG_FILE, ORIGINAL_CONFIG_FILE

class TestOxygenCLIEntryPoints(TestCase):
    def test_config_and_config_original_match(self):
        with open(CONFIG_FILE, 'r') as config:
            with open(ORIGINAL_CONFIG_FILE, 'r') as original_config:
                self.assertEqual(config.read(), original_config.read())
