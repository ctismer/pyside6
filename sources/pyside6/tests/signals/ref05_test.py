#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from PySide6.QtCore import QObject, QCoreApplication, QTimeLine, Slot
from helper.usesqcoreapplication import UsesQCoreApplication


class ExtQObject(QObject):

    def __init__(self):
        super().__init__()
        self.counter = 0

    @Slot('qreal')
    def foo(self, value):
        self.counter += 1


class UserSlotTest(UsesQCoreApplication):

    def setUp(self):
        UsesQCoreApplication.setUp(self)
        self.receiver = ExtQObject()
        self.timeline = QTimeLine(100)

    def tearDown(self):
        del self.timeline
        del self.receiver
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        UsesQCoreApplication.tearDown(self)

    def testUserSlot(self):
        self.timeline.setUpdateInterval(10)

        self.timeline.finished.connect(self.app.quit)

        self.timeline.valueChanged.connect(self.receiver.foo)
        self.timeline.start()

        self.app.exec()

        self.assertTrue(self.receiver.counter > 1)


if __name__ == '__main__':
    unittest.main()

