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
        test_cases = []
        with open(result_file) as results:
            result_contents = results.readlines()
        for line in result_contents:
            columns = line.strip().split('\t')
            if len(columns) < 8:
                continue
            step_name = columns[4]
            status = columns[7]
            if status not in ['OK', 'KO']:
                continue
            message = ''
            if len(columns) > 8:
                message = columns[8]

            keyword = {
                    'name': ' | '.join(columns),
                    'pass': True,
                    'messages': [],
                }

            if status == 'KO':
                keyword['pass'] = False
                keyword['messages'].append(message)

            test_case = {
                'name': step_name,
                'keywords': [keyword]
            }

            test_cases.append(test_case)

        test_suite = {
            'name': 'Gatling Scenario',
            'tags': self._tags,
            'tests': test_cases,
        }

        return test_suite
