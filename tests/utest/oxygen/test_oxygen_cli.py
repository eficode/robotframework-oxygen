from argparse import ArgumentParser, Namespace
from pathlib import Path
from subprocess import check_output, run, STDOUT, CalledProcessError
from tempfile import mkstemp
from unittest import TestCase
from unittest.mock import ANY, create_autospec, patch, Mock
from xml.etree import ElementTree

from robot.running.model import TestSuite

from oxygen.oxygen import OxygenCLI, OxygenCore
from oxygen.config import CONFIG_FILE, ORIGINAL_CONFIG_FILE

from ..helpers import RESOURCES_PATH


class TestOxygenCLIEntryPoints(TestCase):
    '''Coverage does not measure coverage correctly for these tests.

    We have tests for __main__ entrypoint below, but Coverage is unable to
    do its measurements as they are running in subprocesses. They are run in
    subprocesses to simulate real command line usage.

    Setting up Coverage to see subprocesses as well seems a lot of work and
    quite a hack: https://coverage.readthedocs.io/en/latest/subprocess.html
    '''

    @classmethod
    def tearDownClass(cls):
        with open(ORIGINAL_CONFIG_FILE, 'r') as og:
            with open(CONFIG_FILE, 'w') as config:
                config.write(og.read())

    def tearDown(self):
        self.tearDownClass()

    def test_main_level_entrypoint(self):
        self.verify_cli_help_text('python -m oxygen --help')
        self.verify_cli_help_text('python -m oxygen -h')

    def test_direct_module_entrypoint(self):
        self.verify_cli_help_text('python -m oxygen.oxygen --help')
        self.verify_cli_help_text('python -m oxygen.oxygen -h')

    def test_cli_with_no_args(self):
        proc = run('python -m oxygen',
                   shell=True,
                   text=True,
                   capture_output=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn('usage: oxygen', proc.stderr)

    def _run(self, cmd):
        try:
            return check_output(cmd, text=True, shell=True, stderr=STDOUT)
        except CalledProcessError as e:
            print(e.output)  # with this, you can actually see the command
            raise            # output, ie. why it failed

    def verify_cli_help_text(self, cmd):
        out = self._run(cmd)
        self.assertIn('usage: oxygen', out)
        self.assertIn('-h, --help', out)

    def test_junit_works_on_cli(self):
        target = RESOURCES_PATH / 'green-junit-example.xml'
        example = target.with_name('green-junit-expected-robot-output.xml')
        actual = target.with_name('green-junit-example_robot_output.xml')
        if actual.exists():
            actual.unlink()  # delete file if exists

        self._run(f'python -m oxygen oxygen.junit {target}')

        example_xml = ElementTree.parse(example).getroot()
        actual_xml = ElementTree.parse(actual).getroot()

        # RF<4 has multiple `stat` elements therefore we use the double slash
        # and a filter to single out the `stat` element with text "All Tests"
        all_tests_stat_block = './statistics/total//stat[.="All Tests"]'

        example_stat = example_xml.find(all_tests_stat_block)
        actual_stat = actual_xml.find(all_tests_stat_block)

        self.assertEqual(example_stat.get('pass'), actual_stat.get('pass'))
        self.assertEqual(example_stat.get('fail'), actual_stat.get('fail'))

    def _validate_handler_names(self, text):
        for handler in ('JUnitHandler', 'GatlingHandler', 'ZAProxyHandler'):
            self.assertIn(handler, text)

    def test_reset_config(self):
        with open(CONFIG_FILE, 'w') as f:
            f.write('complete: gibberish')

        self._run(f'python -m oxygen --reset-config')

        with open(CONFIG_FILE, 'r') as f:
            config_content = f.read()
        self.assertNotIn('complete: gibberish', config_content)
        self._validate_handler_names(config_content)

    def test_print_config(self):
        out = self._run('python -m oxygen --print-config')

        self.assertIn('Using config file', out)
        self._validate_handler_names(out)

    def _make_test_config(self):
        _, filepath = mkstemp()
        with open(filepath, 'w') as f:
            f.write('complete: gibberish')
        return filepath

    def test_add_config(self):
        filepath = self._make_test_config()

        self._run(f'python -m oxygen --add-config {filepath}')

        with open(CONFIG_FILE, 'r') as f:
            config_content = f.read()
        self._validate_handler_names(config_content)
        self.assertIn('complete: gibberish', config_content)

    def _is_file_content(self, filepath, text):
        with open(filepath, 'r') as f:
            return bool(text in f.read())

    def test_main_level_args_override_handler_args(self):
        filepath = self._make_test_config()

        cmd = ('python -m oxygen {main_level_arg} '
               f'oxygen.junit {RESOURCES_PATH / "green-junit-example.xml"}')

        self._run(cmd.format(main_level_arg=f'--add-config {filepath}'))
        self.assertTrue(self._is_file_content(CONFIG_FILE, 'complete: gibberish'))

        self._run(cmd.format(main_level_arg='--reset-config'))
        self.assertFalse(self._is_file_content(CONFIG_FILE,
                                               'complete: gibberish'))


        out = self._run(cmd.format(main_level_arg='--print-config'))
        self._validate_handler_names(out)
        self.assertNotIn('gibberish', out)


class TestOxygenCLI(TestCase):

    def setUp(self):
        self.cli = OxygenCLI()

    @patch('oxygen.oxygen.RobotInterface')
    @patch('oxygen.oxygen.OxygenCLI.parse_args')
    def test_run(self, mock_parse_args, mock_robot_iface):
        mock_parse_args.return_value = {
            'result_file': 'path/to/file.xml',
            'func': lambda *_, **__: {'some': 'results'}}
        expected_suite = create_autospec(TestSuite)
        mock = Mock()
        mock.running.build_suite = Mock(return_value=expected_suite)
        mock_robot_iface.return_value = mock

        self.cli.run()

        mock.running.build_suite.assert_called_once_with({'some': 'results'})
        expected_suite.run.assert_called_once_with(
            output=str(Path('path/to/file_robot_output.xml')),
            log=None,
            report=None,
            stdout=ANY
        )

    def test_parse_args(self):
        '''verifies that `parse_args()` returns a dictionary'''
        p = create_autospec(ArgumentParser)
        p.parse_args.return_value = create_autospec(Namespace)

        retval = self.cli.parse_args(p)

        self.assertIsInstance(retval, dict)

    def test_add_arguments(self):
        mock_parser = create_autospec(ArgumentParser)
        m = Mock()
        mock_parser.add_subparsers.return_value = m

        self.cli.add_arguments(mock_parser)

        # verify all main-level cli arguments were added
        self.assertEqual(len(mock_parser.add_argument.call_args_list), 4)
        # verify all built-in handlers were added
        self.assertEqual(len(m.add_parser.call_args_list), 3)

    def _actual(self, path):
        return self.cli.get_output_filename(path)

    def _expected(self, path):
        return str(Path(path))

    def test_get_output_filename(self):
        for act, exp in ((self._actual('/absolute/path/to.file'),
                          self._expected('/absolute/path/to_robot_output.xml')),

                         (self._actual('path/to/file.xml'),
                          self._expected('path/to/file_robot_output.xml')),

                         (self._actual('file.extension'),
                          self._expected('file_robot_output.xml'))):
            self.assertEqual(act, exp)



