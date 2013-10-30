#! /usr/bin/python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import getpass
import pexpect
from subprocess import Popen, call, PIPE


def call_init(remote_changes=None):
    if os.path.exists(".multirepo"):
        exit("Already initialized. " +
             " To finish and backup run: mulit done <remote backup>")
    sh = """
        git --git-dir=.multirepo --work-tree=. init
        echo '.multirepo' >> .gitignore
        echo 'multi.py' >> .gitignore
        echo '.gitignore' >> .gitignore
        git --git-dir=.multirepo add .
        git --git-dir=.multirepo reset -- .multirepo
        git --git-dir=.multirepo commit -a -m "Original files"
        git --git-dir=.multirepo tag -a ORIG -m "original files"
        git --git-dir=.multirepo branch CHANGES
        git --git-dir=.multirepo checkout CHANGES
        """
    call(sh, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    if remote_changes:
        call_pull(remote_changes)
    return "Initialized branches ORIG, CHANGES"


def call_pull(remote_changes):
    call_to('CHANGES')
    sh = """
        rsync -Pravdtze ssh %s .
        git --git-dir=.multirepo add .
        git --git-dir=.multirepo reset -- .multirepo
        git --git-dir=.multirepo commit -a -m "Pulled changes"
        """ % remote_changes
    call(sh, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return "Pulled updates"


def call_to(branch):
    if not os.path.exists(".multirepo"):
        exit("missing .git; to initial run: multi init <remote changes>")
    sh = """
        git --git-dir=.multirepo add .
        git --git-dir=.multirepo reset -- .multirepo
        git --git-dir=.multirepo commit -a -m "update"
        git --git-dir=.multirepo checkout %s
        git --git-dir=.multirepo reset --hard
        """ % branch
    call(sh, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return "Switched to %s" % branch


def call_done(remote_changes=None):
    if not os.path.exists(".multirepo"):
        exit("missing .multirepo; to initial run: multi init <remote changes>")
    call_to("CHANGES")
    if remote_changes:
        changes = Popen(
            "git --git-dir=.multirepo diff --name-only ORIG CHANGES",
            shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE
            ).communicate()[0]
        changes = changes.strip().split('\n')
        pswd = getpass.getpass(remote_changes.split(':')[0] + "'s password:")
        for f in changes:
            rsync = "rsync -Pravdtze ssh %s %s" % (f, remote_changes+f)
            child = pexpect.spawn(rsync)
            child.expect('password:')
            child.sendline(pswd)
            child.expect(pexpect.EOF)
            print(f + " \t\ttransfered")
    call_to("ORIG")
    call("rm -rf .multirepo", shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return "DONE"


def main(argv):
    if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
        exit("multi init <remote_changes>\t\tstarts\n" +
             "multi to <ORIG or CHANGES>\t\tnavigates to branch\n" +
             "multi pull <remote_changes>\t\tpulls remote changes branch\n" +
             "multi done [remote_changes]\t\tcopies changes back to remote " +
             "and ends")
    if argv[0] == 'init':
        if len(argv) <= 2:
            print(call_init(*argv[1:]))
        else:
            exit("multi init [remote_changes]")
    elif argv[0] == 'pull':
        if len(argv) == 2:
            print(call_pull(argv[1]))
        else:
            exit("multi pull <remote_changes>")
    elif argv[0] == 'to':
        if len(argv) < 2:
            head = Popen('cat .multirepo/HEAD', shell=True,
                         stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0]
            if 'ref: refs/heads/' in head:
                print(head.strip('ref: refs/heads/').strip('\n'))
            else:
                print('ORIG')
            exit("multi to <ORIG or CHANGES>")
        print(call_to(argv[1]))
    elif argv[0] == 'done':
        if len(argv) <= 2:
            print(call_done(*argv[1:]))
        else:
            exit("multi done [remote_changes]")
    else:
        exit("Not a multi command. See 'multi --help'.")


if __name__ == "__main__":
    main(sys.argv[1:])
