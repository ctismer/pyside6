#############################################################################
##
## Copyright (C) 2021 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the Qt for Python project.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import sys
import logging

from PySide6.QtCore import QDir, QFile, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtSql import QSqlDatabase

# We import the file just to trigger the QmlElement type registration.
import sqlDialog

logging.basicConfig(filename="chat.log", level=logging.DEBUG)
logger = logging.getLogger("logger")


def connectToDatabase():
    database = QSqlDatabase.database()
    if not database.isValid():
        database = QSqlDatabase.addDatabase("QSQLITE")
        if not database.isValid():
            logger.error("Cannot add database")

    write_dir = QDir("")
    if not write_dir.mkpath("."):
        logger.error("Failed to create writable directory")

    # Ensure that we have a writable location on all devices.
    abs_path = write_dir.absolutePath()
    filename = f"{abs_path}/chat-database.sqlite3"

    # When using the SQLite driver, open() will create the SQLite
    # database if it doesn't exist.
    database.setDatabaseName(filename)
    if not database.open():
        logger.error("Cannot open database")
        QFile.remove(filename)


if __name__ == "__main__":
    app = QGuiApplication()
    connectToDatabase()

    engine = QQmlApplicationEngine()
    engine.load(QUrl("chat.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    app.exec()
