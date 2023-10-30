from unittest import TestCase

from oxygen.errors import InvalidOxygenResultException
from oxygen.oxygen_handler_result import OxygenSuiteDict, validate_oxygen_suite

from ..helpers import (MINIMAL_TC_DICT,
                       MINIMAL_SUITE_DICT,
                       _ListSubclass,
                       _StrSubclass,
                       _TCSubclass)
from .shared_tests import (SharedTestsForName,
                           SharedTestsForKeywordField,
                           SharedTestsForTags)

class TestOxygenSuiteDict(TestCase,
                          SharedTestsForName,
                          SharedTestsForKeywordField,
                          SharedTestsForTags):
    def setUp(self):
        self.minimal = MINIMAL_SUITE_DICT

    def test_validate_oxygen_suite_validates_correctly(self):
        with self.assertRaises(InvalidOxygenResultException):
            validate_oxygen_suite({})

    def test_validate_oxygen_suite_with_minimal_valid(self):
        expected = {
            'name': 'My Suite'
        }

        self.assertEqual(validate_oxygen_suite(expected), expected)
        self.assertEqual(validate_oxygen_suite(self.minimal), self.minimal)

    def valid_inputs_for(self, attribute, *valid_inputs):
        for valid_input in valid_inputs:
            self.assertTrue(validate_oxygen_suite({**self.minimal,
                                                   attribute: valid_input}))

    def invalid_inputs_for(self, attribute, *invalid_inputs):
        for invalid_input in invalid_inputs:
            with self.assertRaises(InvalidOxygenResultException):
                validate_oxygen_suite({**self.minimal, attribute: invalid_input})

    def test_validate_oxygen_suite_validates_name(self):
        self.shared_test_for_name()

    def test_validate_oxygen_suite_validates_tags(self):
        self.shared_test_for_tags()

    def test_validate_oxygen_suite_validates_setup(self):
        self.shared_test_for_keyword_field('setup')

    def test_validate_oxygen_suite_validates_teardown(self):
        self.shared_test_for_keyword_field('teardown')

    def test_validate_oxygen_suite_validates_suites(self):
        class OxygenSuiteDictSubclass(OxygenSuiteDict):
            pass
        valid_inherited = _ListSubclass()
        valid_inherited.append(OxygenSuiteDictSubclass(**self.minimal))

        self.valid_inputs_for('suites',
                              [],
                              [self.minimal],
                              valid_inherited,
                              [ OxygenSuiteDictSubclass(**self.minimal) ])

        self.invalid_inputs_for('suites', None, [ {} ])

    def test_validate_oxygen_suite_validates_tests(self):
        valid_inherited = _ListSubclass()
        valid_inherited.append(_TCSubclass(**MINIMAL_TC_DICT))
        valid_inherited.append(MINIMAL_TC_DICT)

        self.valid_inputs_for('tests',
                              [],
                              [ MINIMAL_TC_DICT ],
                              valid_inherited,
                              [ _TCSubclass(**MINIMAL_TC_DICT) ])


        self.invalid_inputs_for('tests', None, [ {} ])

    def test_validate_oxygen_suite_validates_metadata(self):
        class DictSubclass(dict):
            pass
        inherited_key = _StrSubclass('key')

        this_is_not_None = _StrSubclass(None)

        self.valid_inputs_for('metadata',
                              {},
                              {'': ''},
                              {'key': 'value'},
                              {_StrSubclass('key'): _StrSubclass('value')},
                              DictSubclass(inherited_key=_StrSubclass('value')),
                              {this_is_not_None: 'value'})

        self.invalid_inputs_for('metadata',
                                {'key': None},
                                {'key': 1234},)
