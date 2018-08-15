from unittest import TestCase
from unittest.mock import MagicMock

from oxygen.zap import ZAProxyHandler
from ..helpers import get_config


class TestParseZapInstance(TestCase):
    def setUp(self):
        self.object = ZAProxyHandler(get_config()['oxygen.zap'])
        self.object._parse_zap_site_dict = MagicMock(return_value=None)
        self.params = {}

    def test_has_defaults(self):
        return_dict = self.object._parse_zap_instance(self.params, True, True)
        expected_name = ('[Unknown HTTP Method] [Unknown Target URI]: '
                         '[Unknown Target Parameter]')
        assert('name' in return_dict)
        assert(return_dict['name'] == expected_name)

    def test_keepsparams(self):
        self.params = {
            'uri': 'foo',
            'method': 'bar',
            'param': 'baz',
        }
        return_dict = self.object._parse_zap_instance(self.params, True, True)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'bar foo: baz')

    def test_is_fail_if_risk_and_confident(self):
        return_dict = self.object._parse_zap_instance(self.params, True, True)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == False)

    def test_is_pass_if_risk_and_not_confident(self):
        return_dict = self.object._parse_zap_instance(self.params, True, False)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == True)

    def test_is_pass_if_not_risk_and_confident(self):
        return_dict = self.object._parse_zap_instance(self.params, False, True)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == True)

    def test_is_pass_if_not_risk_and_not_confident(self):
        return_dict = self.object._parse_zap_instance(
            self.params, False, False)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == True)
