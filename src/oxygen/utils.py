import subprocess
from pathlib import Path

from .errors import (SubprocessException,
                     ResultFileIsNotAFileException,
                     ResultFileNotFoundException)

def run_command_line(*command):
    try:
        proc = subprocess.run(command, capture_output=True)
    except IndexError as e:
        raise SubprocessException('Command "{}" was empty'.format(command))
    if proc.returncode != 0:
        raise SubprocessException('Command "{}" failed'.format(command))
    return proc.stdout

def validate_path(filepath):
    path = Path(filepath)
    if not path.exists():
        raise ResultFileNotFoundException(f'File "{path}" does not exits')
    if path.is_dir():
         raise ResultFileIsNotAFileException(f'File "{path}" is not a file, '
                                              'but a directory')
    return path
