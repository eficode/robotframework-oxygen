from unittest import TestCase

from oxygen.errors import InvalidOxygenResultException
from oxygen.oxygen_handler_result import (validate_oxygen_keyword,
                                          OxygenKeywordDict)

from ..helpers import (MINIMAL_KEYWORD_DICT,
                       _ListSubclass,
                       _KwSubclass)
from .shared_tests import (SharedTestsForKeywordField,
                           SharedTestsForName,
                           SharedTestsForTags)


class TestOxygenKeywordDict(TestCase,
                            SharedTestsForName,
                            SharedTestsForTags,
                            SharedTestsForKeywordField):
    def setUp(self):
        self.minimal = MINIMAL_KEYWORD_DICT

    def test_validate_oxygen_keyword_validates_correctly(self):
        with self.assertRaises(InvalidOxygenResultException):
            validate_oxygen_keyword({})

    def test_validate_oxygen_keyword_with_minimal_valid(self):
        minimal1 = { 'name': 'somename', 'pass': True }
        minimal2 = { 'name': 'somename', 'pass': False }

        self.assertEqual(validate_oxygen_keyword(minimal1), minimal1)
        self.assertEqual(validate_oxygen_keyword(minimal2), minimal2)

    def valid_inputs_for(self, attribute, *valid_inputs):
        for valid_input in valid_inputs:
            self.assertTrue(validate_oxygen_keyword({**self.minimal,
                                                     attribute: valid_input}))

    def invalid_inputs_for(self, attribute, *invalid_inputs):
        for invalid_input in invalid_inputs:
            with self.assertRaises(InvalidOxygenResultException):
                validate_oxygen_keyword({**self.minimal,
                                         attribute: invalid_input})

    def test_validate_oxygen_keyword_validates_name(self):
        self.shared_test_for_name()

    def test_validate_oxygen_keyword_validates_pass(self):
        '''
        Due note that boolean cannot be subclassed in Python:
        https://mail.python.org/pipermail/python-dev/2002-March/020822.html
        '''
        self.valid_inputs_for('pass', True, False, 0, 1, 0.0, 1.0)
        self.invalid_inputs_for('pass', [], {}, None, object(), -999, -99.9)

    def test_validate_oxygen_keyword_validates_tags(self):
        self.shared_test_for_tags()

    def test_validate_oxygen_keyword_validates_elapsed(self):
        class FloatSubclass(float):
            pass

        self.valid_inputs_for('elapsed',
                              123.4,
                              -123.0,
                              '123.4',
                              '-999.999',
                              123,
                              FloatSubclass())

        self.invalid_inputs_for('elapsed', '', None, object())

    def test_validate_oxygen_keyword_validates_messages(self):
        valid_inherited = _ListSubclass()
        valid_inherited.append('message')

        self.valid_inputs_for('messages',
                              [],
                              ['message'],
                              _ListSubclass(),
                              valid_inherited)

        invalid_inherited = _ListSubclass()
        invalid_inherited.append('message')
        invalid_inherited.append(123)

        self.invalid_inputs_for('messages',
                                'some,messages',
                                None,
                                invalid_inherited)

    def test_validate_oxygen_keyword_validates_teardown(self):
        self.shared_test_for_keyword_field('teardown')

    def test_validate_oxygen_keyword_validates_keywords(self):
        valid_inherited = _ListSubclass()
        valid_inherited.append(_KwSubclass(**self.minimal))

        self.valid_inputs_for('keywords',
                              [],
                              [self.minimal, {**self.minimal,
                                              'something_random': 'will-be-ignored'}],
                              _ListSubclass(),  # empty inherited list
                              valid_inherited)

        invalid_inherited = _ListSubclass()
        invalid_inherited.append(_KwSubclass(**self.minimal))
        invalid_inherited.append(123)
        self.invalid_inputs_for('keywords', None, invalid_inherited)

    def test_validate_oxygen_keyword_with_maximal_valid(self):
        expected = {
            'name': 'keyword',
            'pass': True,
            'tags': ['some-tag'],
            'messages': ['some message'],
            'teardown': {
                'name': 'teardownKeyword',
                'pass': True,
                'tags': ['teardown-kw'],
                'messages': ['Teardown passed'],
                'keywords': []
            },
            'keywords': [{
                'name': 'subKeyword',
                'pass': False,
                # tags missing intentionally
                'messages': ['This particular kw failed'],
                'teardown': {
                    'name': 'anotherTeardownKw',
                    'pass': True,
                    'tags': ['teardown-kw'],
                    'messages': ['message from anotherTeardownKw'],
                    # teardown missing intentionally
                    'keywords': []
                },
                'keywords': [{
                    'name': 'subsubKeyword',
                    'pass': True,
                }]
            },{
                'name': 'anotherSubKeyword',
                'pass': True,
                'tags': [],
                'messages': [],
                'keywords': []
            }]
        }

        self.assertEqual(validate_oxygen_keyword(expected), expected)
