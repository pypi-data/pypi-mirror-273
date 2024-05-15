import sys

from PySide6 import QtWidgets

from PySide6.QtCore import QDir

app = QtWidgets.QApplication.instance()
# noinspection PyArgumentList
if not app:
    app = QtWidgets.QApplication(sys.argv)
    if getattr(sys, 'frozen', None):
        # noinspection PyArgumentList
        app.addLibraryPath(QDir.currentPath())

    # noinspection PyTypeChecker,PyCallByClass
    app.setStyle('Fusion')
