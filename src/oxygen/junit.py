import subprocess

from robot.api import logger
from junitparser import Error, Failure, JUnitXml

from .errors import JUnitHandlerException
from .base_handler import BaseHandler


class JUnitHandler(BaseHandler):

    def run_junit(self, result_file, *command):
        """Run JUnit tool specified with ``command``.

        ``result_file`` must be first argument, so Oxygen can find the result
        file when parsing the results.
        """
        if command:
            proc = subprocess.run(command, capture_output=True)
            if proc.returncode != 0:
                raise JUnitHandlerException('Command "{}" '
                                            'failed'.format(command))
            logger.info(proc.stdout)
        logger.info('Result file: {}'.format(result_file))

    def parse_results(self, kw_args):
        result_file = kw_args[0]
        if not isinstance(result_file, str):
            raise JUnitHandlerException('"{}" is not '
                                        'a file path'.format(result_file))
        xml = JUnitXml.fromfile(result_file)
        return self._transform_tests(xml)

    def _transform_tests(self, node):
        """Convert the given xml object into a test suite dict

        node: An xml object from JUnitXml.fromfile()

        Return: The test suite dict
        """
        suite_dict = {
            'name': 'JUnit Execution',
            'tags': self._tags,
            'setup': [],
            'teardown': [],
            'suites': [],
            'tests': [],
        }

        for xunit_suite in node:
            suite = self._transform_test_suite(xunit_suite)
            suite_dict['suites'].append(suite)

        return suite_dict

    def _transform_test_suite(self, test_suite):
        """Convert the given suite xml object into a suite dict

        test_suite: A JUnit suite xml object

        Return: A suite dict
        """
        suite_dict = {
            'name': test_suite.name,
            'tags': [],
            'setup': [],
            'teardown': [],
            'suites': [],
            'tests': [],
        }

        # For child suites
        for xunit_suite in test_suite.testsuites():
            suite = self._transform_test_suite(xunit_suite)
            suite_dict['suites'].append(suite)

        # For test cases
        for xunit_case in test_suite:
            case = self._transform_test_case(xunit_case)
            suite_dict['tests'].append(case)

        return suite_dict

    def _transform_test_case(self, test_case):
        """Convert the given test case xml object into a test case dict

        test_case: A JUnit case xml object

        Return: A test case dict
        """
        test_dict = {
            'name': '{} (Execution)'.format(test_case.name),
            'pass': True,
            'tags': [],
            'messages': [],
            'teardown': [],
            'keywords': [],
        }

        errors = test_case.iterchildren(Error)
        failures = test_case.iterchildren(Failure)

        if errors:
            for error in errors:
                error_name = 'ERROR: {} ({})'.format(
                    error.message,
                    error.type,
                )
                test_dict['messages'].append(error_name)

        if failures:
            for failure in failures:
                failure_name = 'FAIL: {} ({})'.format(
                    failure.message,
                    failure.type,
                )
                test_dict['messages'].append(failure_name)

        # If we had errors/failures, it's not a PASS
        if test_dict['messages']:
            test_dict['pass'] = False

        execution_time = (test_case.time or 0.0) * 1000
        test_dict['elapsed'] = execution_time

        test_case_dict = {
            'name': test_case.name,
            'tags': [],
            'setup': [],
            'teardown': [],
            'keywords': [
                test_dict,
            ],
        }

        # This is really unreliable but at least we can find the trouble spots
        if not test_case.time:
            test_case_dict['tags'].append(
                'OXYGEN_JUNIT_UNKNOWN_EXECUTION_TIME')

        return test_case_dict
