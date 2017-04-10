#!C:/Python27/python.exe
import glob
import json
import os
from utils import (
    IMAGE_TYPES,
    LANGUAGE_DOC,
    IMAGES,
    DOC,
    GALLERY_LIST_JS,
    IMAGE_JS
)


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
