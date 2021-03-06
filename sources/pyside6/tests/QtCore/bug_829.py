#############################################################################
##
## Copyright (C) 2021 The Qt Company Ltd.
## Copyright (C) 2011 Thomas Perl <thp.io/about>
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

# Test case for PySide bug 829

import gc
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QDir, QSettings, QTemporaryFile


class QVariantConversions(unittest.TestCase):

    _confFileName = None

    def testDictionary(self):
        confFile = QTemporaryFile(QDir.tempPath() + '/pysidebug829_XXXXXX.ini')
        confFile.setAutoRemove(False)
        self.assertTrue(confFile.open())
        confFile.close()
        self._confFileName = confFile.fileName()
        del confFile
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        s = QSettings(self._confFileName, QSettings.IniFormat)
        self.assertEqual(s.status(), QSettings.NoError)
        # Save value
        s.setValue('x', {1: 'a'})
        s.sync()
        self.assertEqual(s.status(), QSettings.NoError)
        del s
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()

        # Restore value
        s = QSettings(self._confFileName, QSettings.IniFormat)
        self.assertEqual(s.status(), QSettings.NoError)
        self.assertEqual(s.value('x'), {1: 'a'})

    def __del__(self):
        if self._confFileName is not None:
            os.unlink(QDir.toNativeSeparators(self._confFileName))


if __name__ == '__main__':
    unittest.main()
