from datetime import datetime
from datetime import timedelta
from datetime import timezone
from robot.result.model import (Keyword as RobotResultKeyword,
                                Message as RobotResultMessage,
                                TestCase as RobotResultTest,
                                TestSuite as RobotResultSuite)

from robot.running.model import TestSuite as RobotRunningSuite


class RobotResultInterface(object):
    def build_suites(self, starting_time, *suites):
        '''Convert a given `suite` dictionaries into a Robot suite'''
        finished_suites = []
        current_time = starting_time

        for suite in suites:
            current_time, finished_suite = self.build_suite(current_time, suite)

            if finished_suite:
                finished_suites.append(finished_suite)

        return current_time, finished_suites


    def build_suite(self, starting_time, suite):
        '''Convert a set of suite dicts into Robot suites and append them to the
        given list-like object

        target: List-like object to add the Robot suites to
        suites: Set of suite dicts to build into Robot suites

        Return: The updated list-like object
        '''

        if not suite:
            return starting_time, None

        updated_time = starting_time
        name = suite.get('name') or 'Unknown Suite Name'
        tags = suite.get('tags') or []
        setup_keyword = suite.get('setup') or None
        teardown_keyword = suite.get('teardown') or None
        child_suites = suite.get('suites') or []
        tests = suite.get('tests') or []
        metadata = suite.get('metadata') or {}

        updated_time, robot_setup = self.build_keyword(updated_time, setup_keyword, setup=True)
        updated_time, robot_teardown = self.build_keyword(updated_time, teardown_keyword, teardown=True)
        updated_time, robot_suites = self.build_suites(updated_time, *child_suites)
        updated_time, robot_tests = self.build_tests(updated_time, *tests)

        robot_suite = self.spawn_robot_suite(name,
                                             starting_time,
                                             updated_time,
                                             tags,
                                             robot_setup,
                                             robot_teardown,
                                             robot_suites,
                                             robot_tests,
                                             metadata)

        return updated_time, robot_suite


    def spawn_robot_suite(self,
                          name,
                          start_time,
                          end_time,
                          tags,
                          setup_keyword,
                          teardown_keyword,
                          suites,
                          tests,
                          metadata):
        start_timestamp = self.ms_to_timestamp(start_time)
        end_timestamp = self.ms_to_timestamp(end_time)

        robot_suite = RobotResultSuite(name,
                                 starttime=start_timestamp,
                                 endtime=end_timestamp,
                                 metadata=metadata)
        robot_suite.set_tags(add=tags, persist=True)

        if setup_keyword:
            robot_suite.keywords.append(setup_keyword)
        if teardown_keyword:
            robot_suite.keywords.append(teardown_keyword)

        for suite in filter(None, suites):
            robot_suite.suites.append(suite)

        for test in filter(None, tests):
            robot_suite.tests.append(test)

        return robot_suite


    def build_tests(self, starting_time, *tests):
        '''Convert a set of `tests` dicts and add to a Robot suite `target`'''
        updated_time = starting_time
        robot_tests = []
        for test in tests:
            updated_time, robot_test = self.build_test(updated_time, test)

            if robot_test:
                robot_tests.append(robot_test)

        return updated_time, robot_tests


    def build_test(self, starting_time, test):
        '''Convert a set of `tests` dicts and add to a Robot suite `target`'''
        if not test:
            return starting_time, None

        updated_time = starting_time
        test_name = test.get('name') or 'Unknown Test Name'
        tags = test.get('tags') or []
        setup_keyword = test.get('setup') or None
        keywords = test.get('keywords') or []
        teardown_keyword = test.get('teardown') or None

        updated_time, robot_setup = self.build_keyword(updated_time,
                                                       setup_keyword,
                                                       setup=True)
        updated_time, robot_keywords = self.build_keywords(updated_time,
                                                           *keywords)
        updated_time, robot_teardown = self.build_keyword(updated_time,
                                                          teardown_keyword,
                                                          teardown=True)

        robot_test = self.spawn_robot_test(test_name,
                                           starting_time,
                                           updated_time,
                                           tags,
                                           robot_setup,
                                           robot_teardown,
                                           robot_keywords)

        return updated_time, robot_test


    def spawn_robot_test(self,
                         name,
                         start_time,
                         end_time,
                         tags,
                         setup_keyword,
                         teardown_keyword,
                         keywords):
        start_timestamp = self.ms_to_timestamp(start_time)
        end_timestamp = self.ms_to_timestamp(end_time)
        status = self.get_keywords_status(setup_keyword, teardown_keyword, *(keywords or []))

        robot_test = RobotResultTest(name,
                               tags=tags,
                               status=status,
                               starttime=start_timestamp,
                               endtime=end_timestamp)

        if setup_keyword:
            robot_test.keywords.append(setup_keyword)
        for keyword in keywords:
            if keyword:
                robot_test.keywords.append(keyword)
        if teardown_keyword:
            robot_test.keywords.append(teardown_keyword)

        return robot_test


    def build_keywords(self, starting_time, *keywords):
        '''Convert `keywords` dicts, add them as sub-keywords to a `target`'''
        updated_time = starting_time
        robot_keywords = []
        for keyword in keywords:
            updated_time, robot_keyword = self.build_keyword(updated_time, keyword)

            if robot_keyword:
                robot_keywords.append(robot_keyword)

        return updated_time, robot_keywords


    def build_keyword(self, starting_time, keyword, setup=False, teardown=False):
        if not keyword:
            return starting_time, None

        updated_time = starting_time
        name = keyword.get('name') or 'Unknown Keyword Name'
        status = keyword.get('pass') or None
        elapsed = keyword.get('elapsed') or 0.0
        tags = keyword.get('tags') or []
        messages = keyword.get('messages') or []
        teardown = keyword.get('teardown') or None
        keywords = keyword.get('keywords') or []

        updated_time, robot_teardown = self.build_keyword(updated_time, teardown)
        updated_time, robot_keywords = self.build_keywords(updated_time, keywords)

        final_time = updated_time + elapsed

        robot_keyword = self.spawn_robot_keyword(name,
                                                 tags,
                                                 status,
                                                 updated_time,
                                                 final_time,
                                                 teardown,
                                                 keywords,
                                                 messages,
                                                 setup,
                                                 teardown)

        return final_time, robot_keyword


    def spawn_robot_keyword(self,
                            name,
                            tags,
                            status,
                            start_time,
                            end_time,
                            teardown_keyword,
                            keywords,
                            messages,
                            setup=False,
                            teardown=False):
        start_timestamp = self.ms_to_timestamp(start_time)
        end_timestamp = self.ms_to_timestamp(end_time)

        if setup:
            keyword_type = RobotResultKeyword.SETUP_TYPE
        elif teardown:
            keyword_type = RobotResultKeyword.TEARDOWN_TYPE
        else:
            keyword_type = RobotResultKeyword.KEYWORD_TYPE

        if status is None:
            keyword_status = 'NOT_RUN'
        elif status:
            keyword_status = 'PASS'
        else:
            keyword_status = 'FAIL'

        robot_keyword = RobotResultKeyword(name,
                                     tags=tags,
                                     status=keyword_status,
                                     starttime=start_timestamp,
                                     endtime=end_timestamp)

        robot_keyword.type = keyword_type

        for keyword in keywords:
            if keyword:
                robot_keyword.keywords.append(keyword)

        if teardown_keyword:
            robot_keyword.keywords.append(teardown_keyword)

        for message in messages:
            if message:
                ishtml = message.startswith('*HTML*')
                if ishtml:
                  message = message[6:]
                robot_keyword.messages.append(RobotResultMessage(message,html=ishtml))

        return robot_keyword


    def get_time_format(self):
        '''Convenience to return the general Robot timestamp format.'''
        return '%Y%m%d %H:%M:%S.%f'


    def timestamp_to_ms(self, timestamp):
        time_format = self.get_time_format()
        time_object = datetime.strptime(
            timestamp,
            time_format,
        )

        tz_delta = self.get_timezone_delta()

        milliseconds = ((time_object + tz_delta).timestamp() * 1000)

        return milliseconds


    def ms_to_timestamp(self, milliseconds):
        tz_delta = self.get_timezone_delta()

        time_object = datetime.fromtimestamp(int(milliseconds / 1000)) - tz_delta
        if time_object.year < 1970:
            time_object = datetime.fromtimestamp(0)
        # fromtimestamp() loses milliseconds, add them back
        milliseconds_delta = timedelta(milliseconds=(milliseconds % 1000))
        time_object = (time_object + milliseconds_delta)

        time_format = self.get_time_format()

        return time_object.strftime(time_format)


    def get_timezone_delta(self):
        local_zone = datetime.now(timezone.utc).astimezone().tzinfo
        return local_zone.utcoffset(None)


    def get_keywords_status(self, *keywords):
        '''
        keywords: List of Robot keywords

        Return: 'PASS' or 'FAIL'
        '''
        if sum(not kw.passed for kw in filter(None, keywords)):
            return 'FAIL'
        else:
            return 'PASS'


    def create_wrapper_keyword(self,
                               name,
                               start_timestamp,
                               end_timestamp,
                               setup,
                               *keywords):
        status = self.get_keywords_status(*keywords)
        start_time = self.timestamp_to_ms(start_timestamp)
        end_time = self.timestamp_to_ms(end_timestamp)

        robot_keyword = self.spawn_robot_keyword(name,
                                                 [],
                                                 status,
                                                 start_time,
                                                 end_time,
                                                 None,
                                                 keywords,
                                                 [],
                                                 setup,
                                                 (not setup))

        return robot_keyword


