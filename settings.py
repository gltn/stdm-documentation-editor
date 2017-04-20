import os

from collections import OrderedDict
from os.path import expanduser
import json

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
LANG_SETTING_FILE = '{}\languages.txt'.format(PLUGIN_DIR)
LANG_FILE = open(LANG_SETTING_FILE, 'r')
LANG_SETTING = LANG_FILE.read()

decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

LANGUAGES = decoder.decode(LANG_SETTING)
LANG_FILE.close()
LANGUAGE = 'en'

IMAGES = 'images'
IMG_PARAM = 'image_path'
IMAGE_TYPES = {
    'png': '*.png', 'jpg': '*.jpg', 'tif': '*.tif',
    'bmp': '*.bmp', 'svg': '*.svg'
}
DOC = 'docs'
HELP_EDITOR_HTML = '{}/help.html'.format(DOC)
CURRENT_FILE = '{}/current_file.js'.format(DOC)
IMAGE_BROWSER_HTML = '{}/image_browser.html'.format(DOC)
GALLERY_LIST_JS = '{}/gallery_list.js'.format(DOC)
IMAGE_JS = '{}/images.js'.format(DOC)
DEFAULT_VERSION = '1_5'
HTML_EXTENSION = '.htm'
LANGUAGE_DOC = '{}/{}'.format(DEFAULT_VERSION, LANGUAGE)
PREVIEW_URL = '{}/{}/index.html'.format(PLUGIN_DIR, DOC)
LANGUAGE_DOC_HTML = '{}/{}/{}'.format(PLUGIN_DIR, DOC, LANGUAGE_DOC)
STDM_VERSIONS = OrderedDict([('1_5', 'STDM 1.5')
                             ])
LIST_OF_JS_DOCS = 'docs_js_list.js'
TABLE_OF_CONTENT_HTML = 'table_of_contents.html'
TABLE_OF_CONTENT_JS = 'table_of_contents.js'
SEARCH_DATA_JS = 'search_data.js'
TABLE_OF_CONTENT_XML = 'table_of_contents.xml'
HOME = expanduser("~")
LANGUAGES_WITH_CONTENT = 'languages_with_content.js'