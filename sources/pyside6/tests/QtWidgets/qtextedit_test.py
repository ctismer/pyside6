#############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the test suite of Qt for Python.
##
## $QT_BEGIN_LICENSE:GPL-EXCEPT$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3 as published by the Free Software
## Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

'''Test cases for QTextEdit and ownership problems.'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtWidgets import QTextEdit

from helper.usesqapplication import UsesQApplication


class DontTouchReference(UsesQApplication):
    '''Check if the QTextTable returned by QTextCursor.insertTable() is not
    referenced by the QTextCursor that returns it.'''

    def setUp(self):
        super(DontTouchReference, self).setUp()
        self.editor = QTextEdit()
        self.cursor = self.editor.textCursor()
        self.table = self.cursor.insertTable(1, 1)

    @unittest.skipUnless(hasattr(sys, "getrefcount"), f"{sys.implementation.name} has no refcount")
    def testQTextTable(self):
        # methods which return QTextTable should not increment its reference
        self.assertEqual(sys.getrefcount(self.table), 2)
        f = self.cursor.currentFrame()
        del f
        self.assertEqual(sys.getrefcount(self.table), 2)
        # destroying the cursor should not raise any "RuntimeError: internal
        # C++ object already deleted." when accessing the QTextTable
        del self.cursor
        self.assertEqual(sys.getrefcount(self.table), 2)
        cell = self.table.cellAt(0, 0)


if __name__ == "__main__":
    unittest.main()
