#!/usr/bin/env python

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

"""Tests covering signal emission and receiving to python slots"""

import gc
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QObject, SIGNAL, SLOT

try:
    from PySide6.QtWidgets import QSpinBox, QPushButton
    hasQtGui = True
except ImportError:
    hasQtGui = False

from helper.basicpyslotcase import BasicPySlotCase
from helper.usesqapplication import UsesQApplication

if hasQtGui:
    class ButtonPySlot(UsesQApplication, BasicPySlotCase):
        """Tests the connection of python slots to QPushButton signals"""

        def testButtonClicked(self):
            """Connection of a python slot to QPushButton.clicked()"""
            button = QPushButton('Mylabel')
            button.clicked.connect(self.cb)
            self.args = tuple()
            button.emit(SIGNAL('clicked(bool)'), False)
            self.assertTrue(self.called)

        def testButtonClick(self):
            """Indirect qt signal emission using the QPushButton.click() method """
            button = QPushButton('label')
            button.clicked.connect(self.cb)
            self.args = tuple()
            button.click()
            self.assertTrue(self.called)


if hasQtGui:
    class SpinBoxPySlot(UsesQApplication, BasicPySlotCase):
        """Tests the connection of python slots to QSpinBox signals"""

        def setUp(self):
            super(SpinBoxPySlot, self).setUp()
            self.spin = QSpinBox()

        def tearDown(self):
            del self.spin
            # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
            gc.collect()
            super(SpinBoxPySlot, self).tearDown()

        def testSpinBoxValueChanged(self):
            """Connection of a python slot to QSpinBox.valueChanged(int)"""
            self.spin.valueChanged.connect(self.cb)
            self.args = [3]
            self.spin.emit(SIGNAL('valueChanged(int)'), *self.args)
            self.assertTrue(self.called)

        def testSpinBoxValueChangedImplicit(self):
            """Indirect qt signal emission using QSpinBox.setValue(int)"""
            self.spin.valueChanged.connect(self.cb)
            self.args = [42]
            self.spin.setValue(self.args[0])
            self.assertTrue(self.called)

        def atestSpinBoxValueChangedFewArgs(self):
            """Emission of signals with fewer arguments than needed"""
            # XXX: PyQt4 crashes on the assertRaises
            self.spin.valueChanged.connect(self.cb)
            self.args = (554,)
            self.assertRaises(TypeError, self.spin.emit, SIGNAL('valueChanged(int)'))

if hasQtGui:
    class QSpinBoxQtSlots(UsesQApplication):
        """Tests the connection to QSpinBox qt slots"""

        qapplication = True

        def testSetValueIndirect(self):
            """Indirect signal emission: QSpinBox using valueChanged(int)/setValue(int)"""
            spinSend = QSpinBox()
            spinRec = QSpinBox()

            spinRec.setValue(5)

            spinSend.valueChanged.connect(spinRec.setValue)
            self.assertEqual(spinRec.value(), 5)
            spinSend.setValue(3)
            self.assertEqual(spinRec.value(), 3)
            self.assertEqual(spinSend.value(), 3)

        def testSetValue(self):
            """Direct signal emission: QSpinBox using valueChanged(int)/setValue(int)"""
            spinSend = QSpinBox()
            spinRec = QSpinBox()

            spinRec.setValue(5)
            spinSend.setValue(42)

            spinSend.valueChanged.connect(spinRec.setValue)
            self.assertEqual(spinRec.value(), 5)
            self.assertEqual(spinSend.value(), 42)
            spinSend.emit(SIGNAL('valueChanged(int)'), 3)

            self.assertEqual(spinRec.value(), 3)
            # Direct emission shouldn't change the value of the emitter
            self.assertEqual(spinSend.value(), 42)

            spinSend.emit(SIGNAL('valueChanged(int)'), 66)
            self.assertEqual(spinRec.value(), 66)
            self.assertEqual(spinSend.value(), 42)


if __name__ == '__main__':
    unittest.main()
