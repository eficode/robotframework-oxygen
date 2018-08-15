from robot.api import SuiteVisitor
from yaml import load

from .config import CONFIG_FILE

class OxygenCore(object):

    def __init__(self):
        with open(CONFIG_FILE, 'r') as infile:
            self._config = load(infile)
        self._handlers = {}
        self._register_handlers()

    def _register_handlers(self):
        for tool_name, config in self._config.items():
            handler_class = getattr(__import__(tool_name,
                                               fromlist=[config['handler']]),
                                    config['handler'])
            handler = handler_class(config)
            self._handlers[tool_name] = handler


class Oxygen(OxygenCore, SuiteVisitor):
    """Read up on what is Robot Framework SuiteVisitor:
    http://robot-framework.readthedocs.io/en/latest/autodoc/robot.model.html#module-robot.model.visitor
    """
    def visit_test(self, test):
        for handler_type, handler in self._handlers.items():
            handler.check_for_keyword(test)


class OxygenLibrary(OxygenCore):
    """Read up on what is Robot Framework dynamic library:
    http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
    """
    def get_keyword_names(self):
        return [handler.get_keyword() for handler in self._handlers.values()]

    def run_keyword(self, name, args):
        """
        If Robot tests feature one of the mock Oxygen keywords, make sure
        running it can mock-succeed
        """
        keywords = [handler.get_keyword() for handler in self._handlers.values()]
        assert(name in keywords)
