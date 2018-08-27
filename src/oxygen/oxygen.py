from argparse import ArgumentParser
from inspect import signature
from traceback import format_exception

from robot.api import ExecutionResult, ResultVisitor
from yaml import load

from .config import CONFIG_FILE
from .errors import OxygenException

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


class OxygenVisitor(OxygenCore, ResultVisitor):
    """Read up on what is Robot Framework SuiteVisitor:
    http://robot-framework.readthedocs.io/en/latest/autodoc/robot.model.html#module-robot.model.visitor
    """
    def visit_test(self, test):
        failures = []
        for handler_type, handler in self._handlers.items():
            try:
                handler.check_for_keyword(test)
            except Exception as e:
                failures.append(e)
        if len(failures) == 1:
            raise failures.pop()
        if failures:
            tracebacks = [''.join(format_exception(e.__class__,
                                                   e,
                                                   e.__traceback__))
                          for e in failures]
            raise OxygenException('Multiple failures:\n{}'.format(
                '\n'.join(tracebacks)))


class Oxygen(object):
    ROBOT_LISTENER_API_VERSION = 3

    def output_file(self, path):
        result = ExecutionResult(path)
        result.visit(OxygenVisitor())
        result.save()


class OxygenLibrary(OxygenCore):
    """Read up on what is Robot Framework dynamic library:
    http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
    """
    LIBRARY_INITIALIZATION_DOC = '''Hello world'''

    def _fetch_handler(self, name):
        try:
            return next(filter(lambda h: h.keyword == name,
                               self._handlers.values()))
        except StopIteration:
            raise OxygenException('No handler for keyword "{}"'.format(name))

    def get_keyword_names(self):
        return list(handler.keyword for handler in self._handlers.values())

    def run_keyword(self, name, args, kwargs):
        return getattr(self._fetch_handler(name), name)(*args, **kwargs)

    def get_keyword_documentation(self, kw_name):
        if kw_name == '__intro__':
            return self.__class__.__doc__
        if kw_name == '__init__':
            return self.LIBRARY_INITIALIZATION_DOC
        return getattr(self._fetch_handler(kw_name), kw_name).__doc__

    def get_keyword_arguments(self, kw_name):
        method_sig = signature(getattr(self._fetch_handler(kw_name), kw_name))
        return [str(param) for param in method_sig.parameters.values()]

if __name__ == '__main__':
    parser = ArgumentParser()
    subcommands = parser.add_subparsers()
    for tool_name, tool_handler in OxygenCore()._handlers.items():
        subcommand_parser = subcommands.add_parser(tool_name)
        for flags, params in tool_handler.cli().iteritems():
            subcommand_parser.add_argument(*flags, **params)
    args = parser.parse_args()
    print(args)
