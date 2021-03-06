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

import os
import sys
import time
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QRunnable, QThread, QThreadPool


thread_function_called = False


class thread_function():
    global thread_function_called
    thread_function_called = True


class Task(QRunnable):
    def run(self):
        QThread.sleep(2)  # Sleep 2 seconds


class QThreadPoolTest(unittest.TestCase):
    def testSlowJobs(self):
        '''This used to cause a segfault due the ownership control on
           globalInstance function'''
        for i in range(3):
            task = Task()
            QThreadPool.globalInstance().start(task)
            time.sleep(1)  # Sleep 1 second

        QThreadPool.globalInstance().waitForDone()

    def testCallable(self):
        global thread_function_called
        tp = QThreadPool.globalInstance()
        tp.start(thread_function)
        tp.waitForDone()
        self.assertTrue(thread_function_called)


if __name__ == '__main__':
    unittest.main()
