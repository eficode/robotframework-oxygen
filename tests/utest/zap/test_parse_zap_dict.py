from unittest import TestCase
from unittest.mock import MagicMock

from oxygen.zap import ZAProxyHandler
from ..helpers import get_config


class TestParseZapDict(TestCase):
    def setUp(self):
        self.object = ZAProxyHandler(get_config()['oxygen.zap'])
        self.params = {
            'version': None,
            'generated': None,
            'site': [True, False],
        }
        self.parser_mock = MagicMock(return_value=None)
        self.object._parse_zap_site_dict = self.parser_mock

    def test_has_defaults(self):
        return_dict = self.object._parse_zap_dict(self.params)
        expected_name = ('Oxygen ZAProxy Report (Unknown ZAProxy Version, '
                         'Unknown ZAProxy Run Time)')
        assert('name' in return_dict)
        assert(return_dict['name'] == expected_name)

    def test_keepsparams(self):
        self.params['version'] = 'my version'
        self.params['generated'] = 'when'
        return_dict = self.object._parse_zap_dict(self.params)
        assert('name' in return_dict)
        assert(return_dict['name'] == ('Oxygen ZAProxy Report '
                                       '(my version, when)'))

    def test_handles_oddparams(self):
        self.params['@version'] = 'my version'
        self.params['@generated'] = 'when'
        return_dict = self.object._parse_zap_dict(self.params)
        assert('name' in return_dict)
        assert(return_dict['name'] == ('Oxygen ZAProxy Report '
                                       '(my version, when)'))

    def test_calls_down(self):
        return_dict = self.object._parse_zap_dict(self.params)
        self.parser_mock.assert_any_call(True)
        self.parser_mock.assert_any_call(False)
        assert(self.parser_mock.call_count == 2)
