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

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolBox, QWidget

from helper.usesqapplication import UsesQApplication


class OwnershipControl(UsesQApplication):

    def setUp(self):
        super(OwnershipControl, self).setUp()
        self.toolbox = QToolBox()

    def tearDown(self):
        del self.toolbox
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        super(OwnershipControl, self).tearDown()

    def testAddItem(self):
        # Was losing ownership of the widget.
        index = self.toolbox.addItem(QWidget(), 'item')
        item = self.toolbox.widget(index)
        self.assertTrue(isinstance(item, QWidget))

    def testAddItemWithIcon(self):
        index = self.toolbox.addItem(QWidget(), QIcon(), 'item')
        item = self.toolbox.widget(index)
        self.assertTrue(isinstance(item, QWidget))


if __name__ == '__main__':
    unittest.main()
