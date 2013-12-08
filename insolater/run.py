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

import sys
import argparse
from insolater import Insolater


help_str = ("{cmd} init [<remote_changes>]              Starts a new session.\n" +
            "{cmd} list                                 Displays versions.\n" +
            "{cmd} save  <version>                      Save to version.\n" +
            "{cmd} rm   <version>                       Remove version.\n" +
            "{cmd} open <version>                       Switches to the requested version\n" +
            "{cmd} pull <remote_location> [<version>]   Pull remote version [to version]\n" +
            "{cmd} push <remote_location> [<version>]   Push [version] to remote location\n" +
            "{cmd} exit                                 Permanently delete all versions\n" +
            (' ' * len(Insolater._CMD)) +
            "                                               and restore original."
            ).format(cmd=Insolater._CMD)


def cli(inso, argv):
    try:
        if argv[0] == 'init':
            if len(argv) <= 2:
                print(inso.init(*argv[1:]))
            else:
                print("Usage: {cmd} init [remote_changes]".format(cmd=Insolater._CMD))
        elif argv[0] == 'list':
                cv = inso.current_version()
                av = inso.all_versions()
                for v in av:
                    if cv == v:
                        print('* ' + v)
                    else:
                        print('  ' + v)
        elif argv[0] == 'save':
            if len(argv) < 2:
                print("Usage: {cmd} save <version>".format(cmd=Insolater._CMD))
            else:
                print(inso.save_version(argv[1]))
        elif argv[0] == 'rm':
            if len(argv) < 2:
                print("Usage: {cmd} rm <version>".format(cmd=Insolater._CMD))
            else:
                print(inso.delete_version(argv[1]))
        elif argv[0] == 'open':
            if len(argv) < 2:
                print("Usage: {cmd} open <version>".format(cmd=Insolater._CMD))
            else:
                print(inso.change_version(argv[1]))
        elif argv[0] == 'pull':
            if len(argv) < 2:
                print("Usage: {cmd} pull <remote_location [<version>]".format(cmd=Insolater._CMD))
            else:
                print(inso.pull_version(*argv[1:]))
        elif argv[0] == 'push':
            if len(argv) < 2:
                print("Usage: {cmd} push <remote_location [<version>]".format(cmd=Insolater._CMD))
            else:
                print(inso.push_version(*argv[1:]))
        elif argv[0] == 'exit':
            print(inso.exit())
        else:
            print("Not a {cmd} command.".format(cmd=Insolater._CMD))
            print(help_str)
    except Exception as error_msg:
        print error_msg.message


def main():
    argv = sys.argv[1:]
    if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
        print(help_str)
        return
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timeout", type=int, default=5,
                        help="set timeout for file transfers")
    parser.add_argument("-r", "--repo", type=str, default='.insolater_repo',
                        help="set repository to store versions")
    parser.add_argument("-p", "--filepattern", type=str, default='. *.py *.txt *.xml',
                        help="set filepatterns to track")
    parser.add_argument('cmd', nargs='+', help='command')
    args = parser.parse_args()
    i = Insolater(repo=args.repo, timeout=args.timeout, filepattern=args.filepattern)
    cli(i, args.cmd)


if __name__ == '__main__':
    main()
