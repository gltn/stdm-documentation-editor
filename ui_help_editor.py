# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_help_editor.ui'
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

class Ui_HelpEditor(object):
    def setupUi(self, HelpEditor):
        HelpEditor.setObjectName(_fromUtf8("HelpEditor"))
        HelpEditor.resize(971, 669)
        self.centralwidget = QtGui.QWidget(HelpEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.layoutWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.add_language_cbo = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_language_cbo.sizePolicy().hasHeightForWidth())
        self.add_language_cbo.setSizePolicy(sizePolicy)
        self.add_language_cbo.setObjectName(_fromUtf8("add_language_cbo"))
        self.gridLayout.addWidget(self.add_language_cbo, 0, 2, 1, 1)
        self.stdm_version_cbo = QtGui.QComboBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stdm_version_cbo.sizePolicy().hasHeightForWidth())
        self.stdm_version_cbo.setSizePolicy(sizePolicy)
        self.stdm_version_cbo.setObjectName(_fromUtf8("stdm_version_cbo"))
        self.gridLayout.addWidget(self.stdm_version_cbo, 1, 1, 1, 2)
        self.language_cbo = QtGui.QComboBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language_cbo.sizePolicy().hasHeightForWidth())
        self.language_cbo.setSizePolicy(sizePolicy)
        self.language_cbo.setObjectName(_fromUtf8("language_cbo"))
        self.gridLayout.addWidget(self.language_cbo, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.toc_container = QtGui.QVBoxLayout()
        self.toc_container.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.toc_container.setSpacing(0)
        self.toc_container.setObjectName(_fromUtf8("toc_container"))
        self.verticalLayout_2.addLayout(self.toc_container)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.image_browse_btn = QtGui.QPushButton(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_browse_btn.sizePolicy().hasHeightForWidth())
        self.image_browse_btn.setSizePolicy(sizePolicy)
        self.image_browse_btn.setObjectName(_fromUtf8("image_browse_btn"))
        self.verticalLayout_3.addWidget(self.image_browse_btn)
        self.image_browser = QtWebKit.QWebView(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_browser.sizePolicy().hasHeightForWidth())
        self.image_browser.setSizePolicy(sizePolicy)
        self.image_browser.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.image_browser.setObjectName(_fromUtf8("image_browser"))
        self.verticalLayout_3.addWidget(self.image_browser)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.content_editor = QtWebKit.QWebView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.content_editor.sizePolicy().hasHeightForWidth())
        self.content_editor.setSizePolicy(sizePolicy)
        self.content_editor.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.content_editor.setObjectName(_fromUtf8("content_editor"))
        self.verticalLayout_4.addWidget(self.splitter)
        HelpEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(HelpEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 971, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuRegister = QtGui.QMenu(self.menubar)
        self.menuRegister.setObjectName(_fromUtf8("menuRegister"))
        HelpEditor.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(HelpEditor)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        HelpEditor.setStatusBar(self.statusbar)
        self.action_submit = QtGui.QAction(HelpEditor)
        self.action_submit.setObjectName(_fromUtf8("action_submit"))
        self.action_download = QtGui.QAction(HelpEditor)
        self.action_download.setObjectName(_fromUtf8("action_download"))
        self.action_register = QtGui.QAction(HelpEditor)
        self.action_register.setObjectName(_fromUtf8("action_register"))
        self.actionUpdate = QtGui.QAction(HelpEditor)
        self.actionUpdate.setObjectName(_fromUtf8("actionUpdate"))
        self.action_preview = QtGui.QAction(HelpEditor)
        self.action_preview.setObjectName(_fromUtf8("action_preview"))
        self.menuFile.addAction(self.action_submit)
        self.menuFile.addAction(self.actionUpdate)
        self.menuFile.addAction(self.action_download)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_preview)
        self.menuRegister.addAction(self.action_register)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRegister.menuAction())

        self.retranslateUi(HelpEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HelpEditor)

    def retranslateUi(self, HelpEditor):
        HelpEditor.setWindowTitle(_translate("HelpEditor", "STDM Help Editor", None))
        self.add_language_cbo.setText(_translate("HelpEditor", "Add", None))
        self.label.setText(_translate("HelpEditor", "Version", None))
        self.label_2.setText(_translate("HelpEditor", "Language", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("HelpEditor", "Contents", None))
        self.image_browse_btn.setText(_translate("HelpEditor", "Upload...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("HelpEditor", "Images", None))
        self.menuFile.setTitle(_translate("HelpEditor", "File", None))
        self.menuRegister.setTitle(_translate("HelpEditor", "Register", None))
        self.action_submit.setText(_translate("HelpEditor", "Submit", None))
        self.action_download.setText(_translate("HelpEditor", "Download", None))
        self.action_register.setText(_translate("HelpEditor", "Register on GitHub", None))
        self.actionUpdate.setText(_translate("HelpEditor", "Update", None))
        self.action_preview.setText(_translate("HelpEditor", "Preview in Browser", None))

from PyQt4 import QtWebKit