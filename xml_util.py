from collections import OrderedDict
from PyQt4.QtCore import QFile
from PyQt4.QtGui import QApplication
from PyQt4.QtXml import QDomDocument
TAG_NAME = 'item'
KEY = 'link'
CHANGING_KEY = 'name'
class XmlUtil():

    def __init__(self, xml_path):
        """
        A utility class to read xml file contents.
        :param xml_path: The GPX file path
        :type xml_path: String
        """
        self.xml_path = xml_path
        self.xml_node_name = 'toc'
        self.xml_element = None
        self.read_xml_file(self.xml_path)

    def set_xml_path(self, path):
        self.xml_path = path
        self.read_xml_file(path)


    def write_to_xml(self):
        xml_file = open(self.xml_path, 'w+')
        xml_file.write(self.document.toString())
        xml_file.close()

    def read_xml_file(self, xml_path):
        """
        Reads the xml file contents and creates QDomDocument version of it.
        """
        xml_file_path = QFile(xml_path)
        self.document = QDomDocument()
        status, msg, line, col = self.document.setContent(xml_file_path)
        if status:
            self.xml_element = self.document.documentElement()

    def find_tree_item(self, value, keyword_key=KEY):
        """
        Find elements by value.
        :param value: The key word to be used for searching
        :type value: String
        :return: A found element
        :rtype: QDomElement
        """
        nodes = self.find_xml_node(TAG_NAME)
        elements = []
        for node in nodes:
            element = node.toElement()
            if value == element.attribute(keyword_key):
                elements.append(element)
        return elements

    def change_title(
            self, changing_val, keyword_val,
            changing_key=CHANGING_KEY, keyword_key=KEY):
        elements = self.find_tree_item(keyword_val, keyword_key)
        for element in elements:
            element.setAttribute(changing_key, changing_val)

        self.write_to_xml()

    def find_xml_node(self, name):
        """
        Get nodes inside a document by a tag name.
        :param name: The tag name
        :type name: String
        :return: The nodes list
        :rtype: List
        """
        node_list = self.document.elementsByTagName(name)
        nodes = []
        for i in range(node_list.length()):
            node = node_list.item(i)
            nodes.append(node)
        return nodes

    def html_title(self):
        nodes = self.find_xml_node('title')
        title_element = nodes[0].toElement()
        return title_element.text()

    def xml_point_attributes(self, xml_feature_name):
        node_list = self.find_xml_node(xml_feature_name)

        QApplication.processEvents()
        attribute = []
        for j, nod in enumerate(node_list):

            child = nod.childNodes()

            attribute = self.extract_data(child)
            if attribute == []:
                continue

        return attribute

    def extract_data(self, child):
        if isinstance(child, str):
            return
        if child.length() < 1:
            return
        data = []
        for i in range(child.length()):
            attribute = OrderedDict()
            node = child.item(i)
            parent_attribute = self.extract_data(node.childNodes())
            if parent_attribute is not None:
                parent_link = str(node.toElement().attribute('link'))
                parent_name = str(node.toElement().attribute('name'))
                attribute[(parent_link, parent_name)] = parent_attribute
            else:
                link = str(node.toElement().attribute('link'))
                name = str(node.toElement().attribute('name'))
                attribute[link] = name
            data.append(attribute)
        return data
