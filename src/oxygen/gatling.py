from robot.api import logger

from .base_handler import BaseHandler
from .errors import GatlingHandlerException, SubprocessException
from .utils import run_command_line

class GatlingHandler(BaseHandler):

    def run_gatling(self, result_file, *command):
        """Run Gatling tool specified with ``command``.

        ``result_file`` must be first argument, so Oxygen can find the result
        file when parsing the results.
        """
        try:
            output = run_command_line(*command)
        except SubprocessException as e:
            raise GatlingHandlerException(e)
        logger.info(output)
        logger.info('Result file: {}'.format(result_file))

    def parse_results(self, rf_kw_args):
        return self._transform_tests(rf_kw_args[0])

    def _transform_tests(self, result_file):
        """Given the result_file path, open the test results and get a suite dict

        The whole Gatling format is jank 3000.
        Here be dragons.

        result_file: The path to the Gatling results
        """
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
                    'tags': [],
                    'messages': [],
                    'teardown': [],
                    'keywords': [],
                }

            if status == 'KO':
                keyword['pass'] = False
                keyword['messages'].append(message)

            test_case = {
                'name': step_name,
                'tags': [],
                'setup': [],
                'teardown': [],
                'keywords': [keyword]
            }

            test_cases.append(test_case)

        test_suite = {
            'name': 'Gatling Scenario',
            'tags': self._tags,
            'setup': [],
            'teardown': [],
            'suites': [],
            'tests': test_cases,
        }

        return test_suite
