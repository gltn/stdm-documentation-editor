from PyQt4.QtGui import QDialog
from ui_add_language import Ui_AddLanguage

class AddLanguage(QDialog, Ui_AddLanguage):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
