from subprocess import check_output, run
from unittest import TestCase, skip


class TestOxygenCLI(TestCase):
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
        self.assertTrue('usage: oxygen' in proc.stderr)

    def verify_cli_help_text(self, cmd):
        out = check_output(cmd, text=True, shell=True)
        self.assertTrue('usage: oxygen' in out)
        self.assertTrue('-h, --help' in out)
