"""
A collection of miscellaneous utilities that might be useful.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import re


def remove_filename_whitespace(directory, replace_with="-", preserve_repetitions=True):
    """
    Utility function to remove whitespace from all files in a given directory.

    Libraries such as Caffe, which require that files and labels are inputted using text files containing paths to images, might complain about file names with spaces. This function removes white space from all file names in a given directory.

    :param directory: The directory to scan.
    :param replace_with: The string to replace whitespace with.
    :param preserve_repetitions: If True, multiple instances of consecutive whitespace are each individually replaced with the ``replace_with`` string. For example ``a  file.txt`` is renamed to ``a--file.txt`` if set to True, otherwise the file is renamed to ``a-file.txt``. **Note that if set to False, files may be overwritten and is therefore True by default**.
    :type directory: String
    :type replace_with: String
    :type preserve_repetitions: Boolean
    :returns: A dictionary mapping of file names and their changed values.
    :rtype: Dictionary

    .. note:: This function will not rename folders, nor does it work recursively.
    """

    renamed_files = dict()

    for current_file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, current_file_name)):
            new_file_name = re.sub('\s' if preserve_repetitions is True else '\s+', replace_with, current_file_name)

            if new_file_name != current_file_name:
                if not os.path.exists(os.path.join(directory, new_file_name)):
                    os.rename(os.path.join(directory, current_file_name), os.path.join(directory, new_file_name))
                    renamed_files[current_file_name] = new_file_name

    return renamed_files
