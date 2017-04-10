# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_language.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_AddLanguage(object):
    def setupUi(self, AddLanguage):
        AddLanguage.setObjectName(_fromUtf8("AddLanguage"))
        AddLanguage.resize(347, 149)
        self.verticalLayout = QtGui.QVBoxLayout(AddLanguage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(AddLanguage)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(AddLanguage)
        self.name.setMaxLength(320)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(AddLanguage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.code = QtGui.QLineEdit(AddLanguage)
        self.code.setMaxLength(10)
        self.code.setObjectName(_fromUtf8("code"))
        self.gridLayout.addWidget(self.code, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_3 = QtGui.QLabel(AddLanguage)
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.buttonBox = QtGui.QDialogButtonBox(AddLanguage)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddLanguage)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddLanguage.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddLanguage.reject)
        QtCore.QMetaObject.connectSlotsByName(AddLanguage)

    def retranslateUi(self, AddLanguage):
        AddLanguage.setWindowTitle(_translate("AddLanguage", "Add a New Language", None))
        self.label.setText(_translate("AddLanguage", "Language Name", None))
        self.label_2.setText(_translate("AddLanguage", "Language Code", None))
        self.label_3.setText(_translate("AddLanguage", "<html><head/><body><p>For more information on ISO 639-1 country language codes refer <a href=\"https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes\"><span style=\" text-decoration: underline; color:#0000ff;\">this link</span></a>.</p></body></html>", None))

