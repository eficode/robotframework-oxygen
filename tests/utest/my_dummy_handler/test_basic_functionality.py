import sys
from unittest import TestCase
from oxygen.errors import MismatchArgumentException
from ..helpers import RESOURCES_PATH, get_config, example_robot_output

sys.path.append(str(RESOURCES_PATH / 'my_dummy_handlers'))

from dummy_handler_single_arg import (
    MyDummyHandler as DummyHandlerSingleArg,
)
from dummy_handler_multiple_args import (
    MyDummyHandler as DummyHandlerMultipleArgs,
)
from dummy_handler_multiple_args_too_few import (
    MyDummyHandler as DummyHandlerMultipleArgsTooFew,
)
from dummy_handler_default_params import (
    MyDummyHandler as DummyHandlerDefaultParams,
)


class DummyHandlerSingleArgTests(TestCase):
    '''
    A test for passing tuple if parse_results accepts one parameter
    '''

    def setUp(self):
        self.handler = DummyHandlerSingleArg(
            get_config()['oxygen.my_dummy_handler']
        )

    def test_run_my_dummy_handler(self):
        return_value = self.handler.run_my_dummy_handler('/some/path/to.ext')
        self.assertTupleEqual(return_value, ('/some/path/to.ext', 'foo'))

    def test_parse_results(self):
        fake_test = example_robot_output().suite.suites[0].tests[6]
        expected_data = {'Atest.Test.My Fifth Test': '/some/path/to.ext'}

        self.handler.check_for_keyword(fake_test, expected_data)

        self.assertEqual(self.handler.run_time_data, '/some/path/to.ext')


class DummyHandlerMultipleArgsTests(TestCase):
    '''
    A test for unfolding parse_results arguments
    if it has multiple parameters
    '''

    def setUp(self):
        self.handler = DummyHandlerMultipleArgs(
            get_config()['oxygen.my_dummy_handler']
        )

    def test_parse_results(self):
        fake_test = example_robot_output().suite.suites[0].tests[6]
        expected_data = {
            'Atest.Test.My Fifth Test': ('/some/path/to.ext', 'foo')
        }

        self.handler.check_for_keyword(fake_test, expected_data)

        self.assertEqual(
            self.handler.run_time_data, ('/some/path/to.ext', 'foo')
        )


class DummyHandlerMultipleArgsTooFewTests(TestCase):
    '''
    A test for testing if it throws mismatch argument exception because
    parse_results expects too many arguments
    '''

    def setUp(self):
        self.handler = DummyHandlerMultipleArgsTooFew(
            get_config()['oxygen.my_dummy_handler']
        )

    def test_parse_results(self):
        fake_test = example_robot_output().suite.suites[0].tests[6]
        expected_data = {
            'Atest.Test.My Fifth Test': ('/some/path/to.ext', 'foo')
        }

        self.assertRaises(
            MismatchArgumentException,
            self.handler.check_for_keyword,
            fake_test,
            expected_data,
        )


class DummyHandlerMultipleArgsSingleTests(TestCase):
    '''
    A test for testing if it throws mismatch argument exception because
    parse_results expects multiple arguments but we do not pass multiple
    '''

    def setUp(self):
        self.handler = DummyHandlerMultipleArgsTooFew(
            get_config()['oxygen.my_dummy_handler']
        )

    def test_parse_results(self):
        fake_test = example_robot_output().suite.suites[0].tests[6]
        expected_data = {'Atest.Test.My Fifth Test': 'some/path/to.ext'}

        self.assertRaises(
            MismatchArgumentException,
            self.handler.check_for_keyword,
            fake_test,
            expected_data,
        )


class DummyHandlerDefaultParamsTests(TestCase):
    '''
    A test for testing arguments with defaults
    '''

    def setUp(self):
        self.handler = DummyHandlerDefaultParams(
            get_config()['oxygen.my_dummy_handler']
        )

    def test_parse_results_with_one(self):
        fake_test = example_robot_output().suite.suites[0].tests[6]
        expected_data = {'Atest.Test.My Fifth Test': 'some/path/to.ext'}
        self.handler.check_for_keyword(fake_test, expected_data)
        self.assertEqual(self.handler.run_time_data, 'some/path/to.ext')

    def test_parse_results_with_multiple(self):
        fake_test = example_robot_output().suite.suites[0].tests[6]
        expected_data = {
            'Atest.Test.My Fifth Test': ('some/path/to.ext', 'foo')}
        self.handler.check_for_keyword(fake_test, expected_data)
        self.assertTupleEqual(
            self.handler.run_time_data, ('some/path/to.ext', 'foo'))

    def test_parse_results_with_too_many(self):
        fake_test = example_robot_output().suite.suites[0].tests[6]
        expected_data = {
            'Atest.Test.My Fifth Test': ('some/path/to.ext', 'foo', 'bar')}
        self.assertRaises(
            MismatchArgumentException,
            self.handler.check_for_keyword,
            fake_test,
            expected_data,
        )
