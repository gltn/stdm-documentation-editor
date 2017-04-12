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
        AddLanguage.resize(468, 238)
        self.verticalLayout = QtGui.QVBoxLayout(AddLanguage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.toolBox = QtGui.QToolBox(AddLanguage)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 446, 119))
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.page_3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.page_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.select_language_cbo = QtGui.QComboBox(self.page_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_language_cbo.sizePolicy().hasHeightForWidth())
        self.select_language_cbo.setSizePolicy(sizePolicy)
        self.select_language_cbo.setObjectName(_fromUtf8("select_language_cbo"))
        self.horizontalLayout.addWidget(self.select_language_cbo)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.toolBox.addItem(self.page_3, _fromUtf8(""))
        self.page_4 = QtGui.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 446, 119))
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.page_4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.page_4)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(self.page_4)
        self.name.setMaxLength(320)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.page_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.code = QtGui.QLineEdit(self.page_4)
        self.code.setMaxLength(10)
        self.code.setObjectName(_fromUtf8("code"))
        self.gridLayout.addWidget(self.code, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.label_3 = QtGui.QLabel(self.page_4)
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.toolBox.addItem(self.page_4, _fromUtf8(""))
        self.verticalLayout.addWidget(self.toolBox)
        self.buttonBox = QtGui.QDialogButtonBox(AddLanguage)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddLanguage)
        self.toolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddLanguage.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddLanguage.reject)
        QtCore.QMetaObject.connectSlotsByName(AddLanguage)

    def retranslateUi(self, AddLanguage):
        AddLanguage.setWindowTitle(_translate("AddLanguage", "Add a New Language", None))
        self.label_4.setText(_translate("AddLanguage", "Language", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("AddLanguage", "Select a Language", None))
        self.label.setText(_translate("AddLanguage", "Language Name", None))
        self.label_2.setText(_translate("AddLanguage", "Language Code", None))
        self.label_3.setText(_translate("AddLanguage", "<html><head/><body><p>For more information on ISO 639-1 country language codes refer <a href=\"https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes\"><span style=\" text-decoration: underline; color:#0000ff;\">this link</span></a>.</p></body></html>", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("AddLanguage", "Create a Language", None))

