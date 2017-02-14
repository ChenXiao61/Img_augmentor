from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import *

from .Operations import *
from .ImageUtilities import scan_directory

import os
import random
import uuid
import string

from tqdm import tqdm
from PIL import Image  # TODO: Check how to define Pillow vs. PIL in the requirements file.


class Pipeline(object):
    def __init__(self, source_directory, recursive_scan=False, output_directory="output",
                 save_format="JPEG"):
        """
        Create a new Pipeline object pointing to a directory containing your
         original image dataset.

        Create a new Pipeline object, using the :attr:`source_directory`
         parameter as a source directory where your original images are
         stored. This folder will be scanned, and any valid file files
         will be collected and used as the original dataset that should
         be augmented. The scan will find any image files with the extensions
         JPEG/JPG, PNG, and GIF (case insensitive).

        :param source_directory: A directory on your filesystem where your
         original images are stored.
        :param recursive_scan: Whether the :attr:`source_directory` should
         be recursively scanned. Default is False.
        :param output_directory: Specifies where augmented images should be
         saved to the disk. Default is the directory **source** relative to
         the path where the original image set was specified. If it does not
         exist it will be created.
        :param save_format: The file format to use when saving newly created,
         augmented images. Default is JPEG. Legal options are BMP, PNG, and
         GIF.
        """
        random.seed()

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

    def __execute(self, image):
        self.image_counter += 1
        for operation in self.operations:
            r = round(random.uniform(0, 1), 1)
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
        if len(self.image_list) is 0:
            raise IndexError("There are no images in the pipeline. Add a directory using add_directory(path).")

        i = 1
        progress_bar = tqdm(total=n, desc="Executing Pipeline", unit=' Image Operations')
        while i <= n:
            for image_path in self.image_list:
                if i <= n:
                    self.__execute(Image.open(image_path))
                    progress_bar.set_description("Processing %s" % os.path.split(image_path)[1])
                    progress_bar.update(1)
                i += 1
        progress_bar.close()

    def add_operation(self, operation):
        """
        Add an operation directly to the pipeline. Can be used to add custom
         operations a pipeline.

        .. seealso:: The :class:`Operation` class.

        To add customer operations to a pipeline, subclass from
         Operation, overload its methods, and insert it into the pipeline
         using this method.

        :param operation: An object of the operation you wish to add to the
         pipeline. Will accept custom operations written at run-time.
        :type operation: Operation
        :return: None
        """
        self.operations.append(operation)

    @staticmethod
    def set_seed(self, seed):
        random.seed(seed)

    def rotate90(self, probability):
        """
        Rotate an image by 90 degrees.

        The operation will rotate an image by 90 degrees, and will be performed with a specified probability.

        :param probability: The probability that an image will have this operation applied when \
         being passed through the pipeline.
        :return: None
        """
        self.operations.append(Rotate(probability=probability, rotation=90))
        self.add_operation(Rotate(probability=probability, rotation=90))

    def rotate180(self, probability):
        """
        Rotate an image by 180 degrees.

        The operation will rotate an image by 180 degrees, and will be performed with a specified probability.

        :param probability: The probability that an image will have this operation applied when \
         being passed through the pipeline.
        :return: None
        """
        self.operations.append(Rotate(probability=probability, rotation=180))

    def rotate270(self, probability):
        """
        Rotate an image by 270 degrees.

        The operation will rotate an image by 270 degrees, and will be performed with a specified probability, \
         defined by the ``probability`` parameter.

        :param probability: The probability that an image will have this operation applied when \
         being passed through the pipeline.
        :return: None
        """
        self.operations.append(Rotate(probability=probability, rotation=270))

    def rotate(self, max_left_rotation=10, max_right_rotation=10, probability=1.0):
        """
        Rotate an image by an arbitrary amount.

        The operation will rotate an image by an random amount, within a range specified. The parameters \
         ``max_left_rotation`` and ``max_right_rotation`` allow you to control this range. If you wish to rotate \
         the images by an exact number of  degrees, set both ``max_left_rotation`` and ``max_right_rotation`` to \
         the same value.

        :param max_left_rotation: The maximum number of degrees the image can be rotated to the left.
        :param max_right_rotation: The maximum number of degrees the image can be rotated to the left.
        :param probability: The probability that an image will have this operation applied when \
         being passed through the pipeline.
        :return: None
        """
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

    def random_distortion(self, approximate_grid_size, sigma, probability=1.0):
        self.operations.append(Distort())

    def zoom(self, probability, min_factor=1.05, max_factor=1.2):
        self.operations.append(Zoom(probability=probability, min_factor=min_factor, max_factor=max_factor))

    def crop_by_size(self, width, height, centre=True):
        """
        Crop an image by a set of dimensions.

        Crop each image according to `width` and `height`, by default in the centre of each image,
         otherwise at a random location within the image.

        :param width: The width of the desired crop.
        :param height: The height of the desired crop.
        :param centre: If **True**, crops from the centre of the image, otherwise crops at a random location
         within the image, maintaining the dimensions specified.
        :return: None
        """
        self.operations.append(Crop(probability=1.0, width=width, height=height, centre=centre))

    def crop_randomly_by_percentage(self, probability, percent_to_crop):

        self.operations.append(Crop(probability=1.0))

    def crop_by_number_of_tiles(self, number_of_crops_per_image):
        # In this function we want to crop images, based on the a number of crops per image
        raise NotImplementedError

    def crop_by_percentage(self, percent_size_of_crop, from_center=True):
        raise NotImplementedError

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

    def sample_from_new_image_source(self, image_source, n, output_directory="output"):
        """
        Uses the current pipeline to generate images from a different image source.

        This function allows you to use the current pipeline to generate samples on a different image source, \
         defined by the :attr:`image_source` parameter. The ``image_source`` can either be a path to a single \
         image, or a path to a folder containing any number of images.

        .. seealso:: The :func:`sample` function.

        :param image_source: Either a path to a single image, or a path to a folder containing any number of \
         images to be passed through the current pipeline.
        :param n: The number of samples to generate from the current pipeline.
        :param output_directory: Optional parameter allowing you to supply a path for where to save \
         generated images. By default this is a directory named output relative to the source of the image(s).
        :type image_source: String
        :type n: Int
        :type output_directory: String
        :return: None
        """
        raise NotImplementedError

