from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import *

from .Operations import *
from .ImageUtilities import scan_directory

import os
import random
import uuid

from tqdm import tqdm
from PIL import Image


class Pipeline(object):

    def __init__(self, source_directory, recursive_scan=False, output_directory="output",
                 save_format="JPEG", seed=None):

        if seed:
            random.seed(seed)  # This will hash strings to set a seed, but some hashing is non-deterministic!
        else:
            random.seed()  # Set this to blank to use /dev/random or the time if that does not exist.

        self.image_counter = 0

        # TODO: No need to place this in __init__ - move later.
        valid_formats = ["PNG", "BMP", "GIF", "JPEG"]  # See: https://infohost.nmt.edu/tcc/help/pubs/pil/formats.html

        self.save_format = save_format

        if not os.path.exists(source_directory):
            raise IOError("The path does not appear to exist.")

        # TODO: Change this so that we just use the relative path to get the absolute path.
        self.output_directory = os.path.join(source_directory, output_directory)

        if not os.path.exists(self.output_directory):
            try:
                os.makedirs(self.output_directory)
            except OSError as exception:
                raise exception

        self.source_directory = source_directory
        self.image_list = scan_directory(self.source_directory, recursive_scan)
        self.total_files = list(self.image_list)  # Ensure we get a new list and not a link.
        self.operations = []

        print("Initialised with %s images found in selected directory." % len(self.image_list))
        print("Output directory set to %s." % self.output_directory)

        # TODO: check each file to make sure it can be opened by PIL, perhaps like so:
        # for file_check in self.image_list:
        #     try:
        #         with Image.open(file_check) as im:
        #             print(file_check, im.format, "%dx%d" % im.size, im.mode)
        #     except IOError:
        #             self.image_list.remove(file_check)

    def execute(self):
        for operation in self.operations:
            new_files = []
            for image in tqdm(self.image_list, desc=str(operation)):
                operation.perform_operation(image)
            self.total_files.extend(new_files)

    def probabilistic(self, image):
        self.image_counter += 1
        for operation in self.operations:
            r = round(random.random(), 1)
            if r <= operation.probability:
                image = operation.perform_operation(image)
        # file_name = str(self.image_counter) + "." + self.save_format
        file_name = str(uuid.uuid4()) + "." + self.save_format
        try:
            image.save(os.path.join(self.output_directory, file_name), self.save_format)
        except IOError:
            print("Error writing %s." % file_name)
        return image

    def sample(self, n):
        # TODO: Check if there are any images in self.image_list as if there are 0, it will hang.
        i = 1
        progress_bar = tqdm(total=n, desc="Executing Pipeline", unit=' Image Operations')
        while i <= n:
            for image_path in self.image_list:
                if i <= n:
                    self.probabilistic(Image.open(image_path))
                    progress_bar.set_description("Processing %s" % os.path.split(image_path)[1])
                    progress_bar.update(1)
                i += 1
        progress_bar.close()

    def rotate90(self, probability):
        self.operations.append(Rotate(probability=probability, rotation=90))

    def rotate180(self, probability):
        self.operations.append(Rotate(probability=probability, rotation=180))

    def rotate270(self, probability):
        self.operations.append(Rotate(probability=probability, rotation=270))

    def rotate(self, max_left_rotation=10, max_right_rotation=10, probability=1.0):
        # TODO: Finish this check and decide if we want to specify a max_l/max_r or not...
        if max_left_rotation < 180 & max_right_rotation < 180:
            pass
        self.operations.append(RotateRange(probability=probability,
                                           rotate_range=(max_left_rotation, max_right_rotation)))

    def flip_top_bottom(self, probability):
        # Flip top to bottom (vertically)
        self.operations.append(Flip(probability=probability, top_bottom_left_right="TOP_BOTTOM"))

    def flip_left_right(self, probability):
        # Flip lef to right (horizontally)
        self.operations.append(Flip(probability=probability, top_bottom_left_right="LEFT_RIGHT"))

    def random_displacement(self, severity, fuzziness, rotate=True, probability=1.0):
        # Control the fuzziness of a transform
        pass

    def skew(self):
        pass

    def zoom(self, probability, min_factor=1.05, max_factor=1.2):
        self.operations.append(Zoom(probability=probability, min_factor=min_factor, max_factor=max_factor))
        pass

    def crop_by_number_of_tiles(self, number_of_crops_per_image):
        # In this function we want to crop images, based on the a number of crops per image
        pass

    def crop_by_size(self, dimensions_per_crop, overlap=False):
        # In this function we will crop as many as we can with no overlap (or with overlap, depending on the param)
        pass

    def crop_by_percentage(self, percent_size_of_crop, from_center=True):
        pass

    def crop_by_size(self, width, height, centre=True):
        """
        Crop each image according to width and height, by default in the centre of each image, otherwise at a random \
        location within the image.
        :param width: The width of the desired crop.
        :param height: The height of the desired crop.
        :param centre: If True, crops from the centre of the image, otherwise crops at a random location within the \
        image, maintaining the dimensions specified.
        :return: None.
        """
        self.operations.append(Crop(probability=1.0, width=width, height=height, centre=centre))

    def histogram_equalisation(self, probability=1.0):
        self.operations.append(HistogramEqualisation(probability=probability))

    def resize(self, width, height, probability=1.0, resample_filter="NEAREST"):
        # TODO: Make this automatic by default, i.e. ANTIALIAS if very small downsampling, BICUBIC if upsampling.
        legal_filters = ["NEAREST", "BICUBIC", "ANTIALIAS", "BILINEAR"]
        if resample_filter in legal_filters:
            self.operations.append(Resize(probability=probability, width=width,
                                          height=height, resample_filter=resample_filter))
        else:
            print("The save_filter parameter must be one of ", legal_filters)
            print("E.g. save_filter(800, 600, \'NEAREST\')")

    def __add_operation(self, operation):
        self.operations.append(operation)

    def add_further_directory(self, new_source_directory, recursive_scan=False):
        if not os.path.exists(new_source_directory):
            raise IOError("The path does not appear to exist.")
        # TODO: Add this functionality later.
        raise NotImplementedError

########################################################################################################################
# Utility Functions                                                                                                    #
########################################################################################################################
    @staticmethod
    def extract_paths_and_extensions(self, image_path):
        """
        Extract a image's file name, its extension, and its root path (the entire path without the file name).
        :param image_path:
        :return: The image's file name (file_name), extension (extension), and root path (root_path).
        """
        file_name, extension = os.path.splitext(image_path)
        root_path = os.path.dirname(image_path)

        return file_name, extension, root_path
