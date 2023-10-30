''' IMPORTANT

OxygenKeywordDict is defined like this since key `pass` is reserved
word in Python, and thus raises SyntaxError if defined like a class.
However, in the functional style you cannot refer to the TypedDict itself
recursively, like you can with with class style. Oh bother.

See more:
 - https://docs.python.org/3/library/typing.html?highlight=typeddict#typing.TypedDict
 - https://stackoverflow.com/a/72460065
'''

import functools

from typing import List, Dict
# TODO FIXME: Python 3.10 requires these to be imported from here
# Python 3.10 EOL is in 2026
from typing_extensions import TypedDict, Required

from pydantic import TypeAdapter, ValidationError

from .errors import InvalidOxygenResultException


_Pass = TypedDict('_Pass', { 'pass': Required[bool], 'name': Required[str] })
# define required fields in this one above
class OxygenKeywordDict(_Pass, total=False):
    elapsed:  float  # milliseconds
    tags:     List[str]
    messages: List[str]
    teardown: 'OxygenKeywordDict'  # in RF, keywords do not have setup kw; just put it as first kw in `keywords`
    keywords: List['OxygenKeywordDict']


class OxygenTestCaseDict(TypedDict, total=False):
    name:     Required[str]
    keywords: Required[List[OxygenKeywordDict]]
    tags:     List[str]
    setup:    OxygenKeywordDict
    teardown: OxygenKeywordDict


class OxygenSuiteDict(TypedDict, total=False):
    name:     Required[str]
    tags:     List[str]
    setup:    OxygenKeywordDict
    teardown: OxygenKeywordDict
    metadata: Dict[str, str]
    suites:   List['OxygenSuiteDict']
    tests:    List[OxygenTestCaseDict]


def _change_validationerror_to_oxygenexception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            raise InvalidOxygenResultException(e)
    return wrapper

@_change_validationerror_to_oxygenexception
def validate_oxygen_suite(oxygen_result_dict):
    return TypeAdapter(OxygenSuiteDict).validate_python(oxygen_result_dict)

@_change_validationerror_to_oxygenexception
def validate_oxygen_test_case(oxygen_test_case_dict):
    return TypeAdapter(OxygenTestCaseDict).validate_python(oxygen_test_case_dict)

@_change_validationerror_to_oxygenexception
def validate_oxygen_keyword(oxygen_kw_dict):
    return TypeAdapter(OxygenKeywordDict).validate_python(oxygen_kw_dict)
