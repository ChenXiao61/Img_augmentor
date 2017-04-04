from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import glob


class AugmentorImage(object):
    def __init__(self, image_path, output_directory):
        # Just to stop Pylint complaining about initialising these outside
        # of __init__ which is not actually happening, as the are being
        # initialised in the setters, but anyway.
        self._ground_truth = None
        self._image_path = None
        self._output_directory = None
        self._file_format = None  # TODO: pass this for each image.

        # Now we call the setters that we require.
        self.image_path = image_path
        self.output_directory = output_directory

    @property
    def output_directory(self):
        return self._output_directory

    @output_directory.setter
    def output_directory(self, value):
        self._output_directory = value

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, value):
        if os.path.exists(value):
            self._image_path = value
        else:
            raise IOError("The file specified does not exist.")

    @property
    def image_file_name(self):
        return os.path.basename(self.image_path)

    @property
    def ground_truth(self):
        return self._ground_truth

    @ground_truth.setter
    def ground_truth(self, value):
        if os.path.isfile(value):
            self._ground_truth = value


def extract_paths_and_extensions(image_path):
    file_name, extension = os.path.splitext(image_path)
    root_path = os.path.dirname(image_path)

    return file_name, extension, root_path


def scan_directory(source_directory):
    file_types = ['*.jpg', '*.bmp', '*.jpeg', '*.gif', '*.img', '*.png']

    # Also include the uppercase versions of the file extensions.
    # TODO: We might need to catch .Jpeg and .Png perhaps?
    file_types.extend([str.upper(str(x)) for x in file_types])

    list_of_files = []

    for file_type in file_types:
        list_of_files.extend(glob.glob(os.path.join(os.path.abspath(source_directory), file_type)))

    return list_of_files
