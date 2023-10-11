from argparse import ArgumentParser
from pathlib import Path
from subprocess import check_output, run
from unittest import TestCase
from unittest.mock import ANY, create_autospec, patch, Mock
from xml.etree import ElementTree

from robot.running.model import TestSuite

from oxygen.oxygen import OxygenCLI

from ..helpers import RESOURCES_PATH


class TestOxygenCLIEntryPoints(TestCase):
    '''Coverage does not measure coverage correctly for these tests.

    We have tests for __main__ entrypoint below, but Coverage is unable to
    do its measurements as they are running in subprocesses. They are run in
    subprocesses to simulate real command line usage.

    Setting up Coverage to see subprocesses as well seems a lot of work and
    quite a hack: https://coverage.readthedocs.io/en/latest/subprocess.html
    '''

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

    def verify_cli_help_text(self, cmd):
        out = check_output(cmd, text=True, shell=True)
        self.assertIn('usage: oxygen', out)
        self.assertIn('-h, --help', out)

    def test_junit_works_on_cli(self):
        target = RESOURCES_PATH / 'green-junit-example.xml'
        example = target.with_name('green-junit-expected-robot-output.xml')
        actual = target.with_name('green-junit-example_robot_output.xml')
        if actual.exists():
            actual.unlink()  # delete file if exists

        check_output(f'python -m oxygen oxygen.junit {target}',
                     text=True,
                     shell=True)

        example_xml = ElementTree.parse(example).getroot()
        actual_xml = ElementTree.parse(actual).getroot()

        # RF<4 has multiple `stat` elements therefore we use the double slash
        # and a filter to single out the `stat` element with text "All Tests"
        all_tests_stat_block = './statistics/total//stat[.="All Tests"]'

        example_stat = example_xml.find(all_tests_stat_block)
        actual_stat = actual_xml.find(all_tests_stat_block)

        self.assertEqual(example_stat.get('pass'), actual_stat.get('pass'))
        self.assertEqual(example_stat.get('fail'), actual_stat.get('fail'))


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
        p = ArgumentParser()

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

    def test_get_output_filename(self):
        self.assertEqual(self.cli.get_output_filename('absolute/path/to.file'),
                         str(Path('absolute/path/to_robot_output.xml')))
        self.assertEqual(self.cli.get_output_filename('path/to/file.xml'),
                         str(Path('path/to/file_robot_output.xml')))
        self.assertEqual(self.cli.get_output_filename('file.extension'),
                         str(Path('file_robot_output.xml')))

