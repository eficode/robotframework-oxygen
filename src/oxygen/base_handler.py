import re

from inspect import signature, Parameter

from .errors import MismatchArgumentException
from .robot_interface import (RobotInterface, get_keywords_from,
                              set_special_keyword)
from .utils import validate_with_deprecation_warning

class BaseHandler(object):
    DEFAULT_CLI = {tuple(['result_file']): {}}

    def __init__(self, config):
        '''
        Set up the handler with the given configuration

        config: A dict including the 'keyword' node
        '''
        self._interface = RobotInterface()
        self._config = config

        tags = self._config.get('tags', [])
        if not isinstance(tags, list):
            tags = [tags]
        self._tags = tags
        self.keyword = self._normalize_keyword_name(self._config['keyword'])
        self.run_time_data = None

    def cli(self):
        '''
        augment in subclasses

        def cli(self):
            cli_interface = self.DEFAULT_CLI.copy()
            cli_interface[('-e', '--example')] = {'help': 'use this like that'}
            cli_interface[('-f', '--flag')] = {'action': 'store_true'}
            return cli_interface
        '''
        return self.DEFAULT_CLI

    def parse_results(self, kw_args):
        raise NotImplementedError('Actual handler implementation should override '
                                  'this with proper implementation!')

    def check_for_keyword(self, test, data):
        '''Check if any of the keywords directly under this test trigger test
        execution

        test: A Robot test
        '''
        test_keywords = get_keywords_from(test)

        for curr, keyword in enumerate(test_keywords):
            keyword_name = self._normalize_keyword_name(keyword.name)
            if not (keyword_name == self.keyword):
                continue

            self.run_time_data = data[test.longname]
            # ALL keywords, setup or not, preceding the trigger will be treated
            # as setup keywords later. Same goes for keywords succeeding the
            # trigger; they will become teardown keywords.
            setup_keywords = test_keywords[:curr]
            teardown_keywords = test_keywords[(curr+1):]

            self._report_oxygen_run(keyword, setup_keywords, teardown_keywords)


    def _report_oxygen_run(self, keyword, setup_keywords, teardown_keywords):
        '''
        keyword: The trigger keyword for this handler
        setup_keywords: The keywords preceding the trigger
        teardown_keywords: The keywords succeeding the trigger
        '''
        # Wrap setup- and teardown keywords as a single keyword
        setup_keyword = None
        teardown_keyword = None

        if setup_keywords:
            setup_start = setup_keywords[0].starttime
            setup_end = setup_keywords[-1].endtime
            setup_keyword = self._interface.result.create_wrapper_keyword(
                'Oxygen Setup',
                setup_start,
                setup_end,
                True,
                *setup_keywords)

        if teardown_keywords:
            teardown_start = teardown_keywords[0].starttime
            teardown_end = teardown_keywords[-1].endtime
            teardown_keyword = self._interface.result.create_wrapper_keyword(
                'Oxygen Teardown',
                teardown_start,
                teardown_end,
                False,
                *teardown_keywords)

        self._build_results(keyword, setup_keyword, teardown_keyword)

    def _build_results(self, keyword, setup_keyword, teardown_keyword):
        '''
        keyword: The trigger keyword
        setup_keyword: The special oxygen setup wrapper
        teardown_keyword: The special oxygen teardown wrapper
        '''
        accepted_params = signature(self.parse_results).parameters
        accepted_params_max = len(accepted_params)
        accepted_params_min = len([
            n for n, v in accepted_params.items()
            if v.default == Parameter.empty])
        is_multiple_inputs = isinstance(self.run_time_data, tuple)

        # there are multiple inputs and in the range of accepted min and max
        if is_multiple_inputs and (accepted_params_min <= len(
                self.run_time_data) <= accepted_params_max):
            test_results = self.parse_results(*self.run_time_data)

        # there is single input and one required, also can be more non-required
        elif not is_multiple_inputs and accepted_params_min == 1:
            test_results = self.parse_results(self.run_time_data)

        # else if there are multiple inputs and not in the range of accepted
        elif is_multiple_inputs:
            raise MismatchArgumentException(
                f'parse_results expects at least {accepted_params_min} and'
                f' at most {accepted_params_max} arguments '
                f'but got {len(self.run_time_data)}')

        # at this point there could be only multiple required and single input
        else:
            raise MismatchArgumentException(
                f'parse_results expects at least {accepted_params_min} '
                'arguments but got 1')

        self._validate(test_results)

        _, result_suite = self._interface.result.build_suite(
            100000, test_results)

        if not result_suite:
            return

        test = keyword.parent
        self._set_suite_tags(result_suite, *(self._tags + list(test.tags)))

        if setup_keyword:
            set_special_keyword(result_suite, 'setup', setup_keyword)

        if teardown_keyword:
            set_special_keyword(result_suite, 'teardown', teardown_keyword)

        self._inject_suite_report(test, result_suite)

    def _validate(self, oxygen_result_dict):
        validate_with_deprecation_warning(oxygen_result_dict, self)

    def _inject_suite_report(self, test, result_suite):
        '''Add the given suite to the parent suite of the test case.

        This also filters out the test case from the parent suite test cases.

        test: Any Robot object part of the current test execution
        result_suite: Robot suite to report on
        '''
        suite = test.parent
        new_tests = [t for t in suite.tests if t is not test]
        suite.suites.append(result_suite)
        suite.tests = new_tests

    def _normalize_keyword_name(self, keyword_name):
        '''
        keyword_name: The raw keyword name (suite.subsuite.test.My Keyword)
        '''
        short_name = str(keyword_name).split('.')[-1].strip()
        underscored = re.sub(r' +', '_', short_name)
        return underscored.lower()

    def _set_suite_tags(self, suite, *tags):
        suite.set_tags(tags)
        return suite

