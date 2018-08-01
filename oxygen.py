from gatling import GatlingHandler
from junit import JUnitHandler
#from zaproxy import ZAProxyHandler

from robot.api import SuiteVisitor
from yaml import load


class OxygenCore(object):

    def __init__(self):
        with open('config.yml', 'r') as infile:
            self._config = load(infile)
        self._register_handlers()

    def _register_handlers(self):
        self._handlers = {
            'gatling': GatlingHandler(),
            'junit': JUnitHandler(),
            # 'zap': ZAProxyHandler(),
        }

        for config_type, config in self._config.items():
            self._handlers[config_type].build(config)


class Oxygen(OxygenCore, SuiteVisitor):
    """Read up on what is Robot Framework SuiteVisitor:
    http://robot-framework.readthedocs.io/en/latest/autodoc/robot.model.html#module-robot.model.visitor
    """
    def visit_test(self, test):
        for handler_type, handler in self._handlers.items():
            handler.check(test)


class OxygenLibrary(OxygenCore):
    """Read up on what is Robot Framework dynamic library:
    http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
    """
    def get_keyword_names(self):
        return [handler.get_keyword() for name, handler in self._handlers.items()]

    def run_keyword(self, name, args):
        """
        If Robot tests feature one of the mock Oxygen keywords, make sure
        running it can mock-succeed
        """
        keywords = [handler.get_keyword()
                    for handler_type, handler in self._handlers.items()]
        assert(name in keywords)
