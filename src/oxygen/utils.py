import os
import subprocess
import sys

from pathlib import Path

from .errors import (InvalidOxygenResultException,
                     ResultFileIsNotAFileException,
                     ResultFileNotFoundException,
                     SubprocessException)
from .oxygen_handler_result import validate_oxygen_suite

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
    try:
        path = Path(filepath)
    except TypeError as e:
        raise ResultFileIsNotAFileException(f'File "{filepath}" is not a file')
    if not path.exists():
        raise ResultFileNotFoundException(f'File "{path}" does not exits')
    if path.is_dir():
        raise ResultFileIsNotAFileException(f'File "{path}" is not a file, '
                                            'but a directory')
    return path

def validate_with_deprecation_warning(oxygen_result_dict, handler):
    try:
        validate_oxygen_suite(oxygen_result_dict)
    except InvalidOxygenResultException as e:
        import warnings
        # this is not done with triple quotes intentionally
        # to get sensible formatting to output
        msg = (f'\n{handler.__module__} is producing invalid results:\n'
               f'{e}\n\n'
               'In Oxygen 1.0, handlers will need to produce valid '
               'results.\nSee: '
               'https://github.com/eficode/robotframework-oxygen/blob/master/parser_specification.md')
        warnings.warn(msg)
