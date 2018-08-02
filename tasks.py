from invoke import run, task


@task
def install(context):
    run('pip install -r requirements.txt')

