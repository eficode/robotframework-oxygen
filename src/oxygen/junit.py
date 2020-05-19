from robot.api import logger
from junitparser import Error, Failure, JUnitXml
from junitparser.junitparser import TestSuite as JUnitXmlTestSuite

from .base_handler import BaseHandler
from .errors import JUnitHandlerException, SubprocessException
from .utils import run_command_line, validate_path


class JUnitHandler(BaseHandler):

    def run_junit(self, result_file, command, check_return_code=False, **env):
        '''Run JUnit unit testing tool specified with ``command``.

        See documentation for other arguments in \`Run Gatling\`.
        '''
        logger.debug(f'Command: {command}')
        try:
            output = run_command_line(command, check_return_code, **env)
        except SubprocessException as e:
            raise JUnitHandlerException(e)
        logger.info(output)
        logger.info('Result file: {}'.format(result_file))
        return result_file

    def parse_results(self, result_file):
        result_file = self._validate_path(result_file)
        try:
            xml = JUnitXml.fromfile(result_file)
        except TypeError as e:
            raise JUnitHandlerException(e)
        return self._transform_tests(xml)

    def _validate_path(self, result_file):
        try:
            return str(validate_path(result_file).resolve())
        except TypeError as e:
            raise JUnitHandlerException(f'Invalid result file path: {e}')

    def _transform_tests(self, node):
        '''Convert the given xml object into a test suite dict

        node: An xml object from JUnitXml.fromfile()

        Return: The test suite dict
        '''
        suite_dict = {
            'name': 'JUnit Execution',
            'tags': self._tags,
            'setup': [],
            'teardown': [],
            'suites': [],
            'tests': [],
        }

        if isinstance(node, JUnitXmlTestSuite):
            node = [node]

        for xunit_suite in node:
            suite = self._transform_test_suite(xunit_suite)
            suite_dict['suites'].append(suite)

        return suite_dict

    def _transform_test_suite(self, test_suite):
        '''Convert the given suite xml object into a suite dict

        test_suite: A JUnit suite xml object

        Return: A suite dict
        '''
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
        '''Convert the given test case xml object into a test case dict

        test_case: A JUnit case xml object

        Return: A test case dict
        '''
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
                'oxygen-junit-unknown-execution-time')

        return test_case_dict
