from __future__ import division

import re
import sys
import os
from HTMLParser import HTMLParser
from PyQt4 import QtWebKit
from uuid import uuid4
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMainWindow
from PyQt4.QtWebKit import QWebSettings, QWebPage
from xml_util import XmlUtil
from images import get_images, get_gallery_images
from ui_help_editor import Ui_HelpEditor
from table_of_contents import TocTreeMenu
from utils import (
    copy_file,
    copy_directory,
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
    HOME,
    format_html,
    STDM_VERSIONS,
    CURRENT_FILE,
    IMAGE_BROWSER_HTML,
    LANG_SETTING,
    PREVIEW_URL,
    TABLE_OF_CONTENT_HTML, LANGUAGE_DOC_HTML)
from ui.add_language import AddLanguage

class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        print '%s line %d: %s' % (source, line, msg)


class HelpEditor(QMainWindow, Ui_HelpEditor):

    window_loaded = pyqtSignal()

    def __init__(self):
        
        # TODO fix image drag drop small size after tree item click
        QMainWindow.__init__(self)
        self.setupUi(self)
        self._curr_file_path = None
        self._curr_title = None
        get_images(LANGUAGE_DOC)
        get_gallery_images(LANGUAGE_DOC)
        self.help_path = os.path.join(PLUGIN_DIR, HELP_EDITOR_HTML)
        self.web_frame = self.content_editor.page().currentFrame()
        self.current_lang_name = 'English'
        self.current_lang_code = 'en'
        # page = WebPage()
        # self.content_editor.setPage(page)
        self.language_doc = LANGUAGE_DOC
        self.current_version = DEFAULT_VERSION
        self.prev_version = None
        self.full_language_dir = os.path.join(
            PLUGIN_DIR, DOC, self.current_version, self.current_lang_code
        )
        self.toc = None
        self.prev_language_code = None
        self.prev_language_name = None
        self.prev_toc_index = None
        self.current_item = None
        self._current_file = None
        self.init_gui()
        self.on_editor_loaded()
        self.on_show_gallery()
        # Start with the first page if current_file.js doesn't exist
        if not os.path.isfile(CURRENT_FILE):
            self.set_current_file('preface.htm')
        else:
            string = open(CURRENT_FILE, 'r').read()
            list_str = string.split('=')
            if len(list_str) > 1:
                json_data = list_str[1].strip().rstrip(';')

                json_data_final = eval(json_data)
                curr_path = json_data_final['current']
                curr_title = json_data_final['title']
                self.set_current_file(os.path.basename(curr_path), curr_title)

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
        self.full_language_dir = os.path.join(
            PLUGIN_DIR, DOC, self.current_version, self.current_lang_code
        )
        self.language_doc = '{}/{}'.format(
            self.current_version, self.current_lang_code
        )
        self.copy_language()
        self.switch_table_of_content(prev_toc_link)

    def switch_table_of_content(self, prev_toc_link):
        if self.toc is not None:
            self.toc.update_contents_path(self.full_language_dir)
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
                # data = data.replace(self.language_doc, '')
                data = re.sub(r"\"/+", '', data)

                full_html = '<html><head><title>{}</title></head>' \
                            '<body>{}</body></html>'.format(self._curr_title, data)
                formatted_html = format_html(full_html)

                html_file = open('{}/{}'.format(DOC, self._curr_file_path), 'w+')
                html_file.write(formatted_html)
                html_file.close()
            # upload image
            else:

                url_data = data.split('{}='.format(IMG_PARAM))

                if len(url_data) > 0:
                    self.save_local_files([url_data[1]])

    def get_item_url(self, item, col=0):

        current_doc = item.data(col, Qt.UserRole).toString()
        current_title = str(item.text(col))
        QApplication.processEvents()
        if self.current_item is not None:
            if self.current_item == item:
                return
        self.set_current_file(current_doc, current_title)
        self.current_item = self.toc.widget_items[str(current_doc)]
        self.load_content_js()

    def set_current_file(self, current_doc, title=None):
        self._curr_file_path = os.path.join(self.language_doc, str(current_doc))

        self._curr_file_path = self._curr_file_path.replace('\\', '/')
        if title is None:
            curr_file_path = os.path.join(PLUGIN_DIR, self._curr_file_path)
            curr_file = open(curr_file_path, 'r')
            html = curr_file.read()
            xml_util = XmlUtil(curr_file_path)
            self._curr_title = xml_util.html_title()
            parser = HTMLParser()
            html_parser = HTMLParser.feed(parser, html)
            if html_parser.handle_endtag('title'):
                self._curr_title = html_parser.handle_data(html)
        else:
            self._curr_title = title
        output_file = open(CURRENT_FILE, 'w+')
        self._current_file = {
            "current": str(self._curr_file_path),
            'doc_path': self.language_doc, 'title': title,
            'full_img_path': '{}/{}'.format(self.full_language_dir, IMAGES),
            'relative_img_path': '{}/{}'.format(self.language_doc, IMAGES),
            'img_param': IMG_PARAM,
            'images_folder': IMAGES
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
        img_name = os.path.basename(destination_file)
        rel_path = '{}/{}/{}'.format(self.language_doc, IMAGES, img_name)
        html = '<img src="{}" alt="{}" style="width:120px;">'.format(
            rel_path.lstrip('\\').lstrip('/'), os.path.basename(rel_path)
        )
        # print rel_path
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
        self.save_local_files(files)

    def save_local_files(self, files):

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
            self.language_cbo.addItem(language, code)

    def on_add_language(self):
        add_language = AddLanguage(self)
        result = add_language.exec_()
        if result:
            lang_name = str(add_language.name.text()).strip()
            lang_code = str(add_language.code.text()).lower().strip()

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
            self.language_cbo.addItem(lang_name, lang_code)

    def on_preview_in_browser(self):
        service = QDesktopServices()

        index_html_path = '{}/index.html'.format(DOC)
        # print open(index_html_path, 'r').closed
        # if not open(index_html_path, 'r').closed:
        #     return
        index_file = open(index_html_path, 'r')
        toc = '{}/{}'.format(LANGUAGE_DOC_HTML, TABLE_OF_CONTENT_HTML)
        toc_file = open(toc, 'r')
        toc_text = toc_file.read()
        toc_file.close()
        index_html_text = index_file.read()

        index_file.close()
        new_toc = '{}{}'.format(
            '<div class="list-group" id="st_side_menu">', toc_text)
        # index_html_text = format_html(index_html_text)
        if new_toc in index_html_text:

            return
        index_html_text = index_html_text.replace(
            '<div class="list-group" id="st_side_menu">', new_toc)
        index_file = open(index_html_path, 'w+')
        print index_html_text
        index_file.write(index_html_text)
        url = QUrl()
        url.setUrl(PREVIEW_URL)
        service.openUrl(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelpEditor()
    window.show()
    sys.exit(app.exec_())