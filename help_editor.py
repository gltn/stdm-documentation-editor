import glob
import json
import os
import re
import shutil
import sys
import zipfile
from HTMLParser import HTMLParser
from collections import OrderedDict

try: import simplejson as simplejson
except ImportError:import json as simplejson

from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QProgressDialog
from PyQt4.QtWebKit import QWebSettings, QWebPage

from utils import get_images, get_gallery_images, get_next_name
from table_of_contents import TocTreeMenu
from ui.add_language import AddLanguage
from ui.ui_help_editor import Ui_HelpEditor

from utils import (
    copy_file,
    copy_directory,
    format_html
)
from settings import (
    IMAGE_TYPES,
    PLUGIN_DIR,
    HELP_EDITOR_HTML,
    LANGUAGES,
    DOC,
    DEFAULT_VERSION,
    IMAGES,
    IMG_PARAM,
    LANGUAGE_DOC,
    LANG_SETTING_FILE,
    TABLE_OF_CONTENT_JS,
    HOME,
    STDM_VERSIONS,
    CURRENT_FILE,
    IMAGE_BROWSER_HTML,
    PREVIEW_URL,
    LIST_OF_JS_DOCS,
    LANGUAGES_WITH_CONTENT, SEARCH_DATA_JS, TABLE_OF_CONTENT_HTML)

