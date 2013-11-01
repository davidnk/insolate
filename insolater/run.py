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

import argparse
from insolater import Insolater


def cli(inso, argv):
    help_str = ("{cmd} init [<remote_changes>]\t\tstarts a new session.\n" +
                "{cmd} pwd\t\t\t\tdisplays current version.\n" +
                "{cmd} cd <ORIG or CHANGES>\t\tswitches to the requested version\n" +
                "{cmd} pull <remote_changes>\t\tpulls remote changes branch\n" +
                "{cmd} push <remote_location>\t\tpulls remote changes branch\n" +
                "{cmd} exit [<remote_changes>]\t\tends the session."
                ).format(cmd=Insolater._CMD)
    if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
        print(help_str)
        return
    if argv[0] == 'init':
        if len(argv) <= 2:
            print(inso.init(*argv[1:])[1])
        else:
            print("Usage: {cmd} init [remote_changes]".format(cmd=Insolater._CMD))
    elif argv[0] == 'pull':
        if len(argv) == 2:
            print(inso.pull(argv[1]))
        else:
            print("Usage: {cmd} pull <remote_changes>".format(cmd=Insolater._CMD))
    elif argv[0] == 'push':
        if len(argv) == 2:
            print(inso.push(argv[1])[1])
        else:
            print("Usage: {cmd} push <remote_changes>".format(cmd=Insolater._CMD))
    elif argv[0] == 'pwd':
            head = inso.get_current_branch()[1]
            if head == 'CHANGES':
                print("Currently in CHANGES version.")
            else:
                print('Currently in ORIG version.')
    elif argv[0] == 'cd':
        if len(argv) < 2:
            print("Usage: {cmd} cd <ORIG or CHANGES>".format(cmd=Insolater._CMD))
        else:
            print(inso.change_branch(argv[1])[1])
    elif argv[0] == 'exit':
        if len(argv) <= 2:
            print(inso.exit(*argv[1:])[1])
        else:
            print("Usage: {cmd} exit [<remote_changes>]".format(cmd=Insolater._CMD))
    else:
        print("Not a {cmd} command. See '{cmd} --help'.".format(cmd=Insolater._CMD))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timeout", type=int, default=5,
                        help="set timeout for file transfers")
    parser.add_argument("-r", "--repo", type=str, default='.insolater_repo',
                        help="set repository to store CHANGES and ORIG")
    parser.add_argument("-p", "--filepattern", type=str, default='. *.py *.txt *.xml',
                        help="set repository to store CHANGES and ORIG")
    parser.add_argument('cmd', nargs='+', help='command')
    args = parser.parse_args()
    i = Insolater(repo=args.repo, timeout=args.timeout, filepattern=args.filepattern)
    cli(i, args.cmd)


if __name__ == '__main__':
    main()