########################################################################################################################
# To be implemented                                                                                                    #
########################################################################################################################
    def new_operation(self, operation, parameters):
        # Add ability to add a new operation at runtime.

        function_name = string.lower(operation.__name__)
        class_name = string.capwords(operation.__name__)

        dyn_class = type(class_name, (object,), parameters)

        # globals()[]

        raise NotImplementedError

    def add_further_directory(self, new_source_directory, recursive_scan=False):
        if not os.path.exists(new_source_directory):
            raise IOError("The path does not appear to exist.")
        raise NotImplementedError

    def apply_pipeline(self, image):
        # Apply the current pipeline to a single image, returning the newly created image.
        # Not yet implemented.

        raise NotImplementedError

    def skew(self):
        # Perspective skew an image.
        # Not yet implemented.
        raise NotImplementedError

    def pad(self):
        # Functionality to pad a non-square image with borders to make it a certain aspect ratio.
        # Not yet implemented.
        raise NotImplementedError

########################################################################################################################
# Utility Functions                                                                                                    #
########################################################################################################################
    @staticmethod
    def extract_paths_and_extensions(self, image_path):
        """
        Extract an image's file name, its extension, and its root path (the entire path without the file name).

        :param image_path: The path to the image.
        :type image_path: String
        :return: The image's file name (file_name), extension (extension), and root path (root_path).
        """
        file_name, extension = os.path.splitext(image_path)
        root_path = os.path.dirname(image_path)

        return file_name, extension, root_path
