from os.path import abspath, dirname, join as path_join

from invoke import run, task


CURDIR = abspath(dirname(__file__))
SRCPATH = path_join(CURDIR, 'src')

@task
def install():
    run('pip install -r requirements.txt')

@task
def utest():
    cmd = ('python -m unittest discover --start-directory tests/ '
           '--top-level-directory {}'.format(CURDIR))
    run(cmd, env={'PYTHONPATH': SRCPATH})

@task
def atest():
        pty=True)  # pty for colored output
