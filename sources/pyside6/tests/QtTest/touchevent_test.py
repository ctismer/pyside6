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

from helper.usesqapplication import UsesQApplication

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPoint, QTimer, Qt, QEvent
from PySide6.QtGui import QTouchDevice
from PySide6.QtTest import QTest


class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._sequence = []
        # Fixme (Qt 5): The device needs to be registered (using
        # QWindowSystemInterface::registerTouchDevice()) for the test to work
        self._device = QTouchDevice()
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        QTimer.singleShot(200, self.generateEvent)

    def event(self, e):
        self._sequence.append(e.type())
        return QWidget.event(self, e)

    def generateEvent(self):
        o = QTest.touchEvent(self, self._device)
        o.press(0, QPoint(10, 10))
        o.commit()
        del o
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()

        QTest.touchEvent(self, self._device).press(0, QPoint(10, 10))
        QTest.touchEvent(self, self._device).stationary(0).press(1, QPoint(40, 10))
        QTest.touchEvent(self, self._device).move(0, QPoint(12, 12)).move(1, QPoint(45, 5))
        QTest.touchEvent(self, self._device).release(0, QPoint(12, 12)).release(1, QPoint(45, 5))
        QTimer.singleShot(200, self.deleteLater)


class TouchEventTest(UsesQApplication):
    def testCreateEvent(self):
        w = MyWidget()
        w.show()
        self.app.exec()
        # same values as C++
        self.assertEqual(w._sequence.count(QEvent.Type.TouchBegin), 2)
        self.assertEqual(w._sequence.count(QEvent.Type.TouchUpdate), 2)
        self.assertEqual(w._sequence.count(QEvent.Type.TouchEnd), 1)


if __name__ == '__main__':
    unittest.main()
