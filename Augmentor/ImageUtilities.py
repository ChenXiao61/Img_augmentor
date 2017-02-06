from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import glob


class AugmentorImage(object):
    def __init__(self, image_path):
        self.image_path = image_path


def extract_paths_and_extensions(image_path):
    file_name, extension = os.path.splitext(image_path)
    root_path = os.path.dirname(image_path)

    return file_name, extension, root_path


def scan_directory(source_directory, recursive_scan=False):
    file_types = ['*.jpg', '*.bmp', '*.jpeg', '*.gif', '*.img', '*.png']
    file_types.extend([str.upper(x) for x in file_types])

    list_of_files = []

    for file_type in file_types:
        list_of_files.extend(glob.glob(os.path.join(os.path.abspath(source_directory), file_type)))

    return list_of_files
