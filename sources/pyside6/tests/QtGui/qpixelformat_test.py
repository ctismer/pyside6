#############################################################################
##
## Copyright (C) 2017 The Qt Company Ltd.
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

'''Unit test for QPixelFormat'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from helper.usesqguiapplication import UsesQGuiApplication
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QImage, QPixelFormat, qPixelFormatRgba


class QPixelFormatTest(UsesQGuiApplication):
    def test(self):
        image = QImage(QSize(200, 200), QImage.Format_ARGB32)
        image.fill(QColor(Qt.red))
        pixelFormat = image.pixelFormat()
        print(pixelFormat.greenSize())
        self.assertEqual(pixelFormat.alphaSize(), 8)
        self.assertEqual(pixelFormat.redSize(), 8)
        self.assertEqual(pixelFormat.greenSize(), 8)
        self.assertEqual(pixelFormat.blueSize(), 8)
        self.assertEqual(pixelFormat.bitsPerPixel(), 32)

    def testHelpers(self):
        format = qPixelFormatRgba(8, 8, 8, 8, QPixelFormat.UsesAlpha,
                                  QPixelFormat.AtBeginning, QPixelFormat.Premultiplied,
                                  QPixelFormat.UnsignedByte)
        self.assertEqual(format.redSize(), 8)


if __name__ == '__main__':
    unittest.main()
