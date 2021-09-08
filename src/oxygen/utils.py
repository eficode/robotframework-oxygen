import os
import subprocess
import sys

from pathlib import Path

from .errors import (SubprocessException,
                     ResultFileIsNotAFileException,
                     ResultFileNotFoundException)


def run_command_line(command, check_return_code=True, **env):
    new_env = os.environ.copy()
    # When user uses 'robot --pythonpath' we need to update PYTHONPATH in the
    # subprocess
    updated_pythonpath = {'PYTHONPATH': os.pathsep.join([new_env.get(
        'PYTHONPATH', '')] + sys.path)}
    new_env.update(updated_pythonpath)
    new_env.update(env)

    try:
        proc = subprocess.run(command, capture_output=True, env=new_env, shell=True)
    except IndexError:
        raise SubprocessException('Command "{}" was empty'.format(command))
    if check_return_code and proc.returncode != 0:
        raise SubprocessException(f'Command "{command}" failed with return '
                                  f'code {proc.returncode}:\n"{proc.stdout.decode("utf-8")}"')
    return proc.stdout


def validate_path(filepath):
    path = Path(filepath)
    if not path.exists():
        raise ResultFileNotFoundException(f'File "{path}" does not exits')
    if path.is_dir():
        raise ResultFileIsNotAFileException(f'File "{path}" is not a file, '
                                            'but a directory')
    return path
