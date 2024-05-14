import sys

from PySide6 import QtWidgets

from . import QDir

# noinspection PyArgumentList
if not QtWidgets.QApplication.instance():
    if getattr(sys, 'frozen', None):
        # noinspection PyArgumentList
        QtWidgets.QApplication.addLibraryPath(QDir.currentPath())

    # noinspection PyTypeChecker,PyCallByClass
    QtWidgets.QApplication.setStyle('Fusion')
    QtWidgets.QApplication([])
