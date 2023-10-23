from unittest import TestCase

from oxygen.errors import InvalidOxygenResultException
from oxygen.oxygen_handler_result import validate_oxygen_test_case

from ..helpers import _ListSubclass, MINIMAL_KEYWORD_DICT, MINIMAL_TC_DICT
from .shared_tests import (SharedTestsForKeywordField,
                           SharedTestsForName,
                           SharedTestsForTags)

class TestOxygenTestCaseDict(TestCase,
                             SharedTestsForName,
                             SharedTestsForTags,
                             SharedTestsForKeywordField):
    def setUp(self):
        self.minimal = MINIMAL_TC_DICT

    def test_validate_oxygen_tc_validates_correctly(self):
        with self.assertRaises(InvalidOxygenResultException):
            validate_oxygen_test_case({})

    def test_validate_oxygen_tc_with_minimal_valid(self):
        expected = {
            'name': 'My TC',
            'keywords': []
        }
        self.assertEqual(validate_oxygen_test_case(expected), expected)
        self.assertEqual(validate_oxygen_test_case(self.minimal), self. minimal)

    def valid_inputs_for(self, attribute, *valid_inputs):
        for valid_input in valid_inputs:
            self.assertTrue(validate_oxygen_test_case({**self.minimal,
                                                       attribute: valid_input}))

    def invalid_inputs_for(self, attribute, *invalid_inputs):
        for invalid_input in invalid_inputs:
            with self.assertRaises(InvalidOxygenResultException):
                validate_oxygen_test_case({**self.minimal,
                                           attribute: invalid_input})

    def test_validate_oxygen_tc_validates_name(self):
        self.shared_test_for_name()

    def test_validate_oxygen_tc_validates_keywords(self):
        valid_inherited = _ListSubclass()
        valid_inherited.append(MINIMAL_KEYWORD_DICT)

        self.valid_inputs_for('keywords',
                              [],
                              [ MINIMAL_KEYWORD_DICT ],
                              _ListSubclass(),
                              valid_inherited)

        invalid_inherited = _ListSubclass()
        invalid_inherited.append( {} )

        self.invalid_inputs_for('keywords', None, invalid_inherited)

    def test_validate_oxygen_tc_validates_tags(self):
        self.shared_test_for_tags()

    def test_validate_oxygen_tc_validates_setup(self):
        self.shared_test_for_keyword_field('setup')

    def test_validate_oxygen_tc_validates_teardown(self):
        self.shared_test_for_keyword_field('teardown')
