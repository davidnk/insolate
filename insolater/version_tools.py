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
import shutil


def init(repo):
    if not os.path.isdir(repo):
        os.mkdir(repo)
        os.mkdir(repo+'/removed')
        os.mkdir(repo+'/versions')
        with open(repo+'/current_version', 'w') as f:
            f.write('original')
        shutil.copytree('.', repo + '/versions/original', ignore=shutil.ignore_patterns(repo))


def current_version(repo):
    with open(repo+'/current_version', 'r') as f:
        return f.readline().strip()


def save_version(repo, version=''):
    if version == '':
        version = current_version(repo)
    version_path = repo + '/versions/' + version
    if os.path.isdir(version_path):
        #TODO: merging changes
        shutil.rmtree(version_path)
    shutil.copytree('.', version_path, ignore=shutil.ignore_patterns(repo))
    with open(repo+'/current_version', 'w') as f:
        f.write(version)


def open_version(repo, version):
    cv = current_version(repo)
    vp = repo + '/versions/' + version + '/'
    if cv == 'original':
        #TODO: overwrite?
        save_version(repo, 'current_version')
    else:
        save_version(repo, cv)
    if not os.path.isdir(vp):
        save_version(repo, version)
    for f in os.listdir('.'):
        if f == repo:
            continue
        if os.path.isdir(f):
            shutil.rmtree(f)
        else:
            os.remove(f)
    for f in os.listdir(vp):
        if os.path.isdir(vp+f):
            shutil.copytree(vp+f, f)
        else:
            shutil.copy2(vp+f, f)
    with open(repo+'/current_version', 'w') as f:
        f.write(version)
