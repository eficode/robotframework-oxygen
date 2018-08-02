from os.path import abspath, dirname, join as path_join

from invoke import run, task


CURDIR = abspath(dirname(__file__))
SRCPATH = path_join(CURDIR, 'src')

@task
def install(context):
    run('pip install -r requirements.txt')

@task
def utest(context):
    cmd = ('python -m unittest discover --start-directory tests/ '
           '--top-level-directory {}'.format(CURDIR))
    run(cmd, env={'PYTHONPATH': SRCPATH})

@task
def atest(context, rf=''):
    run('robot --pythonpath {} --dotted {} test/'.format(SRCPATH, rf),
        pty=True)  # pty for colored output

@task(pre=[utest, atest])
def test(context):
    pass
