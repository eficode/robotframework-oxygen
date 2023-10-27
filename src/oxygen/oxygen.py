import sys

from argparse import ArgumentParser
from datetime import datetime, timedelta
from inspect import getdoc, signature
from io import StringIO
from pathlib import Path
from shutil import copy as copy_file
from traceback import format_exception

from robot.api import ExecutionResult, ResultVisitor, ResultWriter
from robot.libraries.BuiltIn import BuiltIn
from robot.errors import DataError
from yaml import load, FullLoader, dump as dump_yaml

from .config import CONFIG_FILE, ORIGINAL_CONFIG_FILE
from .errors import (OxygenException,
                     InvalidConfigurationException,
                     ResultFileNotFoundException)
from .robot_interface import RobotInterface
from .utils import validate_with_deprecation_warning
from .version import VERSION


class OxygenCore(object):
    '''OxygenCore collects shared faculties used by the actual classes that do
    something'''

    __version__ = VERSION


    def __init__(self):
        self._config = None
        self._handlers = None

    @property
    def config(self):
        if self._config is None:
            self.load_config(CONFIG_FILE)
        return self._config

    def load_config(self, config_file):
        with open(config_file, 'r') as infile:
            self._config = load(infile, Loader=FullLoader)

    @property
    def handlers(self):
        if self._handlers is None:
            self._handlers = {}
            self._register_handlers()
        return self._handlers

    def _register_handlers(self):
        for tool_name, handler_config in self.config.items():
            try:
                handler_class = getattr(
                    __import__(tool_name, fromlist=[handler_config['handler']]),
                    handler_config['handler'])
            except ModuleNotFoundError as e:
                raise InvalidConfigurationException(e)
            handler = handler_class(handler_config)
            self._handlers[tool_name] = handler


class OxygenVisitor(OxygenCore, ResultVisitor):
    '''OxygenVisitor goes over Robot Framework ExcutionResult object,
    transforming test cases that use keywords of OxygenLibrary to parsed test
    results from other tools.

    Read up on what is Robot Framework SuiteVisitor:
    http://robot-framework.readthedocs.io/en/latest/autodoc/robot.model.html#module-robot.model.visitor
    '''
    def __init__(self, data):
        super().__init__()
        self.data = data

    def visit_test(self, test):
        failures = []
        for handler_type, handler in self.handlers.items():
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
    '''listener passes data from test execution to where results are written.

    listener object is used during test execution to get dynamically data
    from OxygenLibrary keywords. After test execution is finished, listener
    will initiate OxygenVisitor, replacing test cases that used OxygenLibrary
    keywords with parsed test results from other test tools. In the end, the new
    output is written on the disk for rebot to take over and generate Robot
    Framework log and report normally
    '''

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.run_time_data = {}

    def end_test(self, name, attributes):
        try:
            lib = BuiltIn()._get_context().namespace.get_library_instance(
                'oxygen.OxygenLibrary')
            if lib:
                self.run_time_data[attributes['longname']] = lib.data
        except DataError as _:
            pass

    def output_file(self, path):
        result = ExecutionResult(path)
        result.visit(OxygenVisitor(self.run_time_data))
        result.save()

