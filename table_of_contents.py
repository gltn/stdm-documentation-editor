import os

import time

import cStringIO
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QHeaderView

from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QTreeWidgetItem

from xml_util import XmlUtil
from utils import (
TABLE_OF_CONTENT_HTML,
TABLE_OF_CONTENT_XML
)


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
        self.save_table_of_contents(self.contents_data)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.itemChanged.connect(self.on_item_changed)
        self.enable_drag_sort()
    
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
    
    def update_contents_path(self, path):
        self.clear()
        self.contents_xml_path = '{}/{}'.format(path, TABLE_OF_CONTENT_XML)
        self.xml_util.set_xml_path(self.contents_xml_path)
        self.contents_data = self.xml_util.xml_point_attributes('toc')
        self.contents_html_path = '{}/{}'.format(path, TABLE_OF_CONTENT_HTML)
        self.parent = None
        if os.path.isfile(self.contents_html_path):
            self.widget_items.clear()
            self.blockSignals(True)
            self.save_table_of_contents(self.contents_data)
            self.blockSignals(False)


    def save_table_of_contents(self, contents_data, widgets=True):
        self.create_table_of_contents(contents_data, self, widgets)
        toc_html = open(self.contents_html_path, 'w+')
        toc_html.write(self.memory_toc_html.getvalue())
        toc_html.close()
        self.memory_toc_html.truncate()

    def create_table_of_contents(self, contents, root, widgets=True):
        print >> self.memory_toc_html, '<ul>'
        for val in contents:
            # print val
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
                        self.widget_items[str(link[0])] = self.parent
                    print >> self.memory_toc_html, '<li><a href="{}">{}</a>'.format(
                        link[0], link[1]
                    )
                    self.create_table_of_contents(name, self.parent, widgets)
                    print >> self.memory_toc_html, '</li>'

                else:
                    if link != name:
                        print >> self.memory_toc_html, \
                            '<li><a href="{}">{}</a></li>'.format(link, name)
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
                            self.widget_items[str(link)] = item
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
#     window = TocTreeMenu()
#     window.resize(400, 300)
#     window.show()
#     sys.exit(app.exec_())

