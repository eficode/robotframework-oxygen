import unittest
from oxygen.zap import ZAProxyHandler
from unittest.mock import MagicMock
from yaml import load

class TestParseZapAlertDict(unittest.TestCase):
    def setUp(self):
        with open('../config.yml', 'r') as infile:
            self._config = load(infile)
            self._object = ZAProxyHandler(self._config['oxygen.zap'])

        self._params = {
            'instances': [True, False],
        }

        self._parser = MagicMock(return_value=None)
        self._object._parse_zap_instance = self._parser


    def tearDown(self):
        pass


    def test_has_defaults(self):
        return_dict = self._object._parse_zap_alert_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == '[Unknown Plugin ID] Unknown Alert Name')


    def test_keeps_params(self):
        self._params['pluginid'] = 'my plugin'
        self._params['name'] = 'my name'

        return_dict = self._object._parse_zap_alert_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'my plugin my name')


    def test_passes_down(self):
        return_dict = self._object._parse_zap_alert_dict(self._params)
        self._parser.assert_any_call(True, True, True)
        self._parser.assert_any_call(False, True, True)
        assert(self._parser.call_count == 2)


    if __name__ == '__main__':
        unittest.main()
