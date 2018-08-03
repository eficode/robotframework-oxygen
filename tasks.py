from os.path import abspath, dirname, join as path_join

from invoke import run, task


CURDIR = abspath(dirname(__file__))
SRCPATH = path_join(CURDIR, 'src')

@task
def install(context, package=None):
    run('pip install -r requirements.txt')
    if package:
        run('pip install {}'.format(package))

@task
def utest(context):
    cmd = ('python -m unittest discover --start-directory tests/utest '
           '--top-level-directory {}'.format(CURDIR))
    run(cmd, env={'PYTHONPATH': SRCPATH})

@task(help={'rf': 'Command-line arguments for Robot Framework as single '
                  'string. E.g: invoke atest --rf "--name my_suite"'})
def atest(context, rf=''):
    run('robot --pythonpath {} --dotted {} --prerebotmodifier oxygen.Oxygen tests/atest'.format(SRCPATH, rf),
        pty=True)  # pty for colored output

@task(pre=[utest, atest])
def test(context):
    pass
