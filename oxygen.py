from argparse import ArgumentParser

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
        return [handler.get_keyword() for handler in self._handlers.values()]

    def run_keyword(self, name, args):
        """
        If Robot tests feature one of the mock Oxygen keywords, make sure
        running it can mock-succeed
        """
        keywords = [handler.get_keyword() for handler in self._handlers.values()]
        assert(name in keywords)


if __name__ == '__main__':
    parser = ArgumentParser()
    subcommands = parser.add_subparsers()
    for tool_name, tool_handler in OxygenCore()._handlers.items():
        subcommand_parser = subcommands.add_parser(tool_name)
        for flags, params in tool_handler.cli().iteritems():
            subcommand_parser.add_argument(*flags, **params)
    args = parser.parse_args()
    print args
