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

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QKeySequence, QIcon
from PySide6.QtCore import SLOT

from helper.usesqapplication import UsesQApplication


class QMenuAddAction(UsesQApplication):

    def setUp(self):
        super(QMenuAddAction, self).setUp()
        self.menu = QMenu()

    def tearDown(self):
        del self.menu
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        super(QMenuAddAction, self).tearDown()

    def testAddActionWithoutKeySequenceCallable(self):
        # bug #280
        action = self.menu.addAction(self.app.tr('aaa'), lambda: 1)

    def testAddActionKeySequenceCallable(self):
        # bug #228
        action = self.menu.addAction(self.app.tr('aaa'), lambda: 1,
                                    QKeySequence(self.app.tr('Ctrl+O')))

    def testAddActionKeySequenceSlot(self):
        action = self.menu.addAction('Quit', self.app, SLOT('quit()'),
                                    QKeySequence('Ctrl+O'))


class QMenuAddActionWithIcon(UsesQApplication):

    def setUp(self):
        super(QMenuAddActionWithIcon, self).setUp()
        self.menu = QMenu()
        self.icon = QIcon()

    def tearDown(self):
        del self.menu
        del self.icon
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        super(QMenuAddActionWithIcon, self).tearDown()

    def testAddActionWithoutKeySequenceCallable(self):
        # bug #280
        action = self.menu.addAction(self.icon, self.app.tr('aaa'), lambda: 1)

    def testAddActionKeySequenceCallable(self):
        # bug #228
        action = self.menu.addAction(self.icon, self.app.tr('aaa'), lambda: 1,
                                    QKeySequence(self.app.tr('Ctrl+O')))

    def testAddActionKeySequenceSlot(self):
        action = self.menu.addAction(self.icon, 'Quit', self.app, SLOT('quit()'),
                                    QKeySequence('Ctrl+O'))


if __name__ == '__main__':
    unittest.main()
