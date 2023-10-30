from ..helpers import (MINIMAL_KEYWORD_DICT,
                       _ListSubclass,
                       _StrSubclass,
                       _KwSubclass)

class SharedTestsForName(object):
    def shared_test_for_name(self):
        valid_inherited = _StrSubclass('someKeyword')
        this_is_not_None = _StrSubclass(None)

        self.valid_inputs_for('name',
                              '',
                              'someKeyword',
                              b'someKeyword',
                              valid_inherited,
                              this_is_not_None)

        self.invalid_inputs_for('name', None)


class SharedTestsForTags(object):
    def shared_test_for_tags(self):
        self.valid_inputs_for('tags',
                              [],
                              ['some-tag', 'another-tag'],
                              _ListSubclass())

        invalid_inherited = _ListSubclass()
        invalid_inherited.append(123)

        self.invalid_inputs_for('tags', [123], None, {'foo': 'bar'}, object())


class SharedTestsForKeywordField(object):
    def shared_test_for_keyword_field(self, attribute):
        valid_inherited = _KwSubclass(**MINIMAL_KEYWORD_DICT)

        self.valid_inputs_for(attribute,
                              MINIMAL_KEYWORD_DICT,
                              valid_inherited,
                              {**MINIMAL_KEYWORD_DICT,
                               'something_random': 'will-be-ignored'})

        self.invalid_inputs_for(attribute, None, {})
