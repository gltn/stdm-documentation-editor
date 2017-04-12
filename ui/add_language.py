import os

from PyQt4.QtGui import QDialog

from settings import LANGUAGES, PLUGIN_DIR, DOC
from ui_add_language import Ui_AddLanguage


class AddLanguage(QDialog, Ui_AddLanguage):
    def __init__(self, version, parent):
        QDialog.__init__(self, parent)
        self._curr_version = version
        self.setupUi(self)
        self.populate_languages()

    def populate_languages(self):
        for code, language in LANGUAGES.iteritems():
            doc_dir = os.path.join(PLUGIN_DIR, DOC, self._curr_version, code)
            if not os.path.isdir(doc_dir):
                self.select_language_cbo.addItem(language, code)
