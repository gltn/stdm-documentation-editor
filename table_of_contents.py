import json
import os
import cStringIO
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QHeaderView

from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QTreeWidgetItem

from xml_util import XmlUtil
from __init__ import (
    TABLE_OF_CONTENT_HTML,
    TABLE_OF_CONTENT_XML,
    TABLE_OF_CONTENT_JS)


class TocTreeMenu(QTreeWidget):
    def __init__(self, current_lang_path):
        QTreeWidget.__init__(self)
        self.header().setResizeMode(QHeaderView.Stretch)
        self.setHeaderHidden(True)
        self.curr_language_path = current_lang_path
        self.contents_xml_path = '{}/{}'.format(
            current_lang_path, TABLE_OF_CONTENT_XML
        )

        self.xml_util = XmlUtil(self.contents_xml_path)
        self.contents_data = self.xml_util.xml_point_attributes('toc')

        self.memory_toc_html = cStringIO.StringIO()

        if self.contents_data is None:
            return
        self.parent = None
        self.widget_items = {}
        self.contents_html_path = '{}/{}'.format(
            current_lang_path, TABLE_OF_CONTENT_HTML
        )
        self.contents_js_path = '{}/{}'.format(
            current_lang_path, TABLE_OF_CONTENT_JS
        )
        # self.update_contents_path(self.curr_language_path)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.itemChanged.connect(self.on_item_changed)

    def enable_drag_sort(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionMode(
            QAbstractItemView.SingleSelection
        )
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setDragDropMode(
            QAbstractItemView.InternalMove
        )
    
    def update_contents_path(self, path, update_info):
        self.clear()
        current_version = update_info[0]
        curr_lang_code = update_info[1]
        self.contents_xml_path = '{}/{}'.format(path, TABLE_OF_CONTENT_XML)
        self.xml_util.set_xml_path(self.contents_xml_path)
        self.contents_data = self.xml_util.xml_point_attributes('toc')

        self.contents_html_path = '{}/{}'.format(path, TABLE_OF_CONTENT_HTML)
        self.contents_js_path = '{}/{}'.format(
            path, TABLE_OF_CONTENT_JS
        )
        self.curr_language_path = path

        self.parent = None
        if hasattr(self, 'widget_items'):
            self.widget_items.clear()
            self.blockSignals(True)
            self.save_table_of_contents(self.contents_data)
            self.blockSignals(False)

    def save_table_of_contents(self, contents_data, widgets=True):
        self.create_table_of_contents(contents_data, self, widgets)
        self.create_json_table_of_contents()

    def create_json_table_of_contents(self):

        toc_json = open(self.contents_js_path, 'w')
        json_data = json.dumps(
            [self.memory_toc_html.getvalue()], ensure_ascii=False)
        toc_json.write('var toc_{} = {};'.format(
                os.path.basename(self.curr_language_path),json_data
            )
        )
        toc_json.close()
        self.memory_toc_html.truncate(0)

    def create_table_of_contents(self, contents, root, widgets=True):
        print >> self.memory_toc_html, '<ul>'

        for val in contents:

            for link, name in val.iteritems():
                if isinstance(name, list):
                    if widgets:
                        self.parent = QTreeWidgetItem(root)
                        self.parent.setFlags(
                            Qt.ItemIsEditable | Qt.ItemIsEnabled |
                            Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
                        )
                        self.parent.setData(0, Qt.UserRole, link[0])
                        self.parent.setText(0, link[1])
                        self.widget_items[link[0]] = self.parent
                    print >> self.memory_toc_html, \
                        '<li data-jstree=\'' \
                        '{"icon":"glyphicon glyphicon-folder-close"}\'>' \
                        '<a href="%s">%s</a>' % (link[0], link[1])
                    self.create_table_of_contents(name, self.parent, widgets)
                    print >> self.memory_toc_html, '</li>'

                else:
                    if link != name:
                        print >> self.memory_toc_html, \
                            '<li data-jstree=\'' \
                            '{"icon":"glyphicon glyphicon-file"}\'' \
                            '><a href="%s">%s</a></li>'% (link, name)
                        if widgets:
                            if self.parent is not None:
                                item = QTreeWidgetItem(self.parent)
                            else:
                                item = QTreeWidgetItem(root)
                            item.setFlags(
                                Qt.ItemIsEditable | Qt.ItemIsEnabled |
                                Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
                            )
                            item.setData(0, Qt.UserRole, link)
                            item.setText(0, name)
                            self.widget_items[link] = item
        print >> self.memory_toc_html, '</ul>'

    def on_item_changed(self):
        item = self.currentItem()
        new_title = item.text(0)
        link = item.data(0, Qt.UserRole).toString()
        self.xml_util.change_title(new_title, link)
        contents_data = self.xml_util.xml_point_attributes('toc')
        self.blockSignals(True)
        self.save_table_of_contents(contents_data, False)
        self.blockSignals(False)
#
# if __name__ == '__main__':
#
#     import sys
#     app = QApplication(sys.argv)
#     full_language_dir = os.path.join(
#         PLUGIN_DIR, DOC, DEFAULT_VERSION, LANGUAGE
#     )
#     window = TocTreeMenu(full_language_dir)
#     # window.create_json_table_of_contents()
#     window.resize(400, 300)
#     window.show()
#     sys.exit(app.exec_())

