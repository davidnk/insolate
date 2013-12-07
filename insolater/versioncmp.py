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
import filecmp


def files_recursive(files_and_dirs, path_to='', path=''):
    files = []
    next_cur = []
    for f in files_and_dirs:
        if os.path.isfile(path_to+path+f):
            files.append(path+f)
        else:
            next_cur.append(f)
    for d in next_cur:
        files += files_recursive(os.listdir(path_to+path+d), path_to, path+d+'/')
    return files


def _dircmp_files(d, path=''):
    left = [path+f for f in d.left_only]
    changes = [path+f for f in d.diff_files]
    right = [path+f for f in d.right_only]
    for sd in d.subdirs:
        l, c, r = _dircmp_files(d.subdirs[sd], path+sd+'/')
        left += l
        changes += c
        right += r
    return left, changes, right


class VersionDiff(object):
    def __init__(self, repo, v1='', v2=''):
        self.repo = repo
        if v1 == '' or v2 == '':
            v2 = v1 or v2
            v2 = '.' if v2 == '' else (repo + '/versions/' + v2)
            v1 = repo + '/versions/original'
        else:
            v1, v2 = repo + '/versions/' + v1, repo + '/versions/' + v2
        self.v1, self.v2 = v1+'/', v2+'/'
        d = filecmp.dircmp(v1, v2, ignore=[repo])
        self.removed, self.changed, self.added = _dircmp_files(d)

    def added_files_recursive(self):
        try:
            self._added_files
        except:
            self._added_files = files_recursive(self.added, self.v2)
        return self._added_files

    def removed_files_recursive(self):
        try:
            self._removed_files
        except:
            self._removed_files = files_recursive(self.removed, self.v1)
        return self._removed_files
