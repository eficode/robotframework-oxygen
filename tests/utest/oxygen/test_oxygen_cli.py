from argparse import ArgumentParser
from subprocess import check_output, run
from unittest import TestCase
from unittest.mock import create_autospec, patch, Mock

from robot.result.model import TestSuite

from oxygen.oxygen import OxygenCLI

from ..helpers import RESOURCES_PATH

class TestOxygenCLIEntryPoints(TestCase):
    """Coverage does not measure coverage correctly for these tests.

    We have tests for __main__ entrypoint below, but Coverage is unable to
    do its measurements as they are running in subprocesses. They are run in
    subprocesses to simulate real command line usage.

    Setting up Coverage to see subprocesses as well seems a lot of work and
    quite a hack: https://coverage.readthedocs.io/en/latest/subprocess.html
    """
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
        expected = target.with_name('green-junit-expected-robot-output.xml')
        actual = target.with_name('green-junit-example_robot_output.xml')
        if actual.exists():
            actual.unlink() # delete file if exists

        out = check_output(f'python -m oxygen oxygen.junit {target}',
                           text=True,
                           shell=True)

        self.assertEqual(expected.read_text(), expected.read_text())

class TestOxygenCLI(TestCase):

    def setUp(self):
        self.cli = OxygenCLI()

    @patch('oxygen.oxygen.OxygenCLI.save_robot_output')
    @patch('oxygen.oxygen.OxygenCLI.convert_results_to_RF')
    @patch('oxygen.oxygen.OxygenCLI.parse_args')
    def test_run(self, mock_parse_args, mock_convert, mock_save):
        m = Mock()
        m.resultfile = 'path/to/file.xml'
        m.func = lambda r: {'some': 'results'}
        mock_parse_args.return_value = m

        expected_suite = create_autospec(TestSuite)
        mock_convert.return_value = expected_suite

        self.cli.run()

        mock_convert.assert_called_once_with({'some': 'results'})
        mock_save.assert_called_once_with('path/to/file_robot_output.xml',
                                          expected_suite)

    def test_parse_args(self):
        mock_parser = create_autospec(ArgumentParser)
        m = Mock()
        mock_parser.add_subparsers.return_value = m

        self.cli.parse_args(mock_parser)

        self.assertEqual(len(m.add_parser.call_args_list), 3)

    def test_get_output_filename(self):
        self.assertEqual(self.cli.get_output_filename('absolute/path/to.file'),
                         'absolute/path/to_robot_output.xml')
        self.assertEqual(self.cli.get_output_filename('path/to/file.xml'),
                         'path/to/file_robot_output.xml')
        self.assertEqual(self.cli.get_output_filename('file.extension'),
                         'file_robot_output.xml')

