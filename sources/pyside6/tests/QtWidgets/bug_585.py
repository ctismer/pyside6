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

'''Test bug 585: http://bugs.openbossa.org/show_bug.cgi?id=585'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem


class Bug585(unittest.TestCase):
    @unittest.skipUnless(hasattr(sys, "getrefcount"), f"{sys.implementation.name} has no refcount")
    def testCase(self):
        app = QApplication([])
        self._tree = QTreeWidget()
        self._tree.setColumnCount(2)
        i1 = QTreeWidgetItem(self._tree, ['1', ])
        i2 = QTreeWidgetItem(self._tree, ['2', ])
        refCount = sys.getrefcount(i1)

        # this function return None
        # because the topLevelItem does not has a parent item
        # but still have a TreeWidget as a parent
        self._tree.topLevelItem(0).parent()

        self.assertEqual(refCount, sys.getrefcount(i1))


if __name__ == '__main__':
    unittest.main()

