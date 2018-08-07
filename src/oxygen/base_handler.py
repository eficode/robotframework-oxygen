import re

from .robot_interface import RobotInterface

class BaseHandler(object):
    def __init__(self, config):
        """
        Set up the handler with the given configuration

        config: A dict including the 'keyword' node
        """
        self._interface = RobotInterface()
        self._config = config

        tags = self._config.get('tags', [])
        if not isinstance(tags, list):
            tags = [tags]
        self._tags = tags

        keyword = self._config['keyword']
        self._keyword = self._normalize_keyword_name(keyword)


    def get_keyword(self):
        return self._keyword


    def check_for_keyword(self, test):
        """Check if any of the keywords directly under this test trigger test
        execution

        test: A Robot test
        """
        for curr, keyword in enumerate(test.keywords):
            keyword_name = self._normalize_keyword_name(keyword.name)
            if not (keyword_name == self._keyword):
                continue

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
        setup_keyword = self._interface.spawn_robot_keyword(
            'Oxygen Setup',
            [],
            'PASS',
            0,
            5000000,
            None,
            setup_keywords,
            [],
            setup=True
        )
        teardown_keyword = self._interface.spawn_robot_keyword(
            'Oxygen Teardown',
            [],
            'PASS',
            6000000,
            15000000,
            None,
            teardown_keywords,
            [],
            teardown=True
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
        end_time, result_suite = self._interface.build_suite(100000, test_results)
        self._set_suite_tags(result_suite, *(self._tags + list(test.tags)))
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
        short_name = str(keyword_name).split('.')[-1].strip()
        underscored = re.sub(r' +', '_', short_name)
        return underscored.lower()

    def _set_suite_tags(self, suite, *tags):
        suite.set_tags(tags)
        return suite

