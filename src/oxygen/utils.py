import subprocess

from .errors import SubprocessException

def run_command_line(*command):
    try:
        proc = subprocess.run(command, capture_output=True)
    except IndexError as e:
        raise SubprocessException('Command "{}" was empty'.format(command))
    if proc.returncode != 0:
        raise SubprocessException('Command "{}" failed'.format(command))
    return proc.stdout
