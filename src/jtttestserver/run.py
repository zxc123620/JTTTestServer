#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2026/9/6 20:26
# Author:zhouxiaochuan
# Description:
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)
engine= QQmlApplicationEngine()
engine.load(QUrl("../qml/main.qml"))
if not engine.rootObjects():
    sys.exit(-1)

exec_code = app.exec()
del engine
sys.exit(exec_code)