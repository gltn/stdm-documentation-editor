# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clone_editor.ui'
#
# Created: Sun Apr 23 13:02:24 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CloneEditor(object):
    def setupUi(self, CloneEditor):
        CloneEditor.setObjectName(_fromUtf8("CloneEditor"))
        CloneEditor.resize(317, 78)
        self.lblStatus = QtGui.QLabel(CloneEditor)
        self.lblStatus.setGeometry(QtCore.QRect(10, 10, 161, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblStatus.setFont(font)
        self.lblStatus.setTextFormat(QtCore.Qt.RichText)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.layoutWidget = QtGui.QWidget(CloneEditor)
        self.layoutWidget.setGeometry(QtCore.QRect(180, 40, 123, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnClone = QtGui.QPushButton(self.layoutWidget)
        self.btnClone.setObjectName(_fromUtf8("btnClone"))
        self.horizontalLayout.addWidget(self.btnClone)

        self.retranslateUi(CloneEditor)
        QtCore.QMetaObject.connectSlotsByName(CloneEditor)

    def retranslateUi(self, CloneEditor):
        CloneEditor.setWindowTitle(_translate("CloneEditor", "Dialog", None))
        self.lblStatus.setText(_translate("CloneEditor", "Download documentation", None))
        self.btnClone.setText(_translate("CloneEditor", "Download", None))

