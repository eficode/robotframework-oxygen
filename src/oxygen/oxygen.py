from argparse import ArgumentParser
from datetime import datetime, timedelta
from inspect import signature
from io import StringIO
from pathlib import Path
from traceback import format_exception

from robot.api import ExecutionResult, ResultVisitor, ResultWriter
from robot.libraries.BuiltIn import BuiltIn
from yaml import load, FullLoader

from .config import CONFIG_FILE
from .errors import OxygenException
from .robot_interface import RobotInterface
from .version import VERSION


class OxygenCore(object):
    __version__ = VERSION


    def __init__(self):
        with open(CONFIG_FILE, 'r') as infile:
            self._config = load(infile, Loader=FullLoader)
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
    def __init__(self, data):
        super().__init__()
        self.data = data

    def visit_test(self, test):
        failures = []
        for handler_type, handler in self._handlers.items():
            try:
                handler.check_for_keyword(test, self.data)
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


class listener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.run_time_data = {}

    def end_test(self, name, attributes):
        lib = BuiltIn().get_library_instance('oxygen.OxygenLibrary')
        if lib:
            self.run_time_data[attributes['longname']] = lib.data

    def output_file(self, path):
        result = ExecutionResult(path)
        result.visit(OxygenVisitor(self.run_time_data))
        result.save()


class OxygenLibrary(OxygenCore):
    """Read up on what is Robot Framework dynamic library:
    http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
    """

    def __init__(self):
        super().__init__()
        self.data = None

    def _fetch_handler(self, name):
        try:
            return next(filter(lambda h: h.keyword == name,
                               self._handlers.values()))
        except StopIteration:
            raise OxygenException('No handler for keyword "{}"'.format(name))

    def get_keyword_names(self):
        return list(handler.keyword for handler in self._handlers.values())

    def run_keyword(self, name, args, kwargs):
        handler = self._fetch_handler(name)
        retval = getattr(handler, name)(*args, **kwargs)
        self.data = retval
        return retval

    def get_keyword_documentation(self, kw_name):
        if kw_name == '__intro__':
            return self.__class__.__doc__
        return getattr(self._fetch_handler(kw_name), kw_name).__doc__

    def get_keyword_arguments(self, kw_name):
        method_sig = signature(getattr(self._fetch_handler(kw_name), kw_name))
        return [str(param) for param in method_sig.parameters.values()]

class OxygenCLI(OxygenCore):
    def parse_args(self, parser):
        subcommands = parser.add_subparsers()
        for tool_name, tool_handler in self._handlers.items():
            subcommand_parser = subcommands.add_parser(tool_name)
            for flags, params in tool_handler.cli().items():
                subcommand_parser.add_argument(*flags, **params)
                subcommand_parser.set_defaults(func=tool_handler.parse_results)
        return parser.parse_args()

    def get_output_filename(self, resultfile):
        filename = Path(resultfile)
        filename = filename.with_suffix('.xml')
        robot_name = filename.stem + '_robot_output' + filename.suffix
        filename = filename.with_name(robot_name)
        return str(filename)

    def run(self):
        parser = ArgumentParser(prog='oxygen')
        parser.add_argument('--version',
                            action='version',
                            version=f'%(prog)s {self.__version__}')
        args = self.parse_args(parser)
        if not vars(args):
            parser.error('No arguments given')
        output_filename = self.get_output_filename(args.resultfile)
        parsed_results = args.func(args.resultfile)
        robot_suite = RobotInterface().running.build_suite(parsed_results)
        robot_suite.run(output=output_filename,
                        log=None,
                        report=None,
                        stdout=StringIO())


if __name__ == '__main__':
    OxygenCLI().run()
