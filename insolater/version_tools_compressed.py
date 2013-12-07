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
import cPickle
from versioncmp import VersionDiff
from version_tools import init, current_version


def save_version(repo, version=''):
    if version == '':
        version = current_version(repo)
    version_path = repo + '/versions/' + version
    if os.path.isdir(version_path):
        #TODO: merging changes
        os.rmdir(version_path)
    os.mkdir(version_path)
    vd = VersionDiff(repo)
    for fp in vd.changed+vd.added_files_recursive():
        p, f = fp.rsplit('/', 1)
        p = version_path + '/' + p
        if not os.path.isdir(p):
            os.makedirs(p)
        shutil.copy2(fp, p+f)
    cPickle.dump(vd.removed_files_recursive(), repo+'/removed/'+version)


def open_version(repo, version):
    cv = current_version(repo)
    if cv == 'original':
        #TODO: overwrite?
        save_version(repo, 'head')
    else:
        save_version(repo, cv)
    vd = VersionDiff(repo)
    for fp in vd.changed:
        shutil.copy2(repo+'/versions/original/'+fp, fp)
    for fp in vd.added_files_recursive():
        os.remove(fp)
    vd = VersionDiff(repo, version)
    for fp in vd.changed:
        shutil.copy2(repo+'/versions/'+version+'/'+fp, fp)
    for fp in vd.added_files_recursive():
        p, f = fp.rsplit('/', 1)
        if not os.path.isdir(p):
            os.makedirs(p)
        shutil.copy2(repo+'/versions/'+version+'/'+fp, fp)
    removed = cPickle.load(repo+'/removed/'+version)
    for fp in removed:
        os.remove(fp)
    with open(repo+'/current_version', 'w') as f:
        f.write(version)
