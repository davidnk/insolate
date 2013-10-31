__all__ = [
    'command',
    'init',
    'push',
    'pull',
    'exit',
    'cd',
    'pwd']

# Export the global Commandr object methods.
import argparse
from insolater import Insolater

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--timeout", type=int, default=5,
                    help="set timeout for file transfers")
parser.add_argument("-r", "--repo", type=str, default='.insolater_repo',
                    help="set repository to store CHANGES and ORIG")
parser.add_argument('cmd', nargs='+', help='command')
args = parser.parse_args()
_INSOLATER = Insolater(repo=args.repo, timeout=args.timeout)

command = lambda: _INSOLATER.main(args.cmd)
init = _INSOLATER.start_session
push = _INSOLATER.push_remote
pull = _INSOLATER.pull_remote
exit = _INSOLATER.exit_session
cd = _INSOLATER.change_branch
pwd = lambda: _INSOLATER.main(['pwd'])
