from robot.api import logger

from .base_handler import BaseHandler
from .errors import GatlingHandlerException, SubprocessException
from .utils import run_command_line, validate_path

class GatlingHandler(BaseHandler):

    def run_gatling(self, result_file, command, check_return_code=False, **env):
        '''Run Gatling performance testing tool specified with ``command``.

        ``result_file`` is path to the file ``oxygen`` uses to parse the results.
        It is important you craft your `command` to produce the file
        `result_file` argument expects — otherwise Oxygen will not be able to
        parse the results later on.

        ``command`` is used to run the test tool. It is a single string which is
        run in a terminal subshell.

        ``check_return_code`` checks that ``command`` returns with exit code zero
        (0). By default, return code is not checked as failing test execution
        generally is reported with non-zero return code. However, it is useful
        to set ``check_return_code`` to ``True`` temporarily when you want to
        debug why the test tool is failing for other reasons than failing test
        execution.

        ``env`` is used to pass environment variables that are set in the subshell
        the ``command`` is run in.
        '''
        try:
            output = run_command_line(command, check_return_code, **env)
        except SubprocessException as e:
            raise GatlingHandlerException(e)
        logger.info(output)
        logger.info('Result file: {}'.format(result_file))
        return result_file

    def parse_results(self, result_file):
        return self._transform_tests(validate_path(result_file).resolve())

    def _transform_tests(self, result_file):
        '''Given the result_file path, open the test results and get a suite
        dict.

        The whole Gatling format is jank 3000.
        Here be dragons.

        result_file: The path to the Gatling results
        '''
        test_suites = []
        test_cases = []
        current_suite = None
        current_test = None
        with open(result_file) as results:
            result_contents = results.readlines()
        for line in result_contents:
            column_names = [
                'Action',
                'Scenario',
                'User ID',
                'Group',
                'Name',
                'Start time',
                'End time',
                'Status',
                'Response',
                'Message',
                'Extra information',
            ]
            columns = line.strip().split('\t')
            messages = []
            for idx, value in enumerate(column_names):
                action = '<NO ACTION>'
                scenario = '<NO SCENARIO>'
                group = '<NO GROUP>'
                step_name = '<NO STEP NAME>'
                start_time = -1
                end_time = -1
                status = 'KO'
                if idx >= len(columns):
                    continue
                log_value = columns[idx]
                messages.append(value + ': ' + log_value)
                if value == 'Action':
                    action = log_value
                if value == 'Scenario':
                    scenario = log_value
                if value == 'Group':
                    group = log_value
                if value == 'Name':
                    step_name = log_value
                if value == 'Start time':
                    start_time = int(log_value)
                if value == 'End time':
                    end_time = int(log_value)
                if value == 'Status':
                    status = log_value

            if action == 'RUN' or current_suite == None:
                if current_suite:
                    test_suites.append(current_suite)
                current_suite = {
                    'name': 'Gatling Scenario: ' + scenario,
                    'start': start_time,
                    'finish': end_time,
                    'tests': [],
                }

            if action == 'USER':
                current_suite['tests'].append(current_test)
                current_suite['finish'] = max(current_suite['finish'], current_test['finish'])
                current_test = {
                    'name': action + ' ' + scenario + ': ' + group,
                    'start': start_time,
                    'finish': end_time,
                    'keywords': [],
                }

            if action == 'REQUEST':
                keyword = {
                    'name': step_name,
                    'start': start_time,
                    'finish': end_time,
                    'pass': (status == 'OK'),
                    'messages': messages,
                }
                current_test['keywords'].append(keyword)
                current_test['finish'] = max(current_test['finish'], end_time)

        current_suite['tests'].append(current_test)
        current_suite['finish'] = max(current_suite['finish'], current_test['finish'])
        test_suites.append(current_suite)

        parent_suite = {
            'name': 'Gatling Scenarios',
        }

        if test_suites:
            parent_suite = {
                'name': 'Gatling Scenarios',
                'start': test_suites[0]['start'],
                'finish': test_suites[-1]['finish'],
                'suites': test_suites,
            }

        return parent_suite
