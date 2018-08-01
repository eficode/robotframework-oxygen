from gatling import GatlingHandler
from junit import JUnitHandler
#from zaproxy import ZAProxyHandler

from robot.api import SuiteVisitor
from yaml import load


class OxygenCore(object):
    #####################
    # __init__
    #
    # Build the core Oxygen object
    #
    # Return: N/A
    #####################
    def __init__(self):
        with open('config.yml', 'r') as infile:
            self._config = load(infile)
        self._register_handlers()

    #####################
    # _register_handlers
    #
    # Create a handler for each supported type
    #
    # Return: None
    #####################

    def _register_handlers(self):
        self._handlers = {
            'gatling': GatlingHandler(),
            'junit': JUnitHandler(),
            # 'zap': ZAProxyHandler(),
        }

        for config_type, config in self._config.items():
            self._handlers[config_type].build(config)


class Oxygen(OxygenCore, SuiteVisitor):
    #####################
    # visit_test
    #
    # Basic Robot test visitor
    #
    # test: for-each executing Robot test
    #
    # Return: N/A
    #####################
    def visit_test(self, test):
        for handler_type, handler in self._handlers.items():
            handler.check(test)


class OxygenLibrary(OxygenCore):
    #####################
    # get_keyword_names
    #
    # Get the trigger keyword for each handler to avoid errors in Robot execution
    #
    # Return: The set of trigger keywords
    #####################
    def get_keyword_names(self):
        return [handler.get_keyword() for name, handler in self._handlers.items()]

    #####################
    # run_keyword
    #
    # If Robot tests feature one of the mock Oxygen keywords, make sure running it
    # can mock-succeed
    #
    # Return: None
    #####################

    def run_keyword(self, name, args):
        keywords = [handler.get_keyword()
                    for handler_type, handler in self._handlers.items()]
        assert(name in keywords)
