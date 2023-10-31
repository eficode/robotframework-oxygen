import os

from pathlib import Path
from platform import system
from tempfile import mkstemp
from textwrap import dedent

from invoke import run, task


CURDIR = Path.cwd()
SRCPATH = CURDIR / 'src'
UNIT_TESTS = CURDIR / 'tests'
DUMMYHANDLERS = UNIT_TESTS / 'resources' / 'my_dummy_handlers'

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
                  'multiple times to select several targets.'
      })
def utest(context, test=None):
    run(f'pytest {" -k".join(test) if test else UNIT_TESTS} -q --disable-warnings',
        env={'PYTHONPATH': str(SRCPATH)},
        pty=(not system() == 'Windows'))

@task
def coverage(context):
    run(f'pytest --cov {UNIT_TESTS}',
        env={'PYTHONPATH': str(SRCPATH)},
        pty=(not system() == 'Windows'))
    run('coverage html')

def _setup_atest():
    _, tempconf =  mkstemp()
    with open(tempconf, 'w') as f:
        f.write('''dummy_handler_metadata:
            handler: MyDummyMetadataHandler
            keyword: run_metadata_dummy_handler
            tags: oxygen-metadata''')
    return (tempconf,
            os.pathsep.join([str(SRCPATH),
                             str(DUMMYHANDLERS)]))

@task(help={
    'rf': 'Additional command-line arguments for Robot Framework as '
          'single string. E.g: invoke atest --rf "--name my_suite"'
})
def atest(context, rf=''):
    tempconf, pythonpath = _setup_atest()
    run(f'python -m oxygen --add-config {tempconf}',
        env={'PYTHONPATH': pythonpath})
    try:
        run(f'robot '
            f'--pythonpath {str(SRCPATH)} '
            f'--pythonpath {str(DUMMYHANDLERS)} '
            f'--dotted '
            f'{rf} '
            f'--listener oxygen.listener '
            f'{str(CURDIR / "tests" / "atest")}',
            pty=(not system() == 'Windows'))
    finally:
        run('python -m oxygen --reset-config', env={'PYTHONPATH': pythonpath})

@task
def test(context):
    utest(context)
    atest(context)

@task
def update_oxygen_schema(context):
    import sys
    import json
    from pydantic import TypeAdapter

    sys.path.insert(0, str(SRCPATH))
    from oxygen.oxygen_handler_result import OxygenSuiteDict

    schema = TypeAdapter(OxygenSuiteDict).json_schema()
    out = json.dumps(schema, indent=2)
    with open(CURDIR / 'handler_result_specification.md', 'r+') as f:
        header = f.readline()
        f.seek(0)
        f.write(header)
        f.write(f'```\n{out}\n```')
        f.truncate()
    print('Updated schema')

@task(pre=[update_oxygen_schema])
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
    run(f'python -m build --wheel')

