# Pipeline.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Licensed under the terms of the MIT Licence.

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

"""
The Pipeline module, containing any classes relating to the pipeline
functionality.
"""
__docformat__ = 'reStructuredText'


class Pipeline(object):
    """
    The Pipeline class handles the creation of augmentation pipelines
    and the generation of augmented data by applying operations to
    this pipeline.
    """
    def __init__(self, source_directory, recursive_scan=False, output_directory="output", save_format="JPEG"):
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
        :return: A :class:`Pipeline` object.
        """
        random.seed()

        self.image_counter = 0

        # TODO: No need to place this in __init__ - move later.
        # See: https://infohost.nmt.edu/tcc/help/pubs/pil/formats.html
        valid_formats = ["PNG", "BMP", "GIF", "JPEG"]

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
        self.operations = []

        # Scan the images to collect information about each image.
        self.distinct_dimensions = set()
        self.distinct_formats = set()
        for image in self.image_list:
            try:
                with Image.open(image) as opened_image:
                    self.distinct_dimensions.add(opened_image.size)
                    self.distinct_formats.add(opened_image.format)
            except IOError:
                print("There is a problem with image %s in your source directory. "
                      "It is unreadable and will not be included when augmenting." % image)
                self.image_list.remove(image)

        print("Initialised with %s image(s) found in selected directory." % len(self.image_list))
        print("Output directory set to %s." % self.output_directory)

        # TODO: check each file to make sure it can be opened by PIL, perhaps like so:
        # for file_check in self.image_list:
        #     try:
        #         with Image.open(file_check) as im:
        #             print(file_check, im.format, "%dx%d" % im.size, im.mode)
        #     except IOError:
        #             self.image_list.remove(file_check)

    def __execute(self, image, save_to_disk=True):
        """
        Private method. Used to pass an image through the current pipeline,
        and return the augmented image.

        :param image: The image to pass through the pipeline.
        :type image: :class:`PIL.Image`
        :return: The augmented image.
        """
        self.image_counter += 1

        for operation in self.operations:
            r = round(random.uniform(0, 1), 1)
            if r <= operation.probability:
                image = operation.perform_operation(image)

        if save_to_disk:
            file_name = str(uuid.uuid4()) + "." + self.save_format
            try:
                image.save(os.path.join(self.output_directory, file_name), self.save_format)
            except IOError:
                print("Error writing %s." % file_name)

        return image

    def sample(self, n):
        """
        Generate :attr:`n` number of samples from the current pipeline.

        This function samples from the pipeline, using the original images
        defined during instantiation. All images generated by the pipeline
        are by default stored in an ``output`` directory, relative to the
        path defined during the pipeline's instantiation.

        :param n: The number of new samples to produce.
        :type n: Int
        :return: None
        """
        if len(self.image_list) == 0:
            raise IndexError("There are no images in the pipeline. "
                             "Add a directory using add_directory(), "
                             "pointing it to a directory containing images.")

        sample_count = 1

        progress_bar = tqdm(total=n, desc="Executing Pipeline", unit=' Samples')
        while sample_count <= n:
            for image_path in self.image_list:
                if sample_count <= n:
                    self.__execute(Image.open(image_path))
                    progress_bar.set_description("Processing %s" % os.path.split(image_path)[1])
                    progress_bar.update(1)
                sample_count += 1
        progress_bar.close()

    def apply_current_pipeline(self, image, save_to_disk=False):
        """
        Apply the current pipeline to a single image, returning the
        transformed image. By default, the transformed image is not saved to
        disk.

        This method can be used to pass a single image through the
        pipeline, but will not save the transformed to disk by
        default. To save to disk, supply a :attr:`save_to_disk`
        argument set to True.

        :param image: The image to pass through the current pipeline.
        :param save_to_disk: Whether to save the image to disk. Defaults to
         False.
        :type image: Image
        :type save_to_disk: Boolean
        :return: The transformed image.
        """

        return self.__execute(image, save_to_disk)

    def add_operation(self, operation):
        """
        Add an operation directly to the pipeline. Can be used to add custom
        operations to a pipeline.

        To add customer operations to a pipeline, subclass from
        Operation, overload its methods, and insert it into the pipeline
        using this method.

         .. seealso:: The :class:`.Operation` class.

        :param operation: An object of the operation you wish to add to the
         pipeline. Will accept custom operations written at run-time.
        :type operation: Operation
        :return: None
        """
        if isinstance(operation, Operation):
            self.operations.append(operation)
        else:
            raise TypeError("Must be of type Operation to be added to the pipeline.")

    def remove_operation(self, operation_index=-1):
        """
        Remove the operation specified by :attr:`operation_index`. if
        supplied, otherwise it will remove the newest operation added to the
        pipeline.

         .. seealso:: Use :func:`status` function to find an operation's
          index.

        :param operation_index: The operation to remove.
        :return: The removed operation. You can add this to the end of the
         pipeline using :func:`add_operation` if required.
        """
        self.operations.pop(operation_index)

    def status(self):
        """
        Prints the status of the pipeline to the console.

        The status includes the number of operations currently attached to
        pipeline, each operation's parameters, the number of images in the
        pipeline, and a summary of the images' properties, such as their
        dimensions and formats.

        :return: None
        """
        # TODO: Return this as a dictionary of some kind and print from the dict if in console
        print("There are %s operation(s) in the current pipeline." % len(self.operations))
        operation_index = 0
        for operation in self.operations:
            print("Index %s. Operation %s (probability: %s):" % (operation_index, operation, operation.probability))
            for operation_attribute, operation_value in operation.__dict__.items():
                print ("\tAttribute: %s (%s)" % (operation_attribute, operation_value))
            operation_index += 1
        print()
        print("There are %s image(s) in the source directory." % len(self.image_list))
        print("Dimensions:")
        for distinct_dimension in self.distinct_dimensions:
            print("\tWidth: %s Height: %s" % (distinct_dimension[0], distinct_dimension[1]))
        print("Formats:")
        for distinct_format in self.distinct_formats:
            print("\t %s" % distinct_format)

    @staticmethod
    def set_seed(seed):
        """
        Set the seed of Python's internal random number generator.

        :param seed: The seed to use. Strings or other objects will be hashed.
        :type seed: Object
        :return: None
        """
        random.seed(seed)

    def rotate90(self, probability):
        """
        Rotate an image by 90 degrees.

        The operation will rotate an image by 90 degrees, and will be
        performed with a specified probability.

        :param probability: The probability that an image will have this
         operation applied when being passed through the pipeline.
        :return: None
        """
        self.add_operation(Rotate(probability=probability, rotation=90))

    def rotate180(self, probability):
        """
        Rotate an image by 180 degrees.

        The operation will rotate an image by 180 degrees, and will be
        performed with a specified probability.

        :param probability: The probability that an image will have this
         operation applied when being passed through the pipeline.
        :return: None
        """
        self.add_operation(Rotate(probability=probability, rotation=180))

    def rotate270(self, probability):
        """
        Rotate an image by 270 degrees.

        The operation will rotate an image by 270 degrees, and will be
        performed with a specified probability, defined by the
        :attr:`probability` parameter.

        :param probability: The probability that an image will have this
         operation applied when being passed through the pipeline.
        :return: None
        """
        self.add_operation(Rotate(probability=probability, rotation=270))

    def rotate_random_90(self, probability):
        """
        Rotate an image by either 90, 180, or 270 degrees, selected randomly.

        This function will rotate by either 90, 180, or 270 degrees. This is
        useful to avoid scenarios where images may be rotated back to their
        original positions (such as a rotate90() + rotate270() performed
        directly afterwards. The random rotation is chosen uniformly from
        90, 180, or 270. The probability controls the chance of the operation
        being performed at all, and does not affect the rotation degree.

        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed.
        :type probability: Float
        :return:
        """
        self.add_operation(Rotate(probability=probability, rotation=-1))

    def rotate(self, max_left_rotation=10, max_right_rotation=10, probability=1.0):
        """
        Rotate an image by an arbitrary amount.

        The operation will rotate an image by an random amount, within a range
        specified. The parameters :attr:`max_left_rotation` and
        :attr:`max_right_rotation` allow you to control this range. If you
        wish to rotate the images by an exact number of  degrees, set both
        :attr:`max_left_rotation` and :attr:`max_right_rotation` to the same
        value.

        :param max_left_rotation: The maximum number of degrees the image can
         be rotated to the left.
        :param max_right_rotation: The maximum number of degrees the image can
         be rotated to the left.
        :param probability: The probability that an image will have this
         operation applied when being passed through the pipeline.
        :return: None
        """
        if max_left_rotation < 180 & max_right_rotation < 180:
            raise ValueError("The max_left_rotation and max_right_rotation values cannot exceed 180.")
        self.add_operation(RotateRange(probability=probability,
                                       rotate_range=(max_left_rotation, max_right_rotation)))

    def flip_top_bottom(self, probability):
        """
        Flip (mirror) the image along its vertical axis, i.e. from top to
        bottom.

        This function mirrors the image along an axis, and is not a rotation
        transform. Mirroring can also be applied along the horizontal axis.

        .. seealso:: The :func:`flip_left_right` function.

        .. seealso:: The :func:`rotate` function.

        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed.
        :type probability: Float
        :return: None
        """
        self.add_operation(Flip(probability=probability, top_bottom_left_right="TOP_BOTTOM"))

    def flip_left_right(self, probability):
        """
        Flip (mirror) the image along its horizontal axis, i.e. from left to
        right.

        This function mirrors the image along an axis, and is not a rotation
        transform. Mirroring can also be applied along the vertical axis.

        .. seealso:: The :func:`flip_top_bottom` function.

        .. seealso:: The :func:`rotate` function.

        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed.
        :type probability: Float
        :return: None
        """
        self.add_operation(Flip(probability=probability, top_bottom_left_right="LEFT_RIGHT"))

    def flip_random(self, probability):
        """
        Flip (mirror) the image along **either** its horizontal or vertical
        axis.

        This function mirrors the image along either the horizontal axis or
        the vertical access. The axis is selected randomly.

        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed.
        :type probability: Float
        :return: None
        """
        self.add_operation(Flip(probability=probability, top_bottom_left_right="RANDOM"))

    def random_distortion(self, approximate_grid_size, sigma, probability=1.0):
        raise NotImplementedError
        # self.add_operation(Distort())

    def zoom(self, probability, min_factor=1.05, max_factor=1.2):
        self.add_operation(Zoom(probability=probability, min_factor=min_factor, max_factor=max_factor))

    def crop_by_size(self, width, height, centre=True):
        """
        Crop an image according to a set of dimensions.

        Crop each image according to :attr:`width` and :attr:`height`, by
        default at the centre of each image, otherwise at a random location
        within the image.

        .. seealso:: See :func:`crop_random` to crop a random, non-centred
         area of the image.

        :param width: The width of the desired crop.
        :param height: The height of the desired crop.
        :param centre: If **True**, crops from the centre of the image,
         otherwise crops at a random location within the image, maintaining
         the dimensions specified.
        :return: None
        """
        self.add_operation(Crop(probability=1.0, width=width, height=height, centre=centre))

    def crop_centre(self, probability, percentage_area):
        self.add_operation(CropPercentage(probability=probability, percentage_area=percentage_area, centre=True))

    def crop_random(self, probability, percentage_area):
        """
        Crop a random area of an image, based on the percentage area to be
        returned.

        This function crops a random area from an image, based on the area you
        specify using :attr:`percentage_area`.

        :param probability: The probability that the function will execute
         when the image is passed through the pipeline.
        :param percentage_area: The area, as a percentage of the current
         image's area, to crop.
        :type probability: Float
        :type percentage_area: Float
        :return: None
        """
        self.add_operation(CropPercentage(probability=probability, percentage_area=percentage_area, centre=False))

    def crop_random_absolute(self, probability, width, height):
        raise NotImplementedError

    def crop_by_number_of_tiles(self, number_of_crops_per_image):
        # In this function we want to crop images, based on the a number of crops per image
        raise NotImplementedError

    def crop_by_percentage(self, percent_size_of_crop, from_center=True):
        raise NotImplementedError

    def histogram_equalisation(self, probability=1.0):
        self.add_operation(HistogramEqualisation(probability=probability))

    def resize_by_percentage(self, percentage_resize):
        raise NotImplementedError

    def scale(self, probability, scale_factor):
        """
        Scale an image, while maintaining its aspect ratio.

        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed.
        :param scale_factor: The a value larger than 1.0 as a factor to scale by.
        :return:
        """
        self.add_operation(Scale(probability=probability, scale_factor=scale_factor))

    def resize(self, probability, width, height, resample_filter="NEAREST"):
        # TODO: Make this automatic by default, i.e. ANTIALIAS if downsampling, BICUBIC if upsampling.
        legal_filters = ["NEAREST", "BICUBIC", "ANTIALIAS", "BILINEAR"]
        if resample_filter in legal_filters:
            self.add_operation(Resize(probability=probability, width=width,
                                      height=height, resample_filter=resample_filter))
        else:
            print("The save_filter parameter must be one of ", legal_filters)
            print("E.g. save_filter(800, 600, \'NEAREST\')")

    def sample_from_new_image_source(self, image_source, n, output_directory="output"):
        """
        Uses the current pipeline to generate images from a different image
        source.

        This function allows you to use the current pipeline to generate
        samples on a different image source, defined by the
        :attr:`image_source` parameter. The ``image_source`` can either be a
        path to a single image, or a path to a folder containing any number
        of images.

        .. seealso:: The :func:`sample` function.

        :param image_source: Either a path to a single image, or a path to a
         folder containing any number of images to be passed through the
         current pipeline.
        :param n: The number of samples to generate from the current pipeline.
        :param output_directory: Optional parameter allowing you to supply a
         path for where to save generated images. By default this is a
         directory named output relative to the source of the image(s).
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
        raise NotImplementedError

        # We will not need to do any of this, users will be required to add operations
        # to the pipeline manually.
        # function_name = string.lower(operation.__name__)
        # class_name = string.capwords(operation.__name__)
        # dyn_class = type(class_name, (object,), parameters)
        # globals()[]

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
    def extract_paths_and_extensions(image_path):
        """
        Extract an image's file name, its extension, and its root path (the
        image's absolute path without the file name).

        :param image_path: The path to the image.
        :type image_path: String
        :return: A tuple containing the image's file name, extension, and
         root path.
        """
        file_name, extension = os.path.splitext(image_path)
        root_path = os.path.dirname(image_path)

        return file_name, extension, root_path