class OxygenLibrary(OxygenCore):
    '''Oxygen is a tool to consolidate different test tools' reports together
    as a single Robot Framework log and report. ``oxygen.OxygenLibrary``
    enables you to write acceptance tests that run your other test tools, parse
    their results and include them into the Robot Framework reporting.

    In addition, you can use the `oxygen command line interface`_ to transform
    an existing test tool report to a single Robot Framework ``output.xml``
    which you can combine together with other Robot Framework ``output.xml``'s
    with Robot Frameworks built-in tool rebot_.

    Acceptance tests that run other test tools might look something like this:

    .. code:: robotframework

        *** Test cases ***
        Java unit tests should pass
            Prepare environment    platform=${PLATFORM}
            Run JUnit    path/to/resuls.xml    mvn clean test

        Java integration tests should pass
            [Tags]    integration-tests
            Prepare environment    platform=${PLATFORM}
            Run JUnit    another/path/results.xml    mvn clean integration-test

        Performance should not degrade
            ${gatling output folder}=    Set variable    path/to/simulations
            Run Gatling    ${gatling output folder}/gatling.log
            ...            %{GATLING_HOME}/bin/gatling.sh --results-folder ${gatling output folder} --simulation MyStressTest

        Application should not have security holes
            Run ZAP    path/to/zap.json    node my_zap_active_scan.js

    As you can see from the examples above, creating acceptance tests that run
    your other test tools is quite flexible. Tests can, in addition to keywords
    described in this documentation, have other Robot Framework keywords (like
    the imaginary user keyword ``Prepare environment`` in the examples above)
    that are normally executed before or after. These are also reported in the
    final Robot Framework reporting.

    You can also observe from the ``Java integration tests should pass`` example
    that tags in the test case will also be part of the final RF reporting —
    these tags will be added to each parsed test result from the other tool.
    This is a good way to add additional metadata like categorization of test
    cases for quality dashboards, if the test tool does not provide this
    themselves.

    Extending oxygen.OxygenLibrary
    ------------------------------

    ``oxygen.OxygenLibrary`` is designed to be extensible with writing your
    own *handler* for Oxygen to use. It is expected that your *handler* also
    provides a keyword for running the test tool you want to provide
    integration for. Since ``oxygen.OxygenLibrary`` is a `dynamic library`_,
    it will also know how to run your *handler's* keyword.

    Keyword documentation should be provided as per `normal way one does with
    Robot Framework libraries`_. The documentation syntax is expected to be
    reStructuredText_.

    After editing Oxygen's ``config.yml`` to `add your own handler`_, you can
    regenerate this library documentation to show your keyword with command:

    .. code:: bash

        $ python -m robot.libdoc OxygenLibrary MyOxygenLibrary.html

    .. _oxygen command line interface: http://github.com/eficode/robotframework-oxygen#using-from-command-line
    .. _rebot: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#post-processing-outputs
    .. _dynamic library: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
    .. _normal way one does with Robot Framework libraries: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#documenting-libraries
    .. _reStructuredText: https://docutils.sourceforge.io/docs/user/rst/quickref.html
    .. _add your own handler: https://github.com/eficode/robotframework-oxygen#extending-oxygen-writing-your-own-handler
    '''

    ROBOT_LIBRARY_DOC_FORMAT = 'reST'

    def __init__(self):
        super().__init__()
        self.data = None

    def _fetch_handler(self, name):
        try:
            return next(filter(lambda h: h.keyword == name,
                               self.handlers.values()))
        except StopIteration:
            raise OxygenException('No handler for keyword "{}"'.format(name))

    def get_keyword_names(self):
        return list(handler.keyword for handler in self.handlers.values())

    def run_keyword(self, name, args, kwargs):
        handler = self._fetch_handler(name)
        retval = getattr(handler, name)(*args, **kwargs)
        self.data = retval
        return retval

    def get_keyword_documentation(self, kw_name):
        if kw_name == '__intro__':
            return getdoc(self.__class__)
        return getdoc(getattr(self._fetch_handler(kw_name), kw_name))

    def get_keyword_arguments(self, kw_name):
        method_sig = signature(getattr(self._fetch_handler(kw_name), kw_name))
        return [str(param) for param in method_sig.parameters.values()]


