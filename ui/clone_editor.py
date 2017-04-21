# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clone_editor.ui'
#
# Created: Fri Apr 21 11:41:16 2017
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
        CloneEditor.resize(425, 199)
        self.verticalLayout = QtGui.QVBoxLayout(CloneEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(CloneEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.edtOut = QtGui.QTextEdit(CloneEditor)
        self.edtOut.setObjectName(_fromUtf8("edtOut"))
        self.verticalLayout.addWidget(self.edtOut)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnClone = QtGui.QPushButton(CloneEditor)
        self.btnClone.setObjectName(_fromUtf8("btnClone"))
        self.horizontalLayout.addWidget(self.btnClone)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CloneEditor)
        QtCore.QMetaObject.connectSlotsByName(CloneEditor)

    def retranslateUi(self, CloneEditor):
        CloneEditor.setWindowTitle(_translate("CloneEditor", "Dialog", None))
        self.label.setText(_translate("CloneEditor", "Download documentation", None))
        self.btnClone.setText(_translate("CloneEditor", "Download", None))

