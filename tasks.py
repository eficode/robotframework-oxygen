from os.path import abspath, dirname, join as path_join

from invoke import run, task


CURDIR = abspath(dirname(__file__))
print(CURDIR)
SRCPATH = path_join(CURDIR, 'src')
print(SRCPATH)

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

@task
def utest(context, k=''):
    cmd = ('python -m unittest discover --start-directory tests/utest '
           '--top-level-directory {} {}'.format(CURDIR,
                                                ('-k ' + k) if k else ''))
    run(cmd, env={'PYTHONPATH': SRCPATH})

@task(help={'rf': 'Command-line arguments for Robot Framework as single '
                  'string. E.g: invoke atest --rf "--name my_suite"'})
def atest(context, rf=''):
    run('robot --pythonpath {} --dotted {} --listener oxygen.Oxygen tests/atest'.format(SRCPATH, rf),
        pty=True)  # pty for colored output

@task(pre=[utest, atest])
def test(context):
    pass
