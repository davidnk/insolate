# Copyright (c) 2013 David Karesh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
parser.add_argument("-p", "--filepattern", type=str, default='*.py *.txt *.xml',
                    help="set repository to store CHANGES and ORIG")
parser.add_argument('cmd', nargs='+', help='command')
args = parser.parse_args()
_INSOLATER = Insolater(repo=args.repo, timeout=args.timeout, filepattern=args.filepattern)

command = lambda: _INSOLATER.main(args.cmd)
init = _INSOLATER.start_session
push = _INSOLATER.push_remote
pull = _INSOLATER.pull_remote
exit = _INSOLATER.exit_session
cd = _INSOLATER.change_branch
pwd = lambda: _INSOLATER.main(['pwd'])
