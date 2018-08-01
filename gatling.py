from base_handler import BaseHandler
from robot.result.model import TestSuite
import subprocess


class GatlingHandler(BaseHandler):
    def _parse_results(self, args):
        """Execute the Gatling tests given the arguments

        args: Keyword arguments (first argument is the location of the test
              output)
        """
        if len(args) > 1:
            subprocess.run(args[1:])
        result_file = args[0]
        return self._transform_tests(result_file)

    def _transform_tests(self, result_file):
        """Given the result_file path, open the test results and get a suite dict

        The whole Gatling format is jank 3000.
        Here be dragons.

        result_file: The path to the Gatling results
        """
        test_cases = []
        with open(result_file) as results:
            for line in results:
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
                    'keywords': [
                        keyword,
                    ],
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