class RobotRunningInterface(object):
    def build_suite(self, parsed_results):
        robot_root_suite = RobotRunningSuite(
            parsed_results['name'],
            metadata=parsed_results.get('metadata', {})
        )
        for parsed_suite in parsed_results.get('suites', []):
            robot_suite = robot_root_suite.suites.create(
                parsed_suite['name'],
                metadata=parsed_results.get('metadata', {})
            )
            for subsuite in parsed_suite.get('suites', []):
                robot_subsuite = self.build_suite(subsuite)
                robot_suite.suites.append(robot_subsuite)
            self.build_tests(parsed_suite, robot_suite)
        self.build_tests(parsed_results, robot_root_suite)
        return robot_root_suite

    def build_tests(self, oxygen_suite, robot_suite):
        for parsed_test in oxygen_suite.get('tests', []):
            name = parsed_test['name']
            tags = parsed_test.get('tags', [])
            kw = parsed_test['keywords'][0]
            msg = '\n'.join(kw.get('messages', []))
            test_robot_counterpart = robot_suite.tests.create(name, tags=tags)
            if kw['pass']:
                args = [msg if msg else 'Test passed :D']
                test_robot_counterpart.keywords.create('Pass execution',
                                                       args=args)
            else:
                args = [msg if msg else 'Test failed D:']
                test_robot_counterpart.keywords.create('Fail', args=args)
