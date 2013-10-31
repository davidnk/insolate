__all__ = [
    'command',
    'init',
    'push',
    'pull',
    'exit',
    'cd',
    'pwd']

# Export the global Commandr object methods.
import sys
from insolater import Insolater
_INSOLATER = Insolater()

command = lambda: _INSOLATER.main(sys.argv[1:])
init = _INSOLATER.start_session
push = _INSOLATER.push_remote
pull = _INSOLATER.pull_remote
exit = _INSOLATER.exit_session
cd = _INSOLATER.change_branch
pwd = lambda: _INSOLATER.main(['pwd'])
