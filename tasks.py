from pathlib import Path
from platform import system

from invoke import run, task


CURDIR = Path.cwd()
SRCPATH = CURDIR / 'src'
UNIT_TESTS = CURDIR / 'tests'
IN_NIX_HELP = ('Setup environment for use inside Nix. By default PYTHONPATH '
               'is being overriden with source path. This flag makes sure '
               'that PYTHONPATH is untouched.')

# If you want colored output for the tasks, use `run()` with `pty=True`
# Not on Windows, though -- it'll fail if you have `pty=True`

@task
def clean(context):
    for path in (f'{SRCPATH / "robotframework_oxygen.egg-info"}',
                 f'{CURDIR / "build"}',
                 f'{CURDIR / "dist"}',
                 f'{CURDIR / ".tox"}',
                 f'{CURDIR / "htmlcov"}',
                 f'{CURDIR / "log.html"}',
                 f'{CURDIR / "report.html"}',
                 f'{CURDIR / "output.xml"}',
                 f'{CURDIR / "green-junit.xml"}'):
      run(f'rm -rf {path}')
    run(f'python {CURDIR / "setup.py"} clean')

@task(pre=[clean])
def install(context, package=None):
    run(f'pip install -r {CURDIR / "requirements.txt"}')
    if package:
        run(f'pip install {package}')

@task(iterable=['test'],
      help={
          'test': 'Limit unit test execution to specific tests. Must be given '
                  'multiple times to select several targets. See more: '
                  'https://github.com/CleanCut/green/blob/master/cli-options.txt#L5',
          'in_nix': IN_NIX_HELP
      })
def utest(context, test=None, in_nix=False):
    env = {} if in_nix else {'PYTHONPATH': str(SRCPATH)}
    run(f'green {" ".join(test) if test else UNIT_TESTS}',
        env=env,
        pty=(not system() == 'Windows'))

@task(help={
    'in_nix': IN_NIX_HELP
})
def coverage(context, in_nix=False):
    env = {} if in_nix else {'PYTHONPATH': str(SRCPATH)}
    run(f'green -r {str(UNIT_TESTS)}',
        env=env,
        pty=(not system() == 'Windows'))

@task(help={
    'rf': 'Additional command-line arguments for Robot Framework as '
          'single string. E.g: invoke atest --rf "--name my_suite"'
})
def atest(context, rf=''):
    run(f'robot '
        f'--pythonpath {str(SRCPATH)}'
        f'--dotted '
        f'{rf} '
        f'--listener oxygen.listener '
        f'{str(CURDIR / "tests" / "atest")}',
        pty=(not system() == 'Windows'))

@task(help={
    'in_nix': IN_NIX_HELP
})
def test(context, in_nix=False):
    utest(context, in_nix=in_nix)
    atest(context)

@task
def doc(context):
    doc_path = CURDIR / 'docs'
    if not doc_path.exists():
        run(f'mkdir {doc_path}')
    version = run('python -c "import oxygen; print(oxygen.__version__)"',
                  env={'PYTHONPATH': str(SRCPATH)})
    version = version.stdout.strip()
    target = doc_path / f'OxygenLibrary-{version}.html'
    run(f'python -m robot.libdoc oxygen.OxygenLibrary {target}',
        env={'PYTHONPATH': str(SRCPATH)})
    run(f'cp {target} {doc_path / "index.html"}')

@task(pre=[clean])
def build(context):
    run(f'python {CURDIR / "setup.py"} bdist_wheel')
