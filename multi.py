#! /usr/bin/python
import os, sys
from subprocess import check_output, call, PIPE

def call_init(remote_changes=None):
    if os.path.exists(".git"):
        exit("Already initialized.  To finish and backup run: mulit done <remote backup>")
    sh = """
        git init
        git add .
        git commit -a -m "Original files"
        git tag -a ORIG -m "original files"
        git branch CHANGES
        git checkout CHANGES
        """
    call(sh, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    if remote_changes:
        sh = """
            rsync -Pravdtze ssh %s .
            git add .
            git commit -a -m "Initial changes"
            """ % remote_changes
        call(sh, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    print "Initialized branches ORIG, CHANGES"

def call_to(branch):
    if not os.path.exists(".git"):
        exit("missing .git; to initial run: multi init <remote changes>")
    sh = """
        git add .
        git commit -a -m "update"
        git checkout %s
        git reset --hard
        """ % branch
    call(sh, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    print "Switched to %s" % branch

def call_done(remote_changes=None):
    if not os.path.exists(".git"):
        exit("missing .git; to initial run: multi init <remote changes>")
    call_to("CHANGES")
    if remote_changes:
        changes = check_output("git diff --name-only ORIG CHANGES", shell=True)
        changes = changes.strip().split('\n')
        for f in changes:
            call("rsync -Pravdtze ssh  %s" % remote_changes, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    call_to("ORIG")
    call("rm -rf .git", shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    print "DONE"

def main(argv):
    if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
        exit("multi init <remote_changes>\t\tstarts\n" + \
             "multi to <ORIG or CHANGES>\t\tnavigates to branch\n" + \
             "multi done [remote_changes]\t\tcopies changes back to remote and ends")
    if argv[0] == 'init':
        if len(argv) <= 2:
            call_init(*argv[1:])
        else:
            exit("multi init [remote_changes]")
    elif argv[0] == 'to':
        if len(argv) < 2:
            exit("multi to <ORIG or CHANGES>")
        call_to(argv[1])
    elif argv[0] == 'done':
        if len(argv) <= 2:
            call_done(*argv[1:])
        else:
            exit("multi done [remote_changes]")
    else:
        exit("Not a multi command. See 'multi --help'.")

if __name__ == "__main__":
    main(sys.argv[1:])
