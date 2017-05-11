# ImageUtilities.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Licensed under the terms of the MIT Licence.
"""
The ImageUtilities module provides a number of helper functions, as well as
the main :class:`~Augmentor.ImageUtilities.AugmentorImage` class, that is used
throughout the package as a container class for images to be augmented.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import glob


class AugmentorImage(object):
    """
    Wrapper class containing paths to images, as well as a number of other 
    parameters, that are used by the Pipeline and Operation modules to perform 
    augmentation.
     
    Each image that is found by Augmentor during the initialisation of a 
    Pipeline object is contained with a new AugmentorImage object.
    """
    def __init__(self, image_path, output_directory):
        """
        To initialise an AugmentorImage object for any image, the image's
        file path is required, as well as that image's output directory,
        which defines where any augmented images are stored. 
        
        :param image_path: The full path to an image. 
        :param output_directory: The directory where augmented images for this
         image should be saved.
        """
        # Just to stop Pylint complaining about initialising these outside
        # of __init__ which is not actually happening, as the are being
        # initialised in the setters from within init, but anyway I shall obey.
        self._ground_truth = None
        self._image_path = None
        self._output_directory = None
        self._file_format = None  # TODO: pass this for each image.

        # Now we call the setters that we require.
        self.image_path = image_path
        self.output_directory = output_directory

    @property
    def output_directory(self):
        """
        The :attr:`output_directory` property contains a path to the directory 
        to which augmented images will be saved for this instance.
        
        :getter: Returns this image's output directory.
        :setter: Sets this image's output directory.
        :type: String
        """
        return self._output_directory

    @output_directory.setter
    def output_directory(self, value):
        self._output_directory = value

    @property
    def image_path(self):
        """
        The :attr:`image_path` property contains the absolute file path to the
        image.
        
        :getter: Returns this image's image path.
        :setter: Sets this image's image path
        :type: String
        """
        return self._image_path

    @image_path.setter
    def image_path(self, value):
        if os.path.exists(value):
            self._image_path = value
        else:
            raise IOError("The file specified does not exist.")

    @property
    def image_file_name(self):
        """
        The :attr:`image_file_name` property contains the **file name** of the
        image contained in this instance. **There is no setter for this 
        property.**
        
        :getter: Returns this image's file name.
        :type: String
        """
        return os.path.basename(self.image_path)

    @property
    def ground_truth(self):
        """
        The :attr:`ground_truth` property contains an absolute path to the
        ground truth file for an image.
        
        :getter: Returns this image's ground truth file path.
        :setter: Sets this image's ground truth file path.
        :type: String
        """
        return self._ground_truth

    @ground_truth.setter
    def ground_truth(self, value):
        # TODO: Include some kind of fuzzy search.
        if os.path.isfile(value):
            self._ground_truth = value


def extract_paths_and_extensions(image_path):
    """
    Extract an image's file name, its extension, and its root path (the
    image's absolute path without the file name).

    :param image_path: The path to the image.
    :type image_path: String
    :return: A 3-tuple containing the image's file name, extension, and
     root path.
    """
    file_name, extension = os.path.splitext(image_path)
    root_path = os.path.dirname(image_path)

    return file_name, extension, root_path


def scan_directory(source_directory):
    """
    Scan a directory for images, returning any images found with the
    extensions ``.jpg``, ``.JPG``, ``.jpeg``, ``.JPEG``, ``.gif``, ``.GIF``,
    ``.img``, ``.IMG``, ``.png`` or ``.PNG``.
    
    :param source_directory: The directory to scan for images.
    :type source_directory: String
    :return: A list of images found in the :attr:`source_directory`
    """
    file_types = ['*.jpg', '*.bmp', '*.jpeg', '*.gif', '*.img', '*.png']

    list_of_files = []

    if os.name == "nt":
        for file_type in file_types:
            list_of_files.extend(glob.glob(os.path.join(os.path.abspath(source_directory), file_type)))
    else:
        file_types.extend([str.upper(str(x)) for x in file_types])
        for file_type in file_types:
            list_of_files.extend(glob.glob(os.path.join(os.path.abspath(source_directory), file_type)))

    return list_of_files
