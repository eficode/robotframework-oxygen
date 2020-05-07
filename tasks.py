from pathlib import Path

from invoke import run, task


CURDIR = Path.cwd()
SRCPATH = CURDIR / 'src'
UNIT_TESTS = CURDIR / 'tests' / 'utest'

# If you want colored output for the tasks, use `run()` with `pty=True`

@task
def clean(context):
    run('rm -rf {}'.format(path_join(SRCPATH,
                                     'robotframework_oxygen.egg-info')))
    run('python {} clean'.format(path_join(CURDIR, 'setup.py')))

@task(pre=[clean])
def install(context, package=None):
    run('pip install -r {}'.format(path_join(CURDIR, 'requirements.txt')))
    if package:
        run('pip install {}'.format(package))

@task(iterable=['test'],
      help={
          'test': 'Limit unit test execution to specific tests. Must be given '
                  'multiple times to select several targets. See more: '
                  'https://github.com/CleanCut/green/blob/master/cli-options.txt#L5'
      })
def utest(context, test):
    run(f'green {" ".join(test) if test else UNIT_TESTS}',
        env={'PYTHONPATH': SRCPATH},
        pty=True)
    run('coverage html')

@task
def coverage(context):
  run(f'green -r {UNIT_TESTS}', env={'PYTHONPATH': SRCPATH}, pty=True)

@task(help={'rf': 'Additional command-line arguments for Robot Framework as '
                  'single string. E.g: invoke atest --rf "--name my_suite"'})
def atest(context, rf=''):
    run(f'robot '
        f'--pythonpath {SRCPATH} '
        f'--dotted '
        f'{rf} '
        f'--listener oxygen.listener '
        f'{CURDIR / "tests" / "atest"}',
        pty=True)

@task(pre=[utest, atest])
def test(context):
    pass
