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

import subprocess


def init(repo):
    _run_git(repo, "--work-tree=. init")
    with open(repo+'/info/exclude', 'a') as f:
        f.write('\n'+repo)
    _run_git(repo, "add -A .")
    _run_git(repo, "commit -am 'Original files'")
    _run_git(repo, "branch original")
    _run_git(repo, "checkout -b current_version")
    with open(repo+'/current_version', 'w') as f:
        f.write('original')


def current_version(repo):
    with open(repo+'/current_version', 'r') as f:
        return f.readline().strip()


def save_version(repo, version=''):
    if version == '':
        version = current_version(repo)
    _run_git(repo, "add -A .")
    _run_git(repo, "commit -am 'update'")
    _run_git(repo, "branch -D "+version)
    _run_git(repo, "branch -m current_version "+version)
    _run_git(repo, "checkout -b current_version")
    with open(repo+'/current_version', 'w') as f:
        f.write(version)


def open_version(repo, version):
    _run_git(repo, "add -A .")
    _run_git(repo, "commit -am 'clear staging'")
    _run_git(repo, "branch "+version)
    _run_git(repo, "checkout "+version)
    _run_git(repo, "reset --hard")
    _run_git(repo, "branch -D current_version")
    _run_git(repo, "checkout -b current_version")
    with open(repo+'/current_version', 'w') as f:
        f.write(version)


def _run(command):
    """Replace instances of {repo} with repo and run the command."""
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exit_code = proc.poll()
    return exit_code, out, err


def _run_git(repo, command):
    """Runs git --git-dir={repo} command."""
    return _run("git --git-dir=" + repo + " " + command)


def _run_git_add(repo, filepatterns=[]):
    """Runs git --git-dir={repo} add -A for each filepattern."""
    sh = ""
    for fp in filepatterns:
        sh += "git --git-dir={repo} add -A " + fp + ";".format(fp)
    return _run(sh)
