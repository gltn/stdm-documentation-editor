import os
import re
import shutil
from HTMLParser import HTMLParser
from collections import OrderedDict
from os.path import expanduser
from xml.dom import minidom
import json
import sys

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
LANG_SETTING_FILE = '{}\languages.txt'.format(PLUGIN_DIR)
LANG_FILE = open(LANG_SETTING_FILE, 'r')
LANG_SETTING = LANG_FILE.read()


reload(sys)
sys.setdefaultencoding('utf8')

decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

LANGUAGES = decoder.decode(LANG_SETTING)
LANG_FILE.close()
LANGUAGE = 'en'

IMAGES = 'images'
IMG_PARAM = 'image_path'
IMAGE_TYPES = {'png': '*.png', 'jpg': '*.jpg', 'tif': '*.tif', 'bmp': '*.bmp', 'svg': '*.svg'}
DOC = 'docs'
HELP_EDITOR_HTML = '{}/help.html'.format(DOC)
CURRENT_FILE = '{}/current_file.js'.format(DOC)
IMAGE_BROWSER_HTML = '{}/image_browser.html'.format(DOC)
GALLERY_LIST_JS = '{}/gallery_list.js'.format(DOC)
IMAGE_JS = '{}/images.js'.format(DOC)
DEFAULT_VERSION = '1_5'
LANGUAGE_DOC = '{}/{}'.format(DEFAULT_VERSION, LANGUAGE)
PREVIEW_URL = '{}/{}/index.html'.format(PLUGIN_DIR, DOC)
LANGUAGE_DOC_HTML = '{}/{}/{}'.format(PLUGIN_DIR, DOC, LANGUAGE_DOC)
STDM_VERSIONS = OrderedDict([('1_5', 'STDM 1.5'), ('2_0', 'STDM 2.0'),
                             ('2_1', 'STDM 2.1')
                             ])
TABLE_OF_CONTENT_HTML = 'table_of_contents.html'

TABLE_OF_CONTENT_XML = 'table_of_contents.xml'
HOME = expanduser("~")


def format_html(full_html_text):
    # Read the file and decode html entities
    parser = HTMLParser()
    # Read the file and decode html entities
    xml = parser.unescape(full_html_text)
    try:
        # Pretify the xml
        xml = minidom.parseString(xml.encode('utf-8')).toprettyxml()
    except Exception:
        pass
    xml = re.sub('>\s+<!', '><!', xml)
    xml = re.sub(']>\s+<', ']><', xml)
    # Remove empty lines
    xml = "".join(
        [s for s in xml.strip().splitlines(True) if s.strip()])
    # remove xml version..
    if len(xml.split('<?xml version="1.0" ?>')) > 1:
        xml = xml.split('<?xml version="1.0" ?>')[1]
    return xml


def copy_directory(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)


def copy_file(source_file_path, path):
    destination_file = None
    file = os.path.basename(str(source_file_path))
    destination = os.path.join(path, file)
    if not os.path.isfile(destination):
        destination_file = destination
        shutil.copyfile(source_file_path, destination)
    else:
        base, extension = os.path.splitext(file)
        i = 1
        while True:
            new_name = os.path.join(
                path, '{}_{}{}'.format(base, i, extension)
            )

            if not os.path.exists(new_name):
                destination_file = new_name
                shutil.copy(source_file_path, new_name)
                break
            i += 1
    return destination_file
