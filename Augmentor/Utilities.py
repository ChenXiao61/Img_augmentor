"""
A collection of miscellaneous utilities that might be useful.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import re
import collections


def remove_filename_whitespace(directory, replace_with="-", preserve_repetitions=True):
    """
    Utility function to remove whitespace from all files in a given directory.

    Libraries such as Caffe, which require that files and labels are inputted using text files containing paths to \
    images, might complain about file names with spaces. This function removes white space from all file names in \
    a given directory.

    :param directory: The directory to scan.
    :param replace_with: The string to replace whitespace with.
    :param preserve_repetitions: If True, multiple instances of consecutive whitespace are each individually \
    replaced with the ``replace_with`` string. For example ``a  file.txt`` is renamed to ``a--file.txt`` if \
    set to True, otherwise the file is renamed to ``a-file.txt``. **Note that if set to False, files may be \
    overwritten and is therefore True by default**.
    :type directory: String
    :type replace_with: String
    :type preserve_repetitions: Boolean
    :return: A dictionary mapping of file names and their changed values.
    :rtype: Dictionary

    .. note:: This function will not rename folders, nor does it work recursively.
    """
    # TODO: Check to see if an absolute path might break this, if so then we can find the absolute path first
    renamed_files = dict()

    for current_file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, current_file_name)):
            new_file_name = re.sub('\s' if preserve_repetitions is True else '\s+', replace_with, current_file_name)

            if new_file_name != current_file_name:
                if not os.path.exists(os.path.join(directory, new_file_name)):
                    os.rename(os.path.join(directory, current_file_name), os.path.join(directory, new_file_name))
                    renamed_files[current_file_name] = new_file_name

    return renamed_files


def summarise(directory):
    """
    Utility function that summarises the contents of a directory, such as number of images, file types, dimensions, etc.

    .. note:: This function does not work recursively.
    :param directory: The directory to summarise, either relative or absolute.
    :type directory: String
    :return: An object containing information about the contents of ```directory```.
    :rtype: Summary object with thw following fields: ```number_of_filetypes``` (the number of unique filetypes \
    encountered), ```number_of_images``` (the total number of files encountered), and ```file_types``` \
    (a ```List``` of filetypes encountered)
    """
    # TODO: Fix this so that we only look at images, from those readable by Pillow
    Summary = collections.namedtuple('Summary', 'number_of_filetypes, number_of_images, file_types')
    path = os.path.abspath(directory)
    list_of_files = os.listdir(path)

    # Count the file types
    extensions = set()  # Create a set so we ignore duplicates
    file_count = 0
    for file in list_of_files:
        full_path_to_file = os.path.join(path, file)
        if os.path.isfile(full_path_to_file):
            extension = os.path.splitext(full_path_to_file)[1]
            extensions.add(extension)
            file_count += 1

    return Summary(number_of_filetypes=len(extensions), number_of_images=file_count, file_types=extensions)