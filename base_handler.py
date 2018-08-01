import re

from datetime import datetime
from datetime import timedelta
from robot.result.model import Keyword as RobotKeyword
from robot.result.model import Message as RobotMessage
from robot.result.model import TestCase as RobotTest
from robot.result.model import TestSuite as RobotSuite


class BaseHandler(object):
    def __init__(self):
        self._keyword = None
        self._tags = []
        self._config = {}

    def build(self, config):
        """
        Set up the handler with the given configuration

        config: A dict including the 'keyword' node

        Return: None
        """
        keyword = config['keyword']

        tags = config.get('tags', [])
        if not isinstance(tags, list):
            tags = [tags]

        self._keyword = self._normalize_keyword_name(keyword)
        self._tags = tags
        self._config = config

    def get_keyword(self):
        return self._keyword

    def check(self, test):
        """Check if any of the keywords directly under this test trigger test
        execution

        test: A Robot test
        """
        for curr, keyword in enumerate(test.keywords):
            keyword_name = self._normalize_keyword_name(keyword.name)
            if not (keyword_name == self._keyword):
                continue

            # Set the current time to be the start of this keyword's execution
            self._current_time = self._get_from_timestamp(keyword.starttime)

            # ALL keywords, setup or not, preceding the trigger will be treated
            # as setup keywords later. Same goes for keywords succeeding the
            # trigger; they will become teardown keywords.
            setup_keywords = test.keywords[:curr]
            teardown_keywords = test.keywords[(curr+1):]

            self._report_oxygen_run(keyword, setup_keywords, teardown_keywords)

    def _report_oxygen_run(self, keyword, setup_keywords, teardown_keywords):
        """Run the tests associated with this handler and report on them

        keyword: The trigger keyword for this handler
        setup_keywords: The keywords preceding the trigger
        teardown_keywords: The keywords succeeding the trigger
        """
        # Wrap setup- and teardown keywords as a single keyword
        setup_keyword = self._robot_keyword(
            'Oxygen Setup',
            setup=True,
            keywords=self._robot_keywords(default_type=True, *setup_keywords),
        )
        teardown_keyword = self._robot_keyword(
            'Oxygen Teardown',
            teardown=True,
            keywords=self._robot_keywords(
                default_type=True, *teardown_keywords),
        )

        result_suite = self._build_results(
            keyword, setup_keyword, teardown_keyword)

    def _build_results(self, keyword, setup_keyword, teardown_keyword):
        """Execute the tests for this handler and report on the results

        keyword: The trigger keyword
        setup_keyword: The special oxygen setup wrapper
        teardown_keyword: The special oxygen teardown wrapper
        """
        test = keyword.parent
        test_results = self._parse_results(keyword.args)
        result_suite = self._build_suite(test_results)
        self._set_suite_tags(result_suite, *self._tags, *test.tags)
        result_suite.keywords.append(setup_keyword)
        result_suite.keywords.append(teardown_keyword)
        self._inject_suite_report(test, result_suite)

    def _inject_suite_report(self, test, result_suite):
        """Add the given suite to the top level of the current test execution

        test: Any Robot object part of the current test execution
        result_suite: Robot suite to report on
        """
        traveller = test.parent
        while traveller.parent is not None:
            traveller = traveller.parent

        traveller.suites.append(result_suite)

        test.parent.tests = [
            sibling for sibling in test.parent.tests if sibling is not test]

    def _normalize_keyword_name(self, keyword_name):
        """
        keyword_name: The raw keyword name (suite.subsuite.test.My Keyword)
        """
        short_name = str(keyword_name).split('.')[-1]
        underscored = re.sub(r' +', '_', short_name)
        return underscored.lower()

    def _set_suite_tags(self, suite, *tags):
        suite.set_tags(tags)
        return suite

    def _build_suite(self, suite):
        """Convert a given `suite` dict into a Robot suite"""
        robot_suites = self._build_suites([], suite)
        return robot_suites[0]

    def _build_suites(self, target, *suites):
        """Convert a set of suite dicts into Robot suites and append them to the
        given list-like object

        target: List-like object to add the Robot suites to
        suites: Set of suite dicts to build into Robot suites

        Return: The updated list-like object
        """
        for suite in suites:
            robot_suite = RobotSuite(suite['name'])
            robot_suite.set_tags(suite['tags'])

            self._build_keywords(robot_suite.keywords, *suite['setup'])
            self._build_keywords(robot_suite.keywords, *suite['teardown'])
            self._build_suites(robot_suite.suites, *suite['suites'])
            self._build_tests(robot_suite.tests, *suite['tests'])

            target.append(robot_suite)

        return target

    def _build_tests(self, target, *tests):
        """Convert a set of `tests` dicts and add to a Robot suite `target`"""
        for test in tests:
            robot_test = RobotTest(test['name'])
            robot_test.tags = test['tags']

            self._build_keywords(robot_test.keywords, *test['setup'])
            self._build_keywords(robot_test.keywords, *test['keywords'])
            self._build_keywords(robot_test.keywords, *test['teardown'])

            robot_test.status = self._keywords_status(robot_test.keywords)

            target.append(robot_test)

        return target

    def _build_keywords(self, target, *keywords):
        """Convert `keywords` dicts, add them as sub-keywords to a `target`"""
        for keyword in keywords:
            robot_keyword = self._robot_keyword(
                keyword['name'],
                tags=keyword['tags'],
                passed=keyword['pass'],
                elapsed=keyword.get('duration', 0.0)
            )

            self._build_messages(robot_keyword.messages, *keyword['messages'])
            self._build_keywords(robot_keyword.keywords, *keyword['keywords'])
            self._build_keywords(robot_keyword.keywords, *keyword['teardown'])

            target.append(robot_keyword)

        return target

    def _build_messages(self, target, *messages):
        for message in messages:
            target.append(RobotMessage(message))

        return target

    def _robot_keywords(self, *keywords, **kwargs):
        """
        Take `keywords` dicts and create Robot keywords from them,
        passing given `kwargs`
        """
        return_keywords = []
        for keyword in keywords:
            return_keywords.append(self._robot_keyword(
                existing=keyword,
                **kwargs,
            ))
        return return_keywords

    def _robot_keyword(self,
                       name=None,
                       tags=None,
                       passed=None,
                       setup=False,
                       teardown=False,
                       default_type=False,
                       existing=None,
                       elapsed=None,
                       keywords=None):
        """Create a new Robot keyword with specified data.

        name: Keyword name
        tags: List of keyword tag strings
        passed: Whether the keyword passed execution
        setup: True if this is a setup keyword (takes precedence over teardown
               and normal
        teardown: True if this is a teardown keyword (takes precedence over
                  normal
        default_type: True to set the keyword type to normal keyword
        existing: If a Robot keyword is passed as existing, all the other work
                  is done to update the existing keyword rather than create
                  a new one
        elapsed: Time spent executing the keyword
        keywords: Sub-keywords for the keyword itself
        """
        if existing:
            keyword = existing
        elif name:
            keyword = self._create_with_time(name, int(elapsed or 0.0))
        else:
            return None

        if tags:
            keyword.tags = tags

        # Determine keyword type based on parameters. Note that KEYWORD_TYPE is
        # not default behaviour (consider the case of updating an existing keyword)
        if setup:
            keyword.type = RobotKeyword.SETUP_TYPE
        elif teardown:
            keyword.type = RobotKeyword.TEARDOWN_TYPE
        elif default_type and keyword.type in [RobotKeyword.SETUP_TYPE,
                                               RobotKeyword.TEARDOWN_TYPE]:
            keyword.type = RobotKeyword.KEYWORD_TYPE

        if keywords:
            keyword.keywords = keywords

        # If the status is not forced by parameter, investigate the
        # sub-keywords (if any)
        if passed is None:
            keyword.status = self._keywords_status(keywords or [])
        elif passed:
            keyword.status = 'PASS'
        else:
            keyword.status = 'FAIL'
        return keyword

    def _create_with_time(self, keyword_name, elapsed, starttime=None):
        """Create a keyword with the given name, duration and start time.

        keyword_name: Keyword name to give the new object
        elapsed: Milliseconds of test duration
        starttime: A time object corresponding to start time.
                   If not given, current time will be used
        """
        starting_point = self._current_time
        # Create a delta object for elapsed time
        delta = timedelta(milliseconds=elapsed)
        time_format = self._get_time_format()

        # TODO: Inherit time based on children

        starting_time = starting_point.strftime(time_format)
        finishing_time = (starting_point + delta).strftime(time_format)

        keyword = RobotKeyword(
            keyword_name,
            starttime=starting_time,
            endtime=finishing_time,
        )
        self._current_time = self._current_time + delta
        return keyword

    def _get_time_format(self):
        """Convenience to return the general Robot timestamp format."""
        return '%Y%m%d %H:%M:%S.%f'

    def _get_from_timestamp(self, timestamp):
        time_object = datetime.strptime(
            timestamp,
            self._get_time_format(),
        )
        return time_object

    def _keywords_status(self, keywords):
        """
        keywords: List of Robot keywords

        Return: 'PASS' or 'FAIL'
        """
        if sum(not kw.passed for kw in keywords):
            return 'FAIL'
        else:
            return 'PASS'
