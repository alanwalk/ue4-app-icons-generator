#!/usr/bin/python
# coding=utf-8


"""
Usage:
    ue4-app-icons-generator.py <icon_path> <output_path>
"""


import re
import os
import sys
import json
from docopt import docopt
from PIL import Image


CONFIG_PATH = "config.json"
MATCH_PATTERN = r"(\d+)x(\d+)"
IMAGE_RESAMPLE_MODE = Image.LANCZOS


def resize_and_save_icon(icon_file, save_path, size_str):
    size_group = re.match(MATCH_PATTERN, size_str)
    if size_group:
        w = int(size_group[1])
        h = int(size_group[2])
        new_icon = icon_file.resize((w, h), IMAGE_RESAMPLE_MODE)
        new_icon.save(save_path, 'png')
        print("[OK] %s %dx%d" % (save_path, w, h))
    else:
        print("[FAILED] %s, size format error." % save_path)


def iter_file_list(icon_file, root_path, file_list):
    for filename in file_list:
        value = file_list[filename]
        new_path = os.path.join(root_path, filename)
        if type(value).__name__ == "dict":
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            iter_file_list(icon_file, new_path, value)
        elif type(value).__name__ == "str":
            resize_and_save_icon(icon_file, new_path, value)
        else:
            print("[FAILED] Config parse failed.")
            sys.exit(1)


def iter_config(icon_file, output_path):
    full_config_path = os.path.join(sys.path[0], CONFIG_PATH)
    with open(full_config_path, 'r') as config_file:
        file_list = json.load(config_file)
        iter_file_list(icon_file, output_path, file_list)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    icon_path = arguments["--icon_path"]
    output_path = arguments["--output_path"]

    print("icon path: %s" % icon_path)
    print("output path: %s" % output_path)

    with Image.open(icon_path) as icon_file:
        w, h = icon_file.size
        print('original image size: %sx%s' % (w, h))
        iter_config(icon_file, output_path)
