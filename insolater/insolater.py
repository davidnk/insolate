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

from __future__ import absolute_import
from __future__ import print_function

import os
import subprocess
import getpass
import pexpect


class Insolater(object):
    _CMD = __file__.split('/')[-1]
    _NOT_INIT_MESSAGE = "No session found. See '{cmd} init <remote changes>'".format(cmd=_CMD)
    _ALREADY_INIT_MESSAGE = (
        "Already initialized. To end session use: {cmd} exit [<remote backup>]".format(cmd=_CMD))

    def __init__(self, repo=".insolater_repo", timeout=5, filepattern="."):
        self.repo = repo
        self.timeout = timeout
        self.filepattern = filepattern.split()

    def init(self, remote_changes=None):
        """Create repo and branches, add current files, optionally add remote changes."""
        self._verify_repo_exists(False)
        self._run_git("--work-tree=. init")
        self._run("echo '{repo}' >> {repo}/info/exclude")
        self._run_git_add()
        self._run_git("commit -am 'Original files'")
        self._run_git("tag -a ORIG -m 'original files'")
        self._run_git("branch CHANGES")
        self._run_git("checkout CHANGES")
        if remote_changes:
            self.pull(remote_changes)
        return "Initialized versions ORIG, CHANGES"

    def change_branch(self, branch):
        """Save changes, switch to the supplied branch, restore branch to saved condition."""
        self._verify_repo_exists(True)
        self._run_git_add()
        self._run_git("commit -am 'update'")
        self._run_git("checkout " + branch)
        self._run_git("reset --hard")
        return "Switched to %s" % branch

    def pull(self, remote_changes):
        """Pull remote changes into local CHANGES branch."""
        head = self.get_current_branch()
        self.change_branch('CHANGES')
        retv = self._run("rsync -Pravdtze ssh {0} .".format(remote_changes))[0]
        self._run_git_add()
        self._run_git("commit -am 'Pulled changes'")
        self.change_branch(head)
        if (retv != 0):
            raise Exception("Failed to sync changes")
        return "Pulled updates"

    def push(self, remote_location):
        """Push changes to remote location."""
        head = self.get_current_branch()
        self.change_branch("CHANGES")
        changes = self._run_git("diff --name-only ORIG CHANGES")[1]
        changes = changes.strip().split('\n')
        pswd = getpass.getpass(remote_location.split(':')[0] + "'s password:")
        transfer_str = ""
        for f in changes:
            rsync = "rsync -R -Pravdtze ssh " + f + " " + remote_location
            exitstatus = 0
            try:
                exitstatus = self._run_with_password(rsync, pswd, self.timeout)[0]
            except pexpect.TIMEOUT:
                raise Exception("Aborted (File transfer timeouted out)")
            if exitstatus != 0:
                transfer_str += f + " \t\tFailed to transfer\n"
                raise Exception(transfer_str + "Aborted (File transfer failed).")
            transfer_str += f + " \t\ttransfered\n"
        self.change_branch(head)
        return transfer_str

    def exit(self, remote_location=None, discard_changes=None):
        """Restore original files, and delete changes (delete repo).
        Optionally send changed files to a remote location."""
        self._save_cur()
        transfers = ""
        if remote_location:
            transfers = self.push(remote_location)
        elif self._run_git("diff --name-only ORIG CHANGES")[1].strip() != '':
            if discard_changes is None:
                discard = raw_input("Do you want to discard changes (y/[n]): ")
                discard_changes = discard.lower() == 'y'
            if not discard_changes:
                return "Aborted to avoid discarding changes."
        self.change_branch("ORIG")
        self._run("rm -rf {repo}")
        return (transfers + "Session Ended")

    def get_current_branch(self):
        """Returns the current branch.  This may be a hash value."""
        self._verify_repo_exists(True)
        cur = self._run("cat {repo}/HEAD")[1]
        if 'ref: refs/heads/' in cur:
            cur = cur.strip('ref: refs/heads/').strip()
        return cur

    def _verify_repo_exists(self, exists):
        """raise and exception if the repo does not have the specfied state of being."""
        if exists:
            if not os.path.exists(self.repo):
                raise Exception(Insolater._NOT_INIT_MESSAGE)
        else:
            if os.path.exists(self.repo):
                raise Exception(Insolater._ALREADY_INIT_MESSAGE)

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

    def _run_git_add(self):
        """Runs git --git-dir={repo} add -A for each filepattern."""
        sh = ""
        for fp in self.filepattern:
            sh += "git --git-dir={repo} add -A " + fp + ";".format(fp)
        return self._run(sh)

    def _run_with_password(self, command, pswd, timeout=5):
        """Replace instances of {repo} with self.repo and run the command using the password."""
        proc = pexpect.spawn(command.format(repo=self.repo))
        proc.expect('password:')
        proc.sendline(pswd)
        proc.expect(pexpect.EOF, timeout=timeout)
        return proc.isalive(), proc.read(), ''
