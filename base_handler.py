import re

from datetime import datetime
from datetime import timedelta
from robot.result.model import Keyword as RobotKeyword
from robot.result.model import Message as RobotMessage
from robot.result.model import TestCase as RobotTest
from robot.result.model import TestSuite as RobotSuite


class BaseHandler(object):
    #####################
    # __init__
    #
    # Class initializer
    #
    # Return: N/A
    #####################
    def __init__(self):
        self._keyword = None
        self._tags = []
        self._config = {}

    #####################
    # build
    #
    # Set up the handler with the given configuration
    #
    # config: A dict including the 'keyword' node
    #
    # Return: None
    #####################

    def build(self, config):
        # The keyword that triggers the handler's behaviour
        keyword = config['keyword']

        # Tags for this handler
        tags = config.get('tags', [])
        if not isinstance(tags, list):
            tags = [tags]

        self._keyword = self._normalize_keyword_name(keyword)
        self._tags = tags
        self._config = config

    #####################
    # get_keyword
    #
    # Get the keyword name that triggers this handler
    #
    # Return: Trigger keyword name
    #####################

    def get_keyword(self):
        return self._keyword

    #####################
    # check
    #
    # Check if any of the keywords directly under this test trigger test execution
    #
    # test: A Robot test
    #
    # Return: None
    #####################

    def check(self, test):
        for curr, keyword in enumerate(test.keywords):
            keyword_name = self._normalize_keyword_name(keyword.name)
            if not (keyword_name == self._keyword):
                continue

            # If one of the test keywords triggers this Oxygen handler:

            # Set the current time to be the start of this keyword's execution
            self._current_time = self._get_from_timestamp(keyword.starttime)

            # ALL keywords, setup or not, preceding the trigger will be treated as
            # setup keywords later
            setup_keywords = test.keywords[:curr]

            # ALL keywords, teardown or not, succeeding the trigger will be treated as
            # teardown keywords later
            teardown_keywords = test.keywords[(curr+1):]

            # Run and report on the triggered handler
            self._report_oxygen_run(keyword, setup_keywords, teardown_keywords)

    #####################
    # _report_oxygen_run
    #
    # Run the tests associated with this handler and report on them
    #
    # keyword: The trigger keyword for this handler
    # setup_keywords: The keywords preceding the trigger
    # teardown_keywords: The keywords succeeding the trigger
    #
    # Return: None
    #####################

    def _report_oxygen_run(self, keyword, setup_keywords, teardown_keywords):
        # Create a special wrapper keyword for all "setup" keywords (see check()
        # comments)
        setup_keyword = self._robot_keyword(
            'Oxygen Setup',
            setup=True,
            keywords=self._robot_keywords(default_type=True, *setup_keywords),
        )

        # Create a special wrapper keyword for all "teardown" keywords (see check()
        # comments)
        teardown_keyword = self._robot_keyword(
            'Oxygen Teardown',
            teardown=True,
            keywords=self._robot_keywords(
                default_type=True, *teardown_keywords),
        )

        # Handle trigger keyword and report
        result_suite = self._build_results(
            keyword, setup_keyword, teardown_keyword)

    #####################
    # _build_results
    #
    # Execute the tests for this handler and report on the results
    #
    # keyword: The trigger keyword
    # setup_keyword: The special oxygen setup wrapper
    # teardown_keyword: The special oxygen teardown wrapper
    #
    # Return: None
    #####################

    def _build_results(self, keyword, setup_keyword, teardown_keyword):
        test = keyword.parent

        # Execute the oxygen tests and get the results
        test_results = self._parse_results(keyword.args)

        result_suite = self._build_suite(test_results)
        self._set_suite_tags(result_suite, *self._tags, *test.tags)

        result_suite.keywords.append(setup_keyword)
        result_suite.keywords.append(teardown_keyword)

        self._inject_suite_report(test, result_suite)

    #####################
    # _inject_suite_report
    #
    # Add the given suite to the top level of the current test execution
    #
    # test: Any Robot object part of the current test execution
    # result_suite: Robot suite to report on
    #
    # Return: None
    #####################

    def _inject_suite_report(self, test, result_suite):
        traveller = test.parent
        while traveller.parent is not None:
            traveller = traveller.parent

        traveller.suites.append(result_suite)

        test.parent.tests = [
            sibling for sibling in test.parent.tests if sibling is not test]

    #####################
    # _normalize_keyword_name
    #
    # Convert a given full keyword name into snake-case simple name (a_b_c)
    #
    # keyword_name: The raw keyword name (suite.suite.My Keyword)
    #
    # Return: The normalized keyword name
    #####################

    def _normalize_keyword_name(self, keyword_name):
        short_name = str(keyword_name).split('.')[-1]
        underscored = re.sub(r' +', '_', short_name)
        return underscored.lower()

    #####################
    # _set_suite_tags
    #
    # Set the given tags for the given suite
    #
    # suite: Robot suite
    # tags: List of tag strings
    #
    # Return: The updated Robot suite
    #####################

    def _set_suite_tags(self, suite, *tags):
        suite.set_tags(tags)
        return suite

    #####################
    # _build_suite
    #
    # Convert a given suite dict into a Robot suite
    #
    # suite: Suite dict
    #
    # Return: A Robot suite
    #####################

    def _build_suite(self, suite):
        robot_suites = self._build_suites([], suite)
        return robot_suites[0]

    #####################
    # _build_suites
    #
    # Convert a set of suite dicts into Robot suites and append them to the
    # given list-like object
    #
    # target: List-like object to add the Robot suites to
    # suites: Set of suite dicts to build into Robot suites
    #
    # Return: The updated list-like object
    #####################

    def _build_suites(self, target, *suites):
        for suite in suites:
            robot_suite = RobotSuite(suite['name'])
            robot_suite.set_tags(suite['tags'])

            self._build_keywords(robot_suite.keywords, *suite['setup'])
            self._build_keywords(robot_suite.keywords, *suite['teardown'])
            self._build_suites(robot_suite.suites, *suite['suites'])
            self._build_tests(robot_suite.tests, *suite['tests'])

            target.append(robot_suite)

        return target

    #####################
    # _build_tests
    #
    # Convert a set of test dicts and add them as sub-tests to a Robot suite
    #
    # target: Robot suite to add the tests to
    # tests: Set of test dicts to build into Robot tests
    #
    # Return: The finished Robot suite
    #####################

    def _build_tests(self, target, *tests):
        for test in tests:
            robot_test = RobotTest(test['name'])
            robot_test.tags = test['tags']

            self._build_keywords(robot_test.keywords, *test['setup'])
            self._build_keywords(robot_test.keywords, *test['keywords'])
            self._build_keywords(robot_test.keywords, *test['teardown'])

            robot_test.status = self._keywords_status(robot_test.keywords)

            target.append(robot_test)

        return target

    #####################
    # _build_keywords
    #
    # Convert a set of keyword dicts and add them as sub-keywords to a Robot object
    #
    # target: The Robot object
    # keywords: Set of keyword dicts
    #
    # Return: The finished Robot object
    #####################

    def _build_keywords(self, target, *keywords):
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

    #####################
    # _build_messages
    #
    # Add the given messages to a Robot object.
    #
    # target: The keyword to append to
    # messages: The set of message strings to add to the Robot object
    #
    # Return: The finished Robot object
    #####################

    def _build_messages(self, target, *messages):
        for message in messages:
            target.append(RobotMessage(message))

        return target

    #####################
    # _robot_keywords
    #
    # Take a list of keyword dicts and create Robot keywords from them, passing
    # given kwargs to _robot_keyword for each
    #
    # keywords: List of keyword dicts
    # kwargs: _robot_keyword parameters
    #
    # Return: The Robot keywords
    #####################

    def _robot_keywords(self, *keywords, **kwargs):
        return_keywords = []
        for keyword in keywords:
            return_keywords.append(self._robot_keyword(
                existing=keyword,
                **kwargs,
            ))
        return return_keywords

    #####################
    # _robot_keyword
    #
    # Create a new Robot keyword with specified data.
    #
    # name: Keyword name
    # tags: List of keyword tag strings
    # passed: Whether the keyword passed execution
    # setup: True if this is a setup keyword (takes precedence over teardown
    # and normal
    # teardown: True if this is a teardown keyword (takes precedence over normal
    # default_type: True to set the keyword type to normal keyword
    # existing: If a Robot keyword is passed as existing, all the other work
    # is done to update the existing keyword rather than create a new one
    # elapsed: Time spent executing the keyword
    # keywords: Sub-keywords for the keyword itself
    #
    # Return: The finished keyword
    #####################

    def _robot_keyword(self, name=None, tags=None, passed=None, setup=False, teardown=False, default_type=False, existing=None, elapsed=None, keywords=None):
        if existing:
            keyword = existing
        elif name:
            keyword = self._create_with_time(name, int(elapsed or 0.0))
        else:
            return None

        if tags:
            keyword.tags = tags

        # Determine keyword type based on parameters. Note that KEYWORD_TYPE is not
        # default behaviour (consider the case of updating an existing keyword)
        if setup:
            keyword.type = RobotKeyword.SETUP_TYPE
        elif teardown:
            keyword.type = RobotKeyword.TEARDOWN_TYPE
        elif default_type and keyword.type in [RobotKeyword.SETUP_TYPE, RobotKeyword.TEARDOWN_TYPE]:
            keyword.type = RobotKeyword.KEYWORD_TYPE

        if keywords:
            keyword.keywords = keywords

        # If the status is not forced by parameter, investigate the sub-keywords,
        # if any
        if passed is None:
            keyword.status = self._keywords_status(keywords or [])
        elif passed:
            keyword.status = 'PASS'
        else:
            keyword.status = 'FAIL'

        return keyword

    #####################
    # _create_with_time
    #
    # Create a keyword with the given name, duration and start time.
    #
    # keyword_name: Keyword name to give the new object
    # elapsed: Milliseconds of test duration
    # starttime: A time object corresponding to start time. If not given,
    # current time will be used
    #
    # Return: The finished keyword
    #####################

    def _create_with_time(self, keyword_name, elapsed, starttime=None):
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

    #####################
    # _get_time_format
    #
    # Convenience to return the general Robot timestamp format.
    #
    # Return: The general Robot timestamp format
    #####################

    def _get_time_format(self):
        return '%Y%m%d %H:%M:%S.%f'

    #####################
    # _get_from_timestamp
    #
    # Get the time object built from a Robot timestamp. Convenience method hiding
    # the normal Robot timestamp format.
    #
    # timestamp: A timestamp from Robot test execution
    #
    # Return: The time object representing the timestamp
    #####################

    def _get_from_timestamp(self, timestamp):
        time_object = datetime.strptime(
            timestamp,
            self._get_time_format(),
        )

        return time_object

    #####################
    # _keywords_status
    #
    # Shorthand for checking if a set of keywords is PASS or FAIL. To PASS, every
    # keyword in the list must pass.
    #
    # keywords: List of Robot keywords
    #
    # Return: 'PASS' or 'FAIL'
    #####################

    def _keywords_status(self, keywords):
        if sum(not kw.passed for kw in keywords):
            return 'FAIL'
        else:
            return 'PASS'
