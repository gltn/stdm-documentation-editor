import os

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox

from settings import LANGUAGES, PLUGIN_DIR, DOC, LANG_SETTING_FILE
from ui_add_language import Ui_AddLanguage


class AddLanguage(QDialog, Ui_AddLanguage):
    def __init__(self, version, parent):
        QDialog.__init__(self, parent)
        self._curr_version = version
        self._help_editor = parent
        self.setupUi(self)
        self.populate_languages()

    def populate_languages(self):
        self.select_language_cbo.addItem('', None)
        for code, language in LANGUAGES.iteritems():
            doc_dir = os.path.join(PLUGIN_DIR, DOC, self._curr_version, code)
            if not os.path.isdir(doc_dir):
                self.select_language_cbo.addItem(language, code)

    def on_add_language(self):
        self.toolBox.currentIndex()
        status = False
        lang_name = str(self.name.text()).strip()
        lang_code = str(self.code.text()).lower().strip()
        if lang_name != '' and lang_code != '' and self.toolBox.currentIndex() == 1:
            self.set_language(lang_name, lang_code)
            self._help_editor.language_cbo.addItem(lang_name, lang_code)
            status = True
        elif str(self.select_language_cbo.currentText()) != '' and \
            self.toolBox.currentIndex() == 0:
            curr_index = self.select_language_cbo.currentIndex()
            lang_code = str(
                self.select_language_cbo.itemData(curr_index).toString())
            lang_name = str(self.select_language_cbo.currentText())
            self.set_language(lang_name, lang_code)
            self._help_editor.language_cbo.addItem(lang_name, lang_code)
            status = True
        return status


    def set_language(self, lang_name, lang_code):
        new_lag_entry = '"{}": "{}"'.format(lang_code, lang_name)
        lang_file = open(LANG_SETTING_FILE, 'r')
        lang_list = lang_file.read()
        index = lang_list.find('}')
        updated_lang_list = '{}, {}{}'.format(
            lang_list[:index], new_lag_entry, lang_list[index:]
        )
        lang_file.close()
        lang_file = open(LANG_SETTING_FILE, 'w+')
        lang_file.write(updated_lang_list)
        lang_file.close()

    def accept(self):
        status = self.on_add_language()
        title = QApplication.translate('AddLanguage', 'Add Language')

        if status:
            message = QApplication.translate(
                'AddLanguage',
                'You have successfully added a new language.\n'
                'To start adding a content, select the language '
                'in the main window.'
            )
            QMessageBox.information(self._help_editor, title, message)
            self.close()
        else:
            message = QApplication.translate(
                'AddLanguage',
                'You have not selected a language. \n'
                'Please choose or add a language with its code.'
            )
            QMessageBox.information(self._help_editor, title, message)
            # self.accept()
