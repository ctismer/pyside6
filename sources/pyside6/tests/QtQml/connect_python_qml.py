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

'''
Test case for bug #442

archive:
https://srinikom.github.io/pyside-bz-archive/442.html
'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from helper.helper import quickview_errorstring
from helper.timedqguiapplication import TimedQGuiApplication
from PySide6.QtCore import QObject, QUrl, SIGNAL
from PySide6.QtGui import QColor
from PySide6.QtQuick import QQuickItem, QQuickView


class TestConnectionWithInvalidSignature(TimedQGuiApplication):
    def onButtonClicked(self):
        self.buttonClicked = True
        self.app.quit()

    def onButtonFailClicked(self):
        pass

    def testFailConnection(self):
        self.buttonClicked = False
        self.buttonFailClicked = False
        view = QQuickView()
        file = Path(__file__).resolve().parent / 'connect_python_qml.qml'
        self.assertTrue(file.is_file())
        view.setSource(QUrl.fromLocalFile(file))
        root = view.rootObject()
        self.assertTrue(root, quickview_errorstring(view))
        button = root.findChild(QObject, "buttonMouseArea")
        self.assertRaises(TypeError, QObject.connect, [button,SIGNAL('entered()'), self.onButtonFailClicked])
        button.entered.connect(self.onButtonClicked)
        button.entered.emit()
        view.show()
        self.app.exec()
        self.assertTrue(self.buttonClicked)


if __name__ == '__main__':
    unittest.main()
