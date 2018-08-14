import unittest
from oxygen.zap import ZAProxyHandler
from unittest.mock import MagicMock
from yaml import load

class TestParseZapInstance(unittest.TestCase):
    def setUp(self):
        with open('../config.yml', 'r') as infile:
            self._config = load(infile)
            self._object = ZAProxyHandler(self._config['oxygen.zap'])

        self._params = {}

        self._parser = MagicMock(return_value=None)
        self._object._parse_zap_site_dict = self._parser


    def tearDown(self):
        pass


    def test_has_defaults(self):
        return_dict = self._object._parse_zap_instance(self._params, True, True)
        assert('name' in return_dict)
        assert(return_dict['name'] == '[Unknown HTTP Method] [Unknown Target URI]: [Unknown Target Parameter]')


    def test_keeps_params(self):
        self._params = {
            'uri': 'foo',
            'method': 'bar',
            'param': 'baz',
        }

        return_dict = self._object._parse_zap_instance(self._params, True, True)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'bar foo: baz')


    def test_is_fail_if_risk_and_confident(self):
        return_dict = self._object._parse_zap_instance(self._params, True, True)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == False)


    def test_is_pass_if_risk_and_not_confident(self):
        return_dict = self._object._parse_zap_instance(self._params, True, False)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == True)


    def test_is_pass_if_not_risk_and_confident(self):
        return_dict = self._object._parse_zap_instance(self._params, False, True)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == True)


    def test_is_pass_if_not_risk_and_not_confident(self):
        return_dict = self._object._parse_zap_instance(self._params, False, False)
        assert('pass' in return_dict)
        assert(return_dict['pass'] == True)


    if __name__ == '__main__':
        unittest.main()
