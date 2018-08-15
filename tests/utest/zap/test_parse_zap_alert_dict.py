from unittest import TestCase
from unittest.mock import MagicMock

from oxygen.zap import ZAProxyHandler
from ..helpers import get_config


class TestParseZapAlertDict(TestCase):
    def setUp(self):
        self.object = ZAProxyHandler(get_config()['oxygen.zap'])
        self._params = {
            'instances': [True, False],
        }
        self.parser_mock = MagicMock(return_value=None)
        self.object._parse_zap_instance = self.parser_mock

    def test_has_defaults(self):
        return_dict = self.object._parse_zap_alert_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == '[Unknown Plugin ID] Unknown Alert Name')

    def test_keeps_params(self):
        self._params['pluginid'] = 'my plugin'
        self._params['name'] = 'my name'
        return_dict = self.object._parse_zap_alert_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'my plugin my name')

    def test_passes_down(self):
        return_dict = self.object._parse_zap_alert_dict(self._params)
        self.parser_mock.assert_any_call(True, True, True)
        self.parser_mock.assert_any_call(False, True, True)
        assert(self.parser_mock.call_count == 2)