class OxygenCLI(OxygenCore):
    '''
    OxygenCLI is a command line interface to transform one test result file to
    corresponding Robot Framework output.xml
    '''
    MAIN_LEVEL_CLI_ARGS = {
        # we intentionally define `dest` here so we can filter arguments later
        '--version': {'action': 'version',
                      'dest': 'version'},
        '--add-config': {'type': Path,
                         'metavar': 'FILE',
                         'dest': 'add_config',
                         'help': ('path to YAML file whose content is '
                                  'appended to existing Oxygen handler '
                                  'configuration')},
        '--reset-config': {'action': 'store_true',
                           'dest': 'reset_config',
                           'help': ('resets the Oxygen handler '
                                    'configuration to a pristine, '
                                    'as-freshly-installed version')},
        '--print-config': {'action': 'store_true',
                           'dest': 'print_config',
                           'help': ('prints current Oxygen handler '
                                    'configuration')}
    }
    def add_arguments(self, parser):
        # Add version number here to the arguments as it depends on OxygenCLI
        # being initiated already
        self.MAIN_LEVEL_CLI_ARGS['--version']['version'] = \
            f'%(prog)s {self.__version__}'
        for flag, params in self.MAIN_LEVEL_CLI_ARGS.items():
            parser.add_argument(flag, **params)

        subcommands = parser.add_subparsers()
        for tool_name, tool_handler in self.handlers.items():
            subcommand_parser = subcommands.add_parser(tool_name)
            for flags, params in tool_handler.cli().items():
                subcommand_parser.add_argument(*flags, **params)
                subcommand_parser.set_defaults(func=tool_handler.parse_results)

    def parse_args(self, parser):
        return vars(parser.parse_args())  # returns a dictionary

    def get_output_filename(self, result_file):
        if result_file is None:
            raise ResultFileNotFoundException('You did not give any result '
                                              'file to convert')
        filename = Path(result_file)
        filename = filename.with_suffix('.xml')
        robot_name = filename.stem + '_robot_output' + filename.suffix
        filename = filename.with_name(robot_name)
        return str(filename)

    def append_config(self, new_config_path):
        with open(new_config_path, 'r') as new_config:
            with open(CONFIG_FILE, 'a') as old_config:
                old_config.write(new_config.read())
        self.load_config(CONFIG_FILE)

    @staticmethod
    def reset_config():
        copy_file(ORIGINAL_CONFIG_FILE, CONFIG_FILE)
        OxygenCLI().load_config(CONFIG_FILE)
        print('Oxygen handler configuration reset!')

    def print_config(self):
        print(f'Using config file: {CONFIG_FILE}')
        print(dump_yaml(self.config))

    def convert_to_robot_result(self, args):
        output_filename = self.get_output_filename(args.get('result_file'))
        parsed_results = args['func'](
            **{k: v for (k, v) in args.items() if not callable(v)})
        validate_with_deprecation_warning(parsed_results, args['func'])
        robot_suite = RobotInterface().running.build_suite(parsed_results)
        robot_suite.run(output=output_filename,
                        log=None,
                        report=None,
                        stdout=StringIO())

    def run(self):
        parser = ArgumentParser(prog='oxygen')
        self.add_arguments(parser)
        args = self.parse_args(parser)
        match args:
            case {'add_config': new_config_path} if new_config_path is not None:
                return self.append_config(new_config_path)
            case {'print_config': should_print} if should_print:
                return self.print_config()
            case {'add_config': _,
                  'reset_config': _,
                  'print_config': _,
                  **rest} if not rest:  # user is not trying to invoke main-level arguments, but do not provide other arguments either
                parser.error('No arguments given')
            case _:
                # filter out arguments meant for other cases so that downstream
                # handler does not need to know about them
                filter_list = [v['dest'] for v in
                                self.MAIN_LEVEL_CLI_ARGS.values()]
                filtered_args = {k: v for k, v in args.items()
                                    if k not in filter_list}
                return self.convert_to_robot_result(filtered_args)

def main():
    '''Main CLI entrypoint

    Also used in __main__.py
    '''
    if '--reset-config' in sys.argv:
        OxygenCLI.reset_config()
        sys.exit(0)
    OxygenCLI().run()

if __name__ == '__main__':
    main()
