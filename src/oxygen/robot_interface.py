from robot.version import get_version as robot_version


class RobotInterface(object):
    def __init__(self):
        major_version = int(robot_version().split('.')[0])

        if major_version > 3:
            from .robot4_interface import (RobotResultInterface,
                                           RobotRunningInterface)
        else:
            from .robot3_interface import (RobotResultInterface,
                                           RobotRunningInterface)

        self.result = RobotResultInterface()
        self.running = RobotRunningInterface()


def get_keywords_from(test):
    if hasattr(test, 'body'):
        return test.body.filter(keywords=True)
    return test.keywords


def set_special_keyword(suite, keyword_type, keyword):
    if hasattr(suite, keyword_type):
        if keyword_type == 'setup':
            suite.setup = keyword
        elif keyword_type == 'teardown':
            suite.teardown = keyword
    else:
        suite.keywords.append(keyword)
