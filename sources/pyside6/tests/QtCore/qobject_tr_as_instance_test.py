#!/usr/bin/python
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

'''Unit tests for QObject's tr static methods.'''

import gc
import os
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QObject

#from helper.usesqcoreapplication import UsesQCoreApplication


class QObjectTrTest(unittest.TestCase):
    '''Test case to check if QObject tr static methods could be treated as instance methods.'''

    def setUp(self):
        self.obj = QObject()

    def tearDown(self):
        del self.obj
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()

    def testTrCommonCase(self):
        # Test common case for QObject.tr
        invar1 = 'test1'
        outvar1 = self.obj.tr(invar1)
        invar2 = 'test2'
        outvar2 = self.obj.tr(invar2, 'test comment')
        self.assertEqual((invar1, invar2), (outvar1, outvar2))

    def testTrAsInstanceMethod(self):
        # Test QObject.tr as instance.
        # PYSIDE-1252: This works now as a class method!
        invar1 = 'test1'
        outvar1 = QObject.tr(invar1)
        invar2 = 'test2'
        outvar2 = QObject.tr(invar2, 'test comment')
        self.assertEqual((invar1, invar2), (outvar1, outvar2))


if __name__ == '__main__':
    unittest.main()

