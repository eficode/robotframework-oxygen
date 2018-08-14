import unittest
from oxygen.zap import ZAProxyHandler
from unittest.mock import MagicMock
from yaml import load

class TestParseZapDict(unittest.TestCase):
    def setUp(self):
        with open('../config.yml', 'r') as infile:
            self._config = load(infile)
            self._object = ZAProxyHandler(self._config['oxygen.zap'])

        self._params = {
            'version': None,
            'generated': None,
            'site': [True, False],
        }

        self._parser = MagicMock(return_value=None)
        self._object._parse_zap_site_dict = self._parser


    def tearDown(self):
        pass


    def test_has_defaults(self):
        return_dict = self._object._parse_zap_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'Oxygen ZAProxy Report (Unknown ZAProxy Version, Unknown ZAProxy Run Time)')


    def test_keeps_params(self):
        self._params['version'] = 'my version'
        self._params['generated'] = 'when'

        return_dict = self._object._parse_zap_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'Oxygen ZAProxy Report (my version, when)')


    def test_handles_odd_params(self):
        self._params['@version'] = 'my version'
        self._params['@generated'] = 'when'

        return_dict = self._object._parse_zap_dict(self._params)
        assert('name' in return_dict)
        assert(return_dict['name'] == 'Oxygen ZAProxy Report (my version, when)')


    def test_calls_down(self):
        return_dict = self._object._parse_zap_dict(self._params)
        self._parser.assert_any_call(True)
        self._parser.assert_any_call(False)
        assert(self._parser.call_count == 2)


    if __name__ == '__main__':
        unittest.main()
