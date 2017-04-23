#!C:/Python27/python.exe
import glob
import json
import os
import os
import re
import shutil
from HTMLParser import HTMLParser
from collections import OrderedDict
from os.path import expanduser
from xml.dom import minidom
import json
import sys

from __init__ import (
    IMAGE_TYPES,
    LANGUAGE_DOC,
    IMAGES,
    DOC,
    GALLERY_LIST_JS,
    IMAGE_JS
)

reload(sys)
sys.setdefaultencoding('utf8')


def get_images(lang_doc):
    doc_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(doc_dir, '{}/{}/{}'.format(DOC, lang_doc, IMAGES))
    images = []

    for dir_path, sub_dirs, files in os.walk(image_dir):
        for type in IMAGE_TYPES.values():
            image_paths = glob.glob('{}/{}'.format(dir_path, type))
            image_paths.sort(key=lambda x: os.path.getmtime(x))
            image_paths = reversed(image_paths)
            for image_path in image_paths:
                relative_path = os.path.relpath(image_path, doc_dir)
                relative_path = relative_path.replace('\\', '/').replace(
                    '{}/'.format(DOC), ''
                )

                images.append({"url": relative_path})
    json_data = json.dumps(images)
    with open(IMAGE_JS, 'w+') as outfile:
        print >> outfile, json_data


def get_gallery_images(lang_dir):
    doc_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(doc_dir, '{}/{}/{}'.format(DOC, lang_dir, IMAGES))
    images = []

    for dir_path, sub_dirs, files in os.walk(image_dir):
        for type in IMAGE_TYPES.values():
            image_paths = glob.glob('{}/{}'.format(dir_path, type))
            image_paths.sort(key=lambda x: os.path.getmtime(x))
            image_paths = reversed(image_paths)
            for image_path in image_paths:
                relative_path = os.path.relpath(image_path, doc_dir)
                relative_path = relative_path.replace('\\', '/').replace(
                    '{}/'.format(DOC), ''
                )

                images.append(
                    {"url": relative_path,
                     "name": os.path.basename(image_path)
                    }
                )
    json_data = json.dumps(images)
    with open(GALLERY_LIST_JS, 'w+') as outfile:
        print >> outfile, json_data

# print(json.JSONEncoder().encode(get_images(LANGUAGE_DOC)))


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
    file_name = os.path.basename(str(source_file_path))
    destination = os.path.join(path, file_name)
    if not os.path.isfile(destination):
        destination_file_path = file_name
        shutil.copyfile(source_file_path, destination)
    else:
        destination_file_path = get_next_name(file_name, path)
        shutil.copy(source_file_path, destination_file_path)
    return destination_file_path


def get_next_name(file_name, path):
    base, extension = os.path.splitext(file_name)
    i = 1
    while True:
        new_path = os.path.join(
            path, '{}_{}{}'.format(base, i, extension)
        )

        if not os.path.exists(new_path):
            return new_path
        i += 1
