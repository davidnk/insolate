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
    """Create repo to store versions.
    Save original version."""
    if not os.path.isdir(repo):
        os.mkdir(repo)
        os.mkdir(repo+'/removed')
        os.mkdir(repo+'/versions')
        with open(repo+'/current_version', 'w') as f:
            f.write('original')
        shutil.copytree('.', repo + '/versions/original', ignore=shutil.ignore_patterns(repo))


def is_version(repo, version):
    """Returns whether the specified version exists."""
    return os.path.isdir(repo+'/versions/'+version)


def all_versions(repo):
    return filter(lambda x: x[0] != '_', os.listdir(repo+'/versions/'))


def current_version(repo):
    """Return the current version."""
    with open(repo+'/current_version', 'r') as f:
        return f.readline().strip()


def open_version(repo, version):
    """Open the specified version.
    Changes are discarded (may be saved into current_version).
    If specified version does not exist, no changes are made."""
    if not is_version(repo, version):
        return
    vp = repo + '/versions/' + version + '/'
    for f in os.listdir('.'):
        if f != repo:
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


def save_version(repo, version=''):
    """Save current into the specified version.
    If no version is supplied save current version.
    Will overwrite old version with the same name.
    Saving to original version is not guarenteed to save."""
    #TODO: merging changes
    if version == '':
        version = current_version(repo)
    if version == 'original':
        return
    version_path = repo + '/versions/' + version
    if os.path.isdir(version_path):
        shutil.rmtree(version_path)
    shutil.copytree('.', version_path, ignore=shutil.ignore_patterns(repo))


def delete_version(repo, version):
    """Delete the specified version if it exists and it is not the current or original version."""
    if ((not is_version(repo, version)) or
            version == 'original' or
            current_version(repo) == version):
        return
    shutil.rmtree(repo+'/versions/'+version)
