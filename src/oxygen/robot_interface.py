from datetime import datetime
from datetime import timedelta
from robot.result.model import Keyword as RobotKeyword
from robot.result.model import Message as RobotMessage
from robot.result.model import TestCase as RobotTest
from robot.result.model import TestSuite as RobotSuite

class RobotInterface(object):
    def build_suites(starting_time, *suites):
        """Convert a given `suite` dict into a Robot suite"""
        finished_suites = []
        current_time = starting_time
        
        for suite in suites:
            current_time, finished_suite = build_suite(current_time, suite)
            finished_suites.append(finished_suite)
          
        return current_time, finished_suites


    def build_suite(starting_time, suite):
        """Convert a set of suite dicts into Robot suites and append them to the
        given list-like object

        target: List-like object to add the Robot suites to
        suites: Set of suite dicts to build into Robot suites

        Return: The updated list-like object
        """
        
        if not suite:
          return starting_time, None
        
        updated_time = starting_time
        name = suite.get('name') or 'Unknown Suite Name'
        tags = suite.get('tags') or []
        setup_keyword = suite.get('setup') or None
        teardown_keyword = suite.get('teardown') or None
        child_suites = suite.get('suites') or []
        tests = suite.get('tests') or []
        
        updated_time, robot_setup = build_keyword(updated_time, setup_keyword, setup=True)
        updated_time, robot_teardown = build_keyword(updated_time, teardown_keyword, teardown=True)
        updated_time, robot_suites = build_suites(updated_time, *child_suites)
        updated_time, robot_tests = build_tests(updated_time, *tests)
        
        robot_suite = spawn_robot_suite(name,
                                        starting_time,
                                        updated_time,
                                        tags,
                                        robot_setup,
                                        robot_teardown,
                                        robot_suites,
                                        robot_tests)
                                        
        return updated_time, robot_suite
        
        
    def spawn_robot_suite(name,
                          start_time,
                          end_time,
                          tags,
                          setup_keyword,
                          teardown_keyword,
                          suites,
                          tests):
        start_timestamp = ms_to_timestamp(start_time)
        end_timestamp = ms_to_timestamp(end_time)
        
        robot_suite = RobotSuite(name,
                                 starttime=start_timestamp,
                                 endtime=end_timestamp)
        robot_suite.set_tags(add=tags, persist=True)
        robot_suite.keywords.append(setup_keyword)
        robot_suite.keywords.append(teardown_keyword)
        robot_suite.suites = suites
        robot_suite.tests = tests

        return robot_suite        


    def build_tests(starting_time, *tests):
        """Convert a set of `tests` dicts and add to a Robot suite `target`"""
        updated_time = starting_time
        robot_tests = []        
        for test in tests:
            updated_time, robot_test = build_test(updated_time, test)
            robot_tests.append(robot_test)

        return updated_time, robot_tests


    def build_test(starting_time, test):
        """Convert a set of `tests` dicts and add to a Robot suite `target`"""
        if not test:
            return starting_time, None
        
        updated_time = starting_time
        test_name = test.get('name') or 'Unknown Test Name'
        tags = test.get('tags') or []
        setup_keyword = test.get('setup') or None
        keywords = test.get('keywords') or []
        teardown_keyword = test.get('teardown') or None

        updated_time, robot_setup = build_keyword(updated_time, setup_keyword, setup=True)
        updated_time, robot_keywords = build_keywords(updated_time, *keywords)
        updated_time, robot_teardown = build_keyword(updated_time, teardown_keyword, teardown=True)

        robot_test = spawn_robot_test(name,
                                      starting_time,
                                      updated_time,
                                      tags,
                                      robot_setup,
                                      robot_teardown,
                                      robot_keywords)

        return updated_time, robot_test
        
        
    def spawn_robot_test(name,
                         start_time,
                         end_time,
                         tags,
                         setup_keyword,
                         teardown_keyword,
                         keywords):
        start_timestamp = ms_to_timestamp(start_time)
        end_timestamp = ms_to_timestamp(end_time)
        status = get_keywords_status(setup_keyword, teardown_keyword, keywords)
        
        robot_test = RobotTest(name,
                               tags=tags,
                               status=status,
                               starttime=start_timestamp,
                               endtime=end_timestamp)
        robot_test.keywords.append(setup_keyword)
        robot_test.keywords.append(keywords)
        robot_test.keywords.append(teardown_keyword)

        return robot_test
          

    def build_keywords(starting_time, *keywords):
        """Convert `keywords` dicts, add them as sub-keywords to a `target`"""
        updated_time = starting_time
        robot_keywords = []        
        for keyword in keywords:
            updated_time, robot_keyword = build_keyword(updated_time, keyword)
            robot_keywords.append(robot_keyword)

        return updated_time, robot_keywords
        
        
    def build_keyword(starting_time, keyword, setup=False, teardown=False):
        updated_time = starting_time
        name = keyword.get('name') or 'Unknown Keyword Name'
        status = keyword.get('pass') or None
        elapsed = keyword.get('elapsed') or 0.0
        tags = keyword.get('tags') or []
        messages = keyword.get('messages') or []
        teardown = keyword.get('teardown') or None
        keywords = keyword.get('keywords') or []
        
        updated_time, robot_teardown = build_keyword(updated_time, teardown)
        updated_time, robot_keywords = build_keywords(updated_time, keywords)
        
        final_time = updated_time + elapsed
        
        robot_keyword = spawn_robot_keyword(name,
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
        
        
    def spawn_robot_keyword(name,
                            tags,
                            status,
                            start_time,
                            end_time,
                            teardown_keyword,
                            keywords,
                            messages,
                            setup=False,
                            teardown=False):
        start_timestamp = ms_to_timestamp(start_time)
        end_timestamp = ms_to_timestamp(end_time)
        
        if setup:
          keyword_type = RobotKeyword.SETUP_TYPE
        elif teardown:
          keyword_type = RobotKeyword.TEARDOWN_TYPE
        else:
          keyword_type = RobotKeyword.KEYWORD_TYPE
          
        if status is None:
          keyword_status = 'NOT_RUN'
        elif status:
          keyword_status = 'PASS'
        else:
          keyword_status = 'FAIL'
        
        robot_keyword = RobotKeyword(name,
                                     tags=tags,
                                     status=keyword_status,
                                     starttime=start_time,
                                     endtime=end_time)
                                     
        robot_keyword.type = keyword_type
        robot_keyword.keywords.append(keywords)
        robot_keyword.keywords.append(teardown_keyword)
        robot_keywords.messages.append(messages)
                                     
        return robot_keyword
        

    def build_messages(target, *messages):
        for message in messages:
            target.append(RobotMessage(message))

        return target
        

    def get_time_format():
        """Convenience to return the general Robot timestamp format."""
        return '%Y%m%d %H:%M:%S.%f'


    def timestamp_to_ms(timestamp):
        time_format = get_time_format()
        time_object = datetime.strptime(
            timestamp,
            time_format,
        )

        milliseconds = (time_object.timestamp() * 1000) + (time_object.microsecond / 1000)

        return time_object.timestamp()


    def ms_to_timestamp(milliseconds):
        time_object = datetime.fromtimestamp(int(milliseconds / 1000))
        time_object.microsecond = int((milliseconds % 1000) * 1000)
        time_format = get_time_format()

        return time_object.strftime(time_format)


    def get_keywords_status(*keywords):
        """
        keywords: List of Robot keywords

        Return: 'PASS' or 'FAIL'
        """
        if sum(not kw.passed for kw in keywords):
            return 'FAIL'
        else:
            return 'PASS'
