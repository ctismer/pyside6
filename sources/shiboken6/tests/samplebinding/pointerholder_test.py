#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

'''Test cases for a class that holds an arbitraty pointer and is modified to hold an PyObject.'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from shiboken_paths import init_paths
init_paths()

from sample import PointerHolder

class TestPointerHolder(unittest.TestCase):
    '''Test cases for a class that holds an arbitraty pointer and is modified to hold an PyObject.'''

    def testStoringAndRetrievingPointer(self):
        ph = PointerHolder('Hello')
        self.assertEqual(ph.pointer(), 'Hello')
        a = (1, 2, 3)
        ph = PointerHolder(a)
        self.assertEqual(ph.pointer(), a)

    @unittest.skipUnless(hasattr(sys, "getrefcount"), f"{sys.implementation.name} has no refcount")
    def testReferenceCounting(self):
        '''Test reference counting when retrieving data with PointerHolder.pointer().'''
        a = (1, 2, 3)
        refcnt = sys.getrefcount(a)
        ph = PointerHolder(a)
        ptr = ph.pointer()
        self.assertEqual(sys.getrefcount(a), refcnt + 1)

if __name__ == '__main__':
    unittest.main()

