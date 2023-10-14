import sys

from .oxygen import OxygenCLI

if __name__ == '__main__':
    if '--reset-config' in sys.argv:
        OxygenCLI.reset_config()
        sys.exit(0)
    OxygenCLI().run()
