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

''' Test case for QObject.receivers()'''

import gc
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QObject, SIGNAL, SLOT


def cute_slot():
    pass


class TestQObjectReceivers(unittest.TestCase):
    '''Test case for QObject::receivers'''

    def testBasic(self):
        sender = QObject()
        receiver1 = QObject()
        receiver2 = QObject()
        self.assertEqual(sender.receivers(SIGNAL("")), 0)
        sender.destroyed.connect(receiver1.deleteLater)
        self.assertEqual(sender.receivers(SIGNAL("destroyed()")), 1)
        sender.destroyed.connect(receiver2.deleteLater)
        self.assertEqual(sender.receivers(SIGNAL("destroyed()")), 2)
        sender.disconnect(sender, SIGNAL("destroyed()"), receiver2, SLOT("deleteLater()"))
        self.assertEqual(sender.receivers(SIGNAL("destroyed()")), 1)
        del receiver2
        del receiver1
        del sender
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()

    def testPySlots(self):
        sender = QObject()
        receiver = QObject()
        sender.destroyed.connect(cute_slot)
        self.assertEqual(sender.receivers(SIGNAL("destroyed( )")), 1)
        sender.destroyed.connect(receiver.deleteLater)
        self.assertEqual(sender.receivers(SIGNAL("destroyed()")), 2)
        del sender
        del receiver
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()

    def testPySignals(self):
        sender = QObject()
        receiver = QObject()
        sender.connect(sender, SIGNAL("some_dynamic_signal()"), cute_slot)
        self.assertEqual(sender.receivers(SIGNAL("some_dynamic_signal(  )")), 1)
        sender.connect(sender, SIGNAL("some_dynamic_signal()"), receiver, SLOT("deleteLater()"))
        self.assertEqual(sender.receivers(SIGNAL("some_dynamic_signal(  )")), 2)


if __name__ == '__main__':
    unittest.main()
