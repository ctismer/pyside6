#############################################################################
##
## Copyright (C) 2021 The Qt Company Ltd.
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

import gc
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtWidgets import QListWidget, QListWidgetItem
from helper.usesqapplication import UsesQApplication


class QListWidgetItemConstructor(UsesQApplication):

    def setUp(self):
        super(QListWidgetItemConstructor, self).setUp()
        self.widgetList = QListWidget()

    def tearDown(self):
        del self.widgetList
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        super(QListWidgetItemConstructor, self).tearDown()

    def testConstructorWithParent(self):
        # Bug 235 - QListWidgetItem constructor not saving ownership
        QListWidgetItem(self.widgetList)
        item = self.widgetList.item(0)
        self.assertEqual(item.listWidget(), self.widgetList)

    def testConstructorWithNone(self):
        # Bug 452 - QListWidgetItem() not casting NoneType to null correctly.
        item = QListWidgetItem(None, 123)


if __name__ == '__main__':
    unittest.main()
