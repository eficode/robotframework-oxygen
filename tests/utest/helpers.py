import sys

from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from tempfile import mkstemp

from robot.api import ExecutionResult
from yaml import FullLoader, load

from oxygen.oxygen_handler_result import OxygenKeywordDict, OxygenTestCaseDict

TEST_CONFIG = '''
oxygen.junit:
  handler: JUnitHandler
  keyword: run_junit
  tags:
    - JUNIT
    - EXTRA_JUNIT_CASE
oxygen.gatling:
  handler: GatlingHandler
  keyword: run_gatling
  tags: GATLING
oxygen.zap:
  handler: ZAProxyHandler
  keyword: run_zap
  tags: ZAP
  accepted_risk_level: 2
  required_confidence_level: 1
oxygen.my_dummy_handler:
  handler: MyDummyHandler
  keyword: run_my_dummy_handler
  tags: MY_DUMMY_HANDLER
'''

RESOURCES_PATH = Path.cwd() / 'tests' / 'resources'

def get_config():
    return load(TEST_CONFIG, Loader=FullLoader)

def get_config_as_file():
    _, filepath = mkstemp()
    with open(filepath, 'w') as f:
        f.write(TEST_CONFIG)
    return filepath

@contextmanager
def suppress_stdout():
    old = sys.stdout
    sys.stdout = StringIO()
    try:
        yield
    finally:
        sys.stdout = old

def example_robot_output():
    output = RESOURCES_PATH / 'example_robot_output.xml'
    return ExecutionResult(output)

MINIMAL_KEYWORD_DICT = { 'name': 'someKeyword', 'pass': True }
MINIMAL_TC_DICT = { 'name': 'Minimal TC', 'keywords': [MINIMAL_KEYWORD_DICT] }
MINIMAL_SUITE_DICT = {'name': 'Minimal Suite',
                      'suites': [{
                          'name': 'Minimal Subsuite',
                          'tests': [ MINIMAL_TC_DICT ]}]}


class _ListSubclass(list):
    '''Used in test cases'''
    pass


class _KwSubclass(OxygenKeywordDict):
    '''Used in test cases'''
    pass


class _TCSubclass(OxygenTestCaseDict):
    '''Used in test cases'''
    pass

class _StrSubclass(str):
    '''Used in test cases'''
    pass

