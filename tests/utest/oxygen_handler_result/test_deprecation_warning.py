'''
Currently, the introduction of pydantic[1] to validate result dictionaries that
handlers return is planned to just raise a deprecation warning.

After 1.0 -- ie. a backwards-incompatible release -- we should turn deprecation
warning to actually start failing. See issue [2].

[1| https://github.com/eficode/robotframework-oxygen/issues/43
[2] https://github.com/eficode/robotframework-oxygen/issues/45
'''
from unittest import TestCase
from unittest.mock import patch
from oxygen.base_handler import BaseHandler
from oxygen.oxygen import OxygenCLI

from ..helpers import get_config, MINIMAL_SUITE_DICT

class TestDeprecationWarningWhenValidating(TestCase):
    def setUp(self):
        self.cli = OxygenCLI()

    def test_warning_about_invalid_result(self):
        handler = BaseHandler(get_config()['oxygen.junit'])

        with self.assertWarns(UserWarning) as warning:
            handler._validate({})

        warning_message = str(warning.warning)
        self.assertIn('oxygen.base_handler', warning_message)
        self.assertIn('validation error for typed-dict', warning_message)
        self.assertIn('In Oxygen 1.0, handlers will'
                      ' need to produce valid results.', warning_message)

    @patch('oxygen.oxygen.RobotInterface')
    def test_warning_about_invalid_result_in_CLI(self, mock_iface):
        with self.assertWarns(UserWarning) as warning:
            self.cli.convert_to_robot_result({
                'result_file': 'doesentmatter',
                'func': lambda **_: {**MINIMAL_SUITE_DICT, 'setup': []}
            })

            mock_iface.assert_any_call()

    def test_deprecation_was_removed(self):
        '''Remove this test once deprecation warning has been removed'''
        if self.cli.__version__.startswith('1'):
            self.fail('Deprecation warning should have been removed in 1.0')
