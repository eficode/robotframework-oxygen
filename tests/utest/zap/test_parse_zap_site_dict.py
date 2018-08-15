from unittest import TestCase
from unittest.mock import MagicMock

from oxygen.zap import ZAProxyHandler
from ..helpers import get_config


class TestParseZapSiteDict(TestCase):
    def setUp(self):
        self.object = ZAProxyHandler(get_config()['oxygen.zap'])
        self._params = {
            'alerts': [True, False],
        }
        self._parser = MagicMock(return_value=None)
        self.object._parse_zap_alert_dict = self._parser

    def test_has_defaults(self):
        return_dict = self.object._parse_zap_site_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'Site: Unknown Site Name')
        assert('tests' in return_dict)
        self._parser.assert_any_call(True)
        self._parser.assert_any_call(False)
        assert(self._parser.call_count == 2)

    def test_reads_prefixed(self):
        self._params['@name'] = 'My Site Name'
        return_dict = self.object._parse_zap_site_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'Site: My Site Name')
        assert('tests' in return_dict)
        self._parser.assert_any_call(True)
        self._parser.assert_any_call(False)
        assert(self._parser.call_count == 2)