GATLING_EXPECTED_OUTPUT = {'name': 'Gatling Scenario',
 'tags': ['GATLING'],
 'tests': [{'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Home | '
                                  '1533120479221 | 1533120479313 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Home | '
                                  '1533120479124 | 1533120479298 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Home Redirect 1 | '
                                  '1533120479321 | 1533120479368 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Home Redirect 1 | '
                                  '1533120479321 | 1533120479367 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Home | '
                                  '1533120480235 | 1533120480421 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Home Redirect 1 | '
                                  '1533120480422 | 1533120480466 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Search | '
                                  '1533120480410 | 1533120480744 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Search | '
                                  '1533120480407 | 1533120480768 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Home | '
                                  '1533120481234 | 1533120481322 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Home Redirect 1 | '
                                  '1533120481323 | 1533120481368 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Search | '
                                  '1533120481486 | 1533120481533 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Select | '
                                  '1533120481736 | 1533120481783 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Select | '
                                  '1533120481756 | 1533120481800 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Home | '
                                  '1533120482095 | 1533120482187 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Home Redirect 1 | '
                                  '1533120482188 | 1533120482235 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Search | '
                                  '1533120482385 | 1533120482431 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Select | '
                                  '1533120482536 | 1533120482582 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Page 0 | '
                                  '1533120482801 | 1533120482848 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Page 0 | '
                                  '1533120482804 | 1533120482848 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Home | '
                                  '1533120483096 | 1533120483190 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Home Redirect 1 | '
                                  '1533120483191 | 1533120483238 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Search | '
                                  '1533120483256 | 1533120483303 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Select | '
                                  '1533120483436 | 1533120483482 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Page 0 | '
                                  '1533120483585 | 1533120483631 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Page 1 | '
                                  '1533120483835 | 1533120483881 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Page 1 | '
                                  '1533120483845 | 1533120483889 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Home | '
                                  '1533120484086 | 1533120484182 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Home | '
                                  '1533120484095 | 1533120484221 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Home Redirect 1 | '
                                  '1533120484183 | 1533120484228 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Home Redirect 1 | '
                                  '1533120484222 | 1533120484269 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Search | '
                                  '1533120484255 | 1533120484303 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Select | '
                                  '1533120484305 | 1533120484352 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Page 0 | '
                                  '1533120484476 | 1533120484523 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Page 1 | '
                                  '1533120484635 | 1533120484679 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Page 2 | '
                                  '1533120484887 | 1533120484933 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Page 2 | '
                                  '1533120484896 | 1533120484940 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Home | '
                                  '1533120485084 | 1533120485170 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Home Redirect 1 | '
                                  '1533120485171 | 1533120485225 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Search | '
                                  '1533120485246 | 1533120485291 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Search | '
                                  '1533120485286 | 1533120485331 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Select | '
                                  '1533120485306 | 1533120485357 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Page 0 | '
                                  '1533120485345 | 1533120485408 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Page 1 | '
                                  '1533120485536 | 1533120485583 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Page 2 | '
                                  '1533120485676 | 1533120485720 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Page 3 | '
                                  '1533120485936 | 1533120485981 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 1 |  | Page 3 | '
                                  '1533120485936 | 1533120485982 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Home | '
                                  '1533120486085 | 1533120486166 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Home Redirect 1 | '
                                  '1533120486167 | 1533120486212 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Search | '
                                  '1533120486247 | 1533120486291 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Select | '
                                  '1533120486295 | 1533120486340 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Select | '
                                  '1533120486335 | 1533120486380 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Page 0 | '
                                  '1533120486355 | 1533120486403 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Page 1 | '
                                  '1533120486414 | 1533120486460 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Page 2 | '
                                  '1533120486586 | 1533120486631 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 2 |  | Page 3 | '
                                  '1533120486716 | 1533120486761 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Form | '
                                  '1533120486987 | 1533120487033 | OK',
                          'pass': True}],
            'name': 'Form'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Home | '
                                  '1533120487094 | 1533120487191 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Home Redirect 1 | '
                                  '1533120487192 | 1533120487237 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Search | '
                                  '1533120487236 | 1533120487280 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Select | '
                                  '1533120487284 | 1533120487332 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Page 0 | '
                                  '1533120487334 | 1533120487378 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Page 0 | '
                                  '1533120487375 | 1533120487420 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Page 1 | '
                                  '1533120487416 | 1533120487464 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Page 2 | '
                                  '1533120487455 | 1533120487502 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 3 |  | Page 3 | '
                                  '1533120487615 | 1533120487662 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Post | '
                                  '1533120488053 | 1533120488103 | OK',
                          'pass': True}],
            'name': 'Post'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 4 |  | Post Redirect 1 | '
                                  '1533120488113 | 1533120488157 | OK',
                          'pass': True}],
            'name': 'Post Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Home | '
                                  '1533120488096 | 1533120488181 | OK',
                          'pass': True}],
            'name': 'Home'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Home Redirect 1 | '
                                  '1533120488182 | 1533120488249 | OK',
                          'pass': True}],
            'name': 'Home Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Search | '
                                  '1533120488256 | 1533120488300 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Select | '
                                  '1533120488276 | 1533120488319 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Page 0 | '
                                  '1533120488334 | 1533120488390 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Page 1 | '
                                  '1533120488384 | 1533120488429 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Page 1 | '
                                  '1533120488425 | 1533120488471 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Page 2 | '
                                  '1533120488465 | 1533120488513 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 5 |  | Page 3 | '
                                  '1533120488504 | 1533120488549 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Search | '
                                  '1533120489266 | 1533120489311 | OK',
                          'pass': True}],
            'name': 'Search'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Select | '
                                  '1533120489306 | 1533120489348 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Page 0 | '
                                  '1533120489316 | 1533120489358 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Page 1 | '
                                  '1533120489395 | 1533120489441 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Page 2 | '
                                  '1533120489425 | 1533120489470 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Page 2 | '
                                  '1533120489463 | 1533120489509 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 6 |  | Page 3 | '
                                  '1533120489504 | 1533120489577 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Select | '
                                  '1533120490304 | 1533120490353 | OK',
                          'pass': True}],
            'name': 'Select'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Page 0 | '
                                  '1533120490344 | 1533120490386 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Page 1 | '
                                  '1533120490365 | 1533120490407 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Page 2 | '
                                  '1533120490436 | 1533120490481 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Page 3 | '
                                  '1533120490475 | 1533120490525 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 7 |  | Page 3 | '
                                  '1533120490515 | 1533120490560 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Page 0 | '
                                  '1533120491366 | 1533120491413 | OK',
                          'pass': True}],
            'name': 'Page 0'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Page 1 | '
                                  '1533120491386 | 1533120491430 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Page 2 | '
                                  '1533120491405 | 1533120491447 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 9 |  | Page 3 | '
                                  '1533120491486 | 1533120491531 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Form | '
                                  '1533120491515 | 1533120491560 | OK',
                          'pass': True}],
            'name': 'Form'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Page 1 | '
                                  '1533120492404 | 1533120492449 | OK',
                          'pass': True}],
            'name': 'Page 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Page 2 | '
                                  '1533120492436 | 1533120492479 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 10 |  | Page 3 | '
                                  '1533120492446 | 1533120492488 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Post | '
                                  '1533120492564 | 1533120492610 | OK',
                          'pass': True}],
            'name': 'Post'},
           {'keywords': [{
                          'messages': ['status.find.is(201), but actually '
                                       'found 200'],
                          'name': 'REQUEST | Admins | 8 |  | Post Redirect 1 | '
                                  '1533120492611 | 1533120492655 | KO | '
                                  'status.find.is(201), but actually found 200',
                          'pass': False}],
            'name': 'Post Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Form | '
                                  '1533120492674 | 1533120492719 | OK',
                          'pass': True}],
            'name': 'Form'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Page 2 | '
                                  '1533120493454 | 1533120493499 | OK',
                          'pass': True}],
            'name': 'Page 2'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 11 |  | Page 3 | '
                                  '1533120493476 | 1533120493518 | OK',
                          'pass': True}],
            'name': 'Page 3'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Admins | 8 |  | Post | '
                                  '1533120493706 | 1533120493750 | OK',
                          'pass': True}],
            'name': 'Post'},
           {'keywords': [{
                          'messages': ['status.find.is(201), but actually '
                                       'found 200'],
                          'name': 'REQUEST | Admins | 8 |  | Post Redirect 1 | '
                                  '1533120493751 | 1533120493797 | KO | '
                                  'status.find.is(201), but actually found 200',
                          'pass': False}],
            'name': 'Post Redirect 1'},
           {'keywords': [{
                          'messages': [],
                          'name': 'REQUEST | Users | 12 |  | Page 3 | '
                                  '1533120494505 | 1533120494552 | OK',
                          'pass': True}],
            'name': 'Page 3'}]}