class HelpEditor(QMainWindow, Ui_HelpEditor):
    window_loaded = pyqtSignal()
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self._curr_file_path = None
        self._curr_file_path_js = None
        self._curr_title = None
        self.current_item = None
        get_images(LANGUAGE_DOC)
        get_gallery_images(LANGUAGE_DOC)
        self.help_path = os.path.join(PLUGIN_DIR, HELP_EDITOR_HTML)
        self.web_frame = self.content_editor.page().currentFrame()
        self.on_editor_loaded()
        self.current_lang_name = 'English'
        self.current_lang_code = 'en'
        self.language_doc = LANGUAGE_DOC
        self.current_version = DEFAULT_VERSION
        self.prev_version = None
        self.full_language_dir = os.path.join(
            PLUGIN_DIR, DOC, self.current_version, self.current_lang_code
        )
        self.toc = None
        self.prev_language_code = None
        self.prev_language_name = None
        self._prev_file_path = None
        self.current_document = None
        self._current_file = None
        self.added_languages = OrderedDict()
        self.start_page = 'preface.htm'

        if not os.path.isdir(self.full_language_dir):
            self.full_language_dir = os.path.join(
                    PLUGIN_DIR, DOC)
            self.start_page = 'help.htm'

        self.init_gui()

        self.on_show_gallery()
        self.content_editor.dropEvent = self.on_help_editor_item_drop
        # Start with the first page if current_file.js doesn't exist

        if not os.path.isfile(CURRENT_FILE) or self._current_file is None:
            if bool(self.toc.widget_items):
                self.switch_table_of_content(self.start_page)
                self.current_item = self.toc.widget_items[self.start_page]
                title = str(self.current_item.text(0))
                self.set_current_file(self.start_page, title)
                self.toc.setCurrentItem(self.current_item)
        else:
            self.read_current_file()
            self.toc.expandItem(self.current_item.parent())
            self.toc.setCurrentItem(self.current_item)
            self.setWindowTitle(
                'STDM Documentation Editor - {}'.format(self._curr_title)
            )

    def read_current_file(self):
        string = open(CURRENT_FILE, 'r').read()
        list_str = string.split('=')
        if len(list_str) > 1:
            json_data = list_str[1].strip().rstrip(';')
            json_data_final = eval(json_data)
            self._curr_file_path = json_data_final['current']
            self._curr_file_path_js = json_data_final['current_js']
            self._curr_title = json_data_final['title']
            self.language_doc = json_data_final['doc_path']
            self.current_item = self.toc.widget_items[
                os.path.basename(self._curr_file_path)
            ]

    def on_help_editor_item_drop(self, event):
        html = str(event.mimeData().html())
        image_name = str(event.mimeData().text())
        correct_src = 'src="{}/{}/{}"'.format(
            self.language_doc, IMAGES, image_name
        )
        # remove absolute url
        fixed_html = re.sub(r"src=\"\S+", correct_src, html)
        # remove style
        fixed_html = re.sub(r'style\S+\"', '', fixed_html)
        js = """
              jQuery(document).ready(function() {
                  jQuery(document).trigger('customDropEvent', '%s');
              });
        """ % fixed_html
        QApplication.processEvents()
        self.web_frame.evaluateJavaScript(QString(js))

    def init_gui(self):
        self.statusbar.hide()
        # enable developer options
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled, True
        )
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.LocalStorageEnabled, True
        )
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.JavascriptCanAccessClipboard, True
        )

        self.init_table_of_contents()
        # remove margins
        self.centralWidget().layout().setContentsMargins(0,0,0,0)
        self.content_editor.urlChanged.connect(self.on_url_changed)
        self.add_language_cbo.clicked.connect(self.on_add_language)
        self.image_browse_btn.clicked.connect(self.file_dialog)
        self.window_loaded.connect(self.on_widow_loaded)
        
        self.action_preview.triggered.connect(self.on_preview_in_browser)
        self.action_export_zip.triggered.connect(self.export_doc_to_zip)
        self.action_download.triggered.connect(self.on_download_repo)

        
        self.populate_languages()
        self.populate_stdm_version()

    def init_table_of_contents(self):
        self.toc = TocTreeMenu(self.full_language_dir)
        self.toc_container.addWidget(self.toc)
        self.toc.itemClicked.connect(self.get_item_url)
        self.toc.setStyleSheet("QTreeWidget { border:1px solid #ddd; }")
        self.toc.rootIsDecorated()
        self.toc.alternatingRowColors()

    def populate_stdm_version(self):
        for dir_name, ver in STDM_VERSIONS.iteritems():
            self.stdm_version_cbo.addItem(ver, dir_name)
        self.window_loaded.emit()

    def on_widow_loaded(self):
        self.language_cbo.currentIndexChanged.connect(
            self.on_language_switched
        )
        self.stdm_version_cbo.currentIndexChanged.connect(
            self.on_version_switched
        )
        # self.toc.itemClicked

    def on_version_switched(self, index):
        self.prev_version = self.current_version
        prev_toc_link = str(self.current_item.data(
            0, Qt.UserRole).toString()
                            )
        self.current_version = str(
            self.stdm_version_cbo.itemData(index).toString()
        )
        self.full_language_dir = os.path.join(
            PLUGIN_DIR, DOC, self.current_version, self.current_lang_code
        )
        self.language_doc = '{}/{}'.format(
            self.current_version, self.current_lang_code
        )
        self.copy_version()
        self.switch_table_of_content(prev_toc_link)

    def on_language_switched(self, index, version_switch=False):
        self.prev_language_code = self.current_lang_code
        self.prev_language_name = self.current_lang_name
        prev_toc_link = str(self.current_item.data(
            0, Qt.UserRole).toString()
        )

        self.current_lang_code = str(
            self.language_cbo.itemData(index).toString()
        )
        self.current_lang_name = str(self.language_cbo.currentText())
        if self.current_lang_code not in self.added_languages.keys():
            self.added_languages[self.current_lang_code] = \
                self.current_lang_name
        self.full_language_dir = os.path.join(
            PLUGIN_DIR, DOC, self.current_version, self.current_lang_code
        )
        self.language_doc = '{}/{}'.format(
            self.current_version, self.current_lang_code
        )
        self.copy_language()
        self.switch_table_of_content(prev_toc_link)
        self.create_added_languages_js()

    def switch_table_of_content(self, prev_toc_link):
        if self.toc is not None:
            updated_info = [self.current_version, self.current_lang_code]
            self.toc.update_contents_path(
                self.full_language_dir, updated_info
            )

            current_widget_item = self.toc.widget_items[prev_toc_link]
            self.toc.setCurrentItem(current_widget_item)
            current_title = str(current_widget_item.text(0))
            self.set_current_file(prev_toc_link, current_title)
            self.get_item_url(current_widget_item)

    def copy_language(self):
        prev_language_dir = os.path.join(
            PLUGIN_DIR, DOC, self.current_version, self.prev_language_code
        )
        if not os.path.isdir(self.full_language_dir):
            copy_directory(prev_language_dir, self.full_language_dir)

    def copy_version(self):
        prev_doc_dir = os.path.join(
            PLUGIN_DIR, DOC, self.prev_version, self.current_lang_code
        )
        if not os.path.isdir(self.full_language_dir):
            copy_directory(prev_doc_dir, self.full_language_dir)

    def on_url_changed(self, url):
        if url.hasFragment():
            data = str(url.fragment())
            # handle saving.
            if not data.startswith(IMG_PARAM):
                self.save_html_js_doc(data)
            # upload image
            else:
                url_data = data.split('{} = '.format(IMG_PARAM))
                if len(url_data) > 0:
                    self.save_local_images([url_data[1]])

    def save_html_js_doc(self, data):
        data = re.sub(r"\"/+", '', data)
        full_html = '<html><head><title>{}</title></head>' \
                    '<body>{}</body></html>'.format(
            self._curr_title, data
        )
        formatted_html = format_html(full_html)
        html_file = open(
            '{}/{}'.format(DOC, self._curr_file_path), 'w')
        html_file.write(formatted_html)
        html_file.close()
        json_data = json.dumps([formatted_html], ensure_ascii=False)
        path = '{}/{}'.format(DOC, self._curr_file_path_js)
        file_name = os.path.basename(self._curr_file_path_js).split('.')[0]
        self.write_js_doc(file_name, json_data, path)

    def get_html_content(self, content, tag):
        pattern = re.compile(r'<'+tag+'.*?>(.+?)</'+tag+'>')
        return re.findall(pattern, content)

    def export_doc_to_zip(self):
        path = self.folder_dialog()
        progress = self.create_js_doc()
        progress.open()
        zip_file_path = '{}/stdm_docs.zip'.format(path)
        if os.path.isfile(zip_file_path):
            zip_file_path = get_next_name('stdm_docs.zip', path)

        zip_file = zipfile.ZipFile(zip_file_path, 'w')
        for dir_name, sub_dirs, files in os.walk(DOC):
            progress.setRange(0, len(files) - 1)
            if dir_name.startswith(os.path.join(DOC, 'js')):
                continue
            else:
                zip_file.write(dir_name)
            for i, filename in enumerate(files):
                progress.setValue(i)
                if dir_name == DOC:
                    if filename == 'index.html' or \
                                    filename == 'current_file.js':
                        zip_file.write(os.path.join(dir_name, filename))
                else:
                    zip_file.write(os.path.join(dir_name, filename))

        zip_file.close()
        progress.close()
        title = QApplication.translate('HelpEditor', 'Add Language')
        message = QApplication.translate(
            'HelpEditor',
            'You have successfully exported the documentation.\n'
            'To access the contents, extract the zip file starting '
            'with stdm_docs and open the index.html file in the docs folder. '
        )
        QMessageBox.information(self, title, message)

    def create_js_doc(self):
        progress = self.init_progress_dialog()
        for lang_code in self.added_languages.keys():
            doc_path = os.path.join(
                PLUGIN_DIR, DOC, self.current_version, lang_code
            )
            js_files = []
            search_cont = []

            for dir_path, sub_dirs, files in os.walk(doc_path):
                if os.path.basename(dir_path) == 'images':
                    continue

                html_files = glob.glob('{}/*{}'.format(dir_path, '.html'))
                html_files.extend(glob.glob('{}/*{}'.format(dir_path, '.htm')))
                progress.setRange(0, len(html_files) - 1)
                for i, html_file_path in enumerate(html_files):
                    if TABLE_OF_CONTENT_HTML in html_file_path:
                        continue
                    if os.path.basename(html_file_path) == '.':
                        continue
                    data, json_data = self.html_to_json(html_file_path)
                    file_name = os.path.basename(html_file_path).split('.')[0]
                    path = '{}/{}.js'.format(doc_path, file_name)

                    relative_path = '{}/{}/{}.js'.format(
                        self.current_version, lang_code, file_name)
                    js_files.append(relative_path)
                    self.write_js_doc(file_name, json_data, path)
                    search_cont = self.prepare_search(
                        data, file_name, search_cont
                    )
                    progress.setValue(i)

            self.create_file_js_list(doc_path, js_files)
            self.create_search_js(doc_path, search_cont)
        progress.hide()
        return progress

    def init_progress_dialog(self):
        progress = QProgressDialog(self)
        title = QApplication.translate('HelpEditor', 'Generating...')
        progress.setWindowTitle(title)
        progress.setMinimumHeight(70)
        progress.setValue(0)
        progress.open()
        return progress

    def create_search_js(self, doc_path, search_cont):
        js_search_cont = open('{}/{}'.format(
            doc_path, SEARCH_DATA_JS
        ), 'w')
        js_search_cont.write('var tipuesearch = {"pages": %s };'
                             % search_cont)
        js_search_cont.close()

    def create_file_js_list(self, doc_path, js_files):
        js_doc_cont = open('{}/{}'.format(
            doc_path, LIST_OF_JS_DOCS
        ), 'w')
        js_doc_cont.write('var js_doc_files = {};'.format(js_files))
        js_doc_cont.close()

    def html_to_json(self, html_file_path):
        html_file = open(html_file_path, 'r')
        data = html_file.read()
        json_data = json.dumps([data], ensure_ascii=False)
        html_file.close()
        return data, json_data

    def prepare_search(self, data, file_name, search_cont):
        searchable_data = {}
        title = self.get_html_content(data, 'title')
        if len(title) > 0:
            searchable_data['title'] = title[0]
            searchable_data['tags'] = title[0]
        else:
            searchable_data['title'] = ''
            searchable_data['tags'] = ''
        searchable_data['text'] = re.sub(r'title\S+\"', '', data)
        searchable_data['url'] = '#{}'.format(file_name)

        search_cont.append(searchable_data)
        return search_cont

    def write_js_doc(self, file_name, json_data, path):
        js_file = open(path, 'w')
        variable_name = file_name.replace('-', '_')
        js_file.write('var {} = {};'.format(variable_name, json_data))
        js_file.close()

    def get_item_url(self, item, col=0):
        self._prev_file_path = self._curr_file_path
        current_doc = item.data(col, Qt.UserRole).toString()
        current_title = str(item.text(col))
        QApplication.processEvents()
        if self.current_item is not None:
            if self.current_item == item:
                return
        self.set_current_file(current_doc, current_title)
        self.current_item = self.toc.widget_items[str(current_doc)]
        self.setWindowTitle(
            'STDM Documentation Editor - {}'.format(self._curr_title)
        )
        self.content_editor.blockSignals(True)
        self.load_content_js()
        self.content_editor.blockSignals(False)

    def set_current_file(self, current_doc, title=None):

        self._curr_file_path = os.path.join(self.language_doc, str(current_doc))
        self._curr_file_path = self._curr_file_path.replace('\\', '/')
        self._curr_title = title
        file_name = os.path.basename(self._curr_file_path).split('.')[0]
        self._curr_file_path_js = '{}/{}.js'.format(self.language_doc,
                                                    file_name)
        output_file = open(CURRENT_FILE, 'w')

        self._current_file = {
            "current": str(self._curr_file_path),
            'current_js_path': self._curr_file_path_js,
            'language': self.current_lang_code,
            'current_name': file_name.replace('-', '_'),
            'doc_path': self.language_doc, 'title': title,
            'full_img_path': '{}/{}'.format(self.full_language_dir, IMAGES),
            'relative_img_path': '{}/{}'.format(self.language_doc, IMAGES),
            'img_param': IMG_PARAM,
            'images_folder': IMAGES,
            'search_data': '{}/{}'.format(self.language_doc, SEARCH_DATA_JS)
        }
        output_file.write('var html_file = {};'.format(self._current_file))
        output_file.close()

    def load_content_js(self):

        js = """
            jQuery(document).ready(function() {
                jQuery(document).trigger('customChangeEvent', %s);
            });
        """ % self._current_file
        QApplication.processEvents()
        self.web_frame.evaluateJavaScript(QString(js))

    def load_image(self, destination_file):

        rel_path = '{}/{}/{}'.format(
            self.language_doc, IMAGES, destination_file
        )
        html = '<img src="{}" alt="{}" style="width:120px;">'.format(
            rel_path.lstrip('\\').lstrip('/'), os.path.basename(rel_path)
        )
        self.image_browser.page().mainFrame().documentElement().\
            findFirst("ul").prependInside(html)

    def on_editor_loaded(self):

        help_url = QUrl()

        help_url.setPath(self.help_path)
        self.content_editor.load(help_url)

    def on_show_gallery(self):
        help_url = QUrl()
        help_path = os.path.join(PLUGIN_DIR, IMAGE_BROWSER_HTML)
        help_url.setPath(help_path)
        self.image_browser.load(help_url)

    def file_dialog(self):
        """
        Displays a file dialog for a user to select an image.
        """
        dialog_title = QApplication.translate(
            "HelpEditor",
            "Select an Image"
        )
        files = QFileDialog.getOpenFileNames(
            self,
            dialog_title,
            HOME,
            "Images ({})".format(' '.join(IMAGE_TYPES.values()))
        )
        return files

    def folder_dialog(self):
        """
        Displays a file dialog to choose the destination folder of the zip.
        :param line_edit: The line edit in which the folder is going to be set.
        :type line_edit: QLineEdit
        """
        title = QApplication.translate(
            "HelpEditor",
            "Select a Folder to Save the Zip"
        )
        last_path = HOME
        path = QFileDialog.getExistingDirectory(
            self,
            title,
            last_path,
            QFileDialog.ShowDirsOnly
        )
        return str(path)

    def save_local_images(self, files=None):
        if files is None:
            files = self.file_dialog()
        path = os.path.join(PLUGIN_DIR, DOC, self.language_doc, IMAGES)
        destination_files = []
        for file_path in files:
            destination_file = copy_file(file_path, path)
            destination_files.append(destination_file)
        get_images(self.language_doc)
        get_gallery_images(self.language_doc)
        for destination_file in destination_files:
            self.load_image(destination_file)

    def populate_languages(self):
        for code, language in LANGUAGES.iteritems():
            doc_dir = os.path.join(PLUGIN_DIR, DOC, self.current_version, code)
            if os.path.isdir(doc_dir):
                self.language_cbo.addItem(language, code)
                self.added_languages[str(code)] =str(language)
        self.create_added_languages_js()

    def create_added_languages_js(self):
        path = '{}/{}/{}'.format(PLUGIN_DIR, DOC, LANGUAGES_WITH_CONTENT)
        js_file = open(path, 'w')
        ordered_json = self.to_ordered_json(self.added_languages)
        js_file.write('var added_languages = {};'.format(ordered_json))
        js_file.close()

    def to_ordered_json(self, ordered_dic):
        encoder = OrderedJsonEncoder()
        ordered_json = encoder.encode(ordered_dic)
        return ordered_json

    def on_add_language(self):
        add_language = AddLanguage(self.current_version, self)
        add_language.exec_()

    def on_preview_in_browser(self):
        service = QDesktopServices()
        self.create_js_doc()
        url = QUrl.fromLocalFile(PREVIEW_URL)
        service.openUrl(url)
    
    def on_download_repo(self):
        from git_editor import CloneEditor
        editor = CloneEditor(self)
        editor.exec_()

class OrderedJsonEncoder( simplejson.JSONEncoder ):
   def encode(self, data):
      if isinstance(data, OrderedDict):
         return "{" + ",".join(
             [self.encode(k)+":"+self.encode(v) for (k,v) in data.iteritems()]
         ) + "}"
      else:
         return simplejson.JSONEncoder.encode(self, data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelpEditor()
    window.show()
    sys.exit(app.exec_())
