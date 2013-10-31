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
#! /usr/bin/python

from __future__ import absolute_import
from __future__ import print_function

import os
import subprocess
import getpass
import pexpect


class Insolater(object):
    _CMD = __file__.split('/')[-1]
    _NOT_INIT_MESSAGE = "No session found. See '{cmd} init <remote changes>'".format(cmd=_CMD)
    _ALREADY_INIT_MESSAGE = "Already initialized. To end session use: mulit exit [<remote backup>]"

    def __init__(self, repo=".insolater_repo", timeout=5):
        self.repo = repo
        self.timeout = timeout

    def main(self, argv):
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
                print(self.start_session(*argv[1:])[1])
            else:
                print("Usage: {cmd} init [remote_changes]".format(cmd=Insolater._CMD))
        elif argv[0] == 'pull':
            if len(argv) == 2:
                print(self.pull_remote(argv[1]))
            else:
                print("Usage: {cmd} pull <remote_changes>".format(cmd=Insolater._CMD))
        elif argv[0] == 'push':
            if len(argv) == 2:
                print(self.push_remote(argv[1])[1])
            else:
                print("Usage: {cmd} push <remote_changes>".format(cmd=Insolater._CMD))
        elif argv[0] == 'pwd':
                head = self._get_current_branch()[1]
                if head == 'CHANGES':
                    print("Currently in CHANGES version.")
                else:
                    print('Currently in ORIG version.')
        elif argv[0] == 'cd':
            if len(argv) < 2:
                print("Usage: {cmd} cd <ORIG or CHANGES>".format(cmd=Insolater._CMD))
            else:
                print(self.change_branch(argv[1])[1])
        elif argv[0] == 'exit':
            if len(argv) <= 2:
                print(self.exit_session(*argv[1:])[1])
            else:
                print("Usage: {cmd} exit [<remote_changes>]".format(cmd=Insolater._CMD))
        else:
            print("Not a {cmd} command. See '{cmd} --help'.".format(cmd=Insolater._CMD))

    def start_session(self, remote_changes=None):
        """Create repo and branches, add current files, optionally add remote changes."""
        if self._repo_exists():
            return False, Insolater._ALREADY_INIT_MESSAGE
        self._run("echo '{repo}' >> .gitignore")
        self._run("echo '{fname}*' >> .gitignore".format(fname=__file__.split('/')[-1]))
        self._run("echo '.gitignore' >> .gitignore")
        self._run_git("--work-tree=. init")
        self._run_git("add .")
        self._run_git("commit -am 'Original files'")
        self._run_git("tag -a ORIG -m 'original files'")
        self._run_git("branch CHANGES")
        self._run_git("checkout CHANGES")
        if remote_changes:
            r = self.pull_remote(remote_changes)
            if not r[0]:
                return r
        return True, "Initialized versions ORIG, CHANGES"

    def change_branch(self, branch):
        """Save changes, switch to the supplied branch, restore branch to saved condition."""
        if not self._repo_exists():
            return False, Insolater._NOT_INIT_MESSAGE
        self._run_git("add .")
        self._run_git("commit -am 'update'")
        self._run_git("checkout " + branch)
        self._run_git("reset --hard")
        return True, "Switched to %s" % branch

    def pull_remote(self, remote_changes):
        """Pull remote changes into local CHANGES branch."""
        head = self._get_current_branch()[1]
        r = self.change_branch('CHANGES')
        if not r[0]:
            return r
        retv = self._run("rsync -Pravdtze ssh {0} .".format(remote_changes))[0]
        self._run_git("add .")
        self._run_git("commit -am 'Pulled changes'")
        self.change_branch(head)
        if (retv != 0):
            return False, "Failed to sync changes"
        return True, "Pulled updates"

    def push_remote(self, remote_location):
        """Push changes to remote location."""
        head = self._get_current_branch()[1]
        r = self.change_branch("CHANGES")
        if not r[0]:
            return r
        changes = self._run_git("diff --name-only ORIG CHANGES")[1]
        changes = changes.strip().split('\n')
        pswd = getpass.getpass(remote_location.split(':')[0] + "'s password:")
        transfer_str = ""
        all_sync = True
        for f in changes:
            rsync = "rsync -Pravdtze ssh %s %s" % (f, remote_location + f)
            exitstatus = 0
            try:
                exitstatus = self._run_with_password(rsync, pswd, self.timeout)[0]
            except pexpect.TIMEOUT:
                return False, "Timeout\n"
            if exitstatus != 0:
                transfer_str += f + " \t\tFailed to transfer\n"
                all_sync = False
            else:
                transfer_str += f + " \t\ttransfered\n"
        self.change_branch(head)
        return all_sync, transfer_str

    def exit_session(self, remote_changes=None):
        """Restore original files, and delete changes (delete repo).
        Optionally send changed files to a remote location."""
        r = self._save_cur()
        if not r[0]:
            return r
        transfers = ""
        if remote_changes:
            all_sync, transfers = self.push_remote(remote_changes)
            if not all_sync:
                return all_sync, (transfers + "Aborted (File transfer failed).")
        elif self._run_git("diff --name-only ORIG CHANGES")[1].strip() != '':
            discard = raw_input("Do you want to discard changes (y/[n]): ")
            if discard.lower() != 'y':
                return False, "Aborted to avoid discarding changes."
        self.change_branch("ORIG")
        self._run("rm -rf {repo}")
        return True, (transfers + "Session Ended")

    def _repo_exists(self):
        """Return whether or not the repo exists."""
        return os.path.exists(self.repo)

    def _get_current_branch(self):
        """Returns the current branch.  This may be a hash value."""
        if not self._repo_exists():
            return False, Insolater._NOT_INIT_MESSAGE
        cur = self._run("cat {repo}/HEAD")[1]
        if 'ref: refs/heads/' in cur:
            cur = cur.strip('ref: refs/heads/').strip()
        return True, cur

    def _save_cur(self):
        """Save progress of current branch"""
        return self.change_branch("HEAD")

    def _run(self, command):
        """Replace instances of {repo} with self.repo and run the command."""
        command = command.format(repo=self.repo)
        proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        exit_code = proc.poll()
        return exit_code, out, err

    def _run_git(self, command):
        """Runs git --git-dir={repo} command."""
        return self._run("git --git-dir={repo} " + command)

    def _run_with_password(self, command, pswd, timeout=5):
        """Replace instances of {repo} with self.repo and run the command using the password."""
        proc = pexpect.spawn(command.format(repo=self.repo))
        proc.expect('password:')
        proc.sendline(pswd)
        proc.expect(pexpect.EOF, timeout=timeout)
        return proc.isalive(), proc.read(), ''
