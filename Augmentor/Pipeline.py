# Pipeline.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Licensed under the terms of the MIT Licence.

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import *

from .Operations import *
from .ImageUtilities import scan_directory, AugmentorImage

import os
import random
import uuid
import warnings

from tqdm import tqdm
from PIL import Image


class Pipeline(object):
    """
    The Pipeline class handles the creation of augmentation pipelines
    and the generation of augmented data by applying operations to
    this pipeline.
    """
    def __init__(self, source_directory, ground_truth_directory=None, output_directory="output", save_format="JPEG"):
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

        # TODO: Allow a single image to be added when initialising.
        self.image_counter = 0
        self.augmentor_images = []
        self.distinct_dimensions = set()
        self.distinct_formats = set()
        # TODO: Refactor this out
        self.ground_truth_image_list = {}

        # Now we populate some fields, which we may need to do again later if another
        # directory is added, so we place it all in a function of its own.
        self._populate(source_directory=source_directory,
                       output_directory=output_directory,
                       ground_truth_directory=ground_truth_directory,
                       ground_truth_output_directory=output_directory)

        self._valid_formats = ["PNG", "BMP", "GIF", "JPEG"]
        self._legal_filters = ["NEAREST", "BICUBIC", "ANTIALIAS", "BILINEAR"]
        self.save_format = save_format
        self.operations = []

        # print("Initialised with %s image(s) found in selected directory." % len(self.augmentor_images))
        # print("Output directory set to %s." % self.output_directory)

    def _populate(self, source_directory, output_directory, ground_truth_directory, ground_truth_output_directory):
        """
        Private method for populating member variables with AugmentImage
        objects for each of the images found in the source directory 
        specified by the user. It also populates a number of fields such as
        the :attr:`output_directory` member variable, used later when saving
        images to disk.
        
        This method is used by :func:`__init__`. 
        
        :param source_directory: The directory to scan for images.
        :param output_directory: The directory to set for saving files.
         Defaults to a directory named output relative to 
         :attr:`source_directory`.
        :param ground_truth_directory: A directory containing ground truth 
         files for the associated images in the :attr:`source_directory` 
         directory.
        :param ground_truth_output_directory: A path to a directory to store
         the output of the operations on the ground truth data set.
        :type source_directory: String
        :type output_directory: String
        :type ground_truth_directory: String
        :type ground_truth_output_directory: String
        :return: None
        """

        ####
        # NOTE.
        # A lot of this functionality, such as checking for paths that exist
        # and that they are writable, etc., will eventually be moved to the
        # AugmentorImage class in the ImageUtilities module.
        ####

        # Check if the source directory for the original images to augment exists at all
        if not os.path.exists(source_directory):
            raise IOError("The source directory you specified does not exist.")

        # If a ground truth directory is being specified we will check here if the path exists at all.
        if ground_truth_directory:
            if not os.path.exists(ground_truth_directory):
                raise IOError("The ground truth source directory you specified does not exist.")

        # Get the absolute path of the output directory specified.
        abs_output_directory = os.path.join(source_directory, output_directory)

        # Check if the output directory exists, if it does not attempt to create it
        # and raise an exception if this fails.
        if not os.path.exists(abs_output_directory):
            try:
                os.makedirs(abs_output_directory)
            except IOError:
                print("Insufficient rights to read or write output directory (%s)" % abs_output_directory)

        self.image_list = scan_directory(source_directory)

        for image_path in scan_directory(source_directory):
            single_augmentor_image = AugmentorImage(image_path=image_path,
                                                    output_directory=abs_output_directory)
            if ground_truth_directory:
                single_augmentor_image.ground_truth = os.path.join(os.path.abspath(ground_truth_directory),
                                                                   os.path.basename(image_path))
            self.augmentor_images.append(single_augmentor_image)

        # TODO: Check if all ground truth images are readable.
        for augmentor_image in self.augmentor_images:
            try:
                with Image.open(augmentor_image.image_path) as opened_image:
                    self.distinct_dimensions.add(opened_image.size)
                    self.distinct_formats.add(opened_image.format)
            except IOError:
                print("There is a problem with image %s in your source directory. "
                      "It is unreadable and will not be included when augmenting."
                      % os.path.basename(augmentor_image.image_path))
                self.augmentor_images.remove(augmentor_image)

        # Finally, we will print some informational messages.
        print("Initialised with %s image(s) found in selected directory." % len(self.augmentor_images))
        print("Output directory set to %s." % abs_output_directory)

    def _execute(self, augmentor_image, save_to_disk=True):
        """
        Private method. Used to pass an image through the current pipeline,
        and return the augmented image.
        
        The returned image can then either be saved to disk or simply passed
        back to the user. Currently this is fixed to True, as Augmentor
        has only been implemented to save to disk at present.

        :param augmentor_image: The image to pass through the pipeline.
        :param save_to_disk: Whether to save the image to disk. Currently
         fixed to true.
        :type augmentor_image: :class:`ImageUtilities.AugmentorImage`
        :type save_to_disk: Boolean
        :return: The augmented image.
        """
        self.image_counter += 1

        image = Image.open(augmentor_image.image_path)

        for operation in self.operations:
            r = round(random.uniform(0, 1), 1)
            if r <= operation.probability:
                image = operation.perform_operation(image)

        if save_to_disk:
            file_name = str(uuid.uuid4()) + "." + self.save_format
            try:
                # A strange error is forcing me to do this at the moment, but will fix later properly
                if image.mode != "RGB":
                    image = image.convert("RGB")
                # For testing this cab be commented out to create only one output image.
                # file_name = "test"
                image.save(os.path.join(augmentor_image.output_directory, file_name), self.save_format)
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
        if len(self.augmentor_images) == 0:
            raise IndexError("There are no images in the pipeline. "
                             "Add a directory using add_directory(), "
                             "pointing it to a directory containing images.")

        sample_count = 1

        progress_bar = tqdm(total=n, desc="Executing Pipeline", unit=' Samples', leave=False)
        while sample_count <= n:
            for augmentor_image in self.augmentor_images:
                if sample_count <= n:
                    self._execute(augmentor_image)
                    file_name_to_print = os.path.basename(augmentor_image.image_path)
                    # This is just to avoid printing very long file names
                    if len(file_name_to_print) >= 30:
                        file_name_to_print = file_name_to_print[0:10] + "..." + \
                                             file_name_to_print[-10: len(file_name_to_print)]
                    progress_bar.set_description("Processing %s" % file_name_to_print)
                    progress_bar.update(1)
                sample_count += 1
        progress_bar.close()

    def apply_current_pipeline(self, image_path, save_to_disk=False):
        """
        Apply the current pipeline to a single image, returning the
        transformed image. By default, the transformed image is not saved 
        to disk.

        This method can be used to pass a single image through the
        pipeline, but will not save the transformed to disk by
        default. To save to disk, supply a :attr:`save_to_disk`
        argument set to True.

        :param image_path: The path to the image to pass through the current 
         pipeline.
        :param save_to_disk: Whether to save the image to disk. Defaults to
         False.
        :type image: String
        :type save_to_disk: Boolean
        :return: The transformed image.
        """

        return self._execute(AugmentorImage(os.path.abspath(image_path), None), save_to_disk)

    def add_operation(self, operation):
        """
        Add an operation directly to the pipeline. Can be used to add custom
        operations to a pipeline.

        To add custom operations to a pipeline, subclass from
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
        Remove the operation specified by :attr:`operation_index`, if
        supplied, otherwise it will remove the latest operation added to the
        pipeline.

         .. seealso:: Use the :func:`status` function to find an operation's
          index.

        :param operation_index: The index of the operation to remove.
        :return: The removed operation. You can reinsert this at end of the
         pipeline using :func:`add_operation` if required.
        """

        self.operations.pop(operation_index)

    def add_ground_truth_directory(self, ground_truth_directory, halt_on_non_match=False):
        """
        Add a directory containing the ground truth for your current set of
        images.

        This function allows you to add ground truth images that relate to
        the images currently in pipeline. It will scan a folder and collate
        images in the pipeline with the ground truth images in the new
        ground truth directory by *file name*, ignoring file extension.
        This means you can use the same directory if the file names are
        differentiable only be extension.

        :param ground_truth_directory: The new directory to scan.
        :param halt_on_non_match: Do not halt on non-match and throw away
         any images if :attr:`False`. Otherwise halt on non-match, if
         :attr:`True`.
        :exception: IOError if no ground truth images found or if
         :attr:`halt_on_non_match` is :attr:`True`.
        :return: None
        """

        # Right now, it seems unlikely that we will need this function at all.
        # Keeping it here for the meantime however.
        raise NotImplementedError("This method is currently not implemented.")

        # if not halt_on_non_match:
        #     ground_truth_file_paths = scan_directory(ground_truth_directory)

        # The variable ground_truth_files contains paths, so we need to strip these away
        # ground_truth_file_names = \
        #    [os.path.basename(x) for x in ground_truth_file_paths]
        # original_file_names = \
        #     [os.path.basename(x) for x in self.image_list]

        # common_files = set(ground_truth_file_names).intersection(original_file_names)
        # missing_files = set(ground_truth_file_names).difference(original_file_names)

        # return common_files, missing_files

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

        if len(self.operations) != 0:
            operation_index = 0
            for operation in self.operations:
                print("Index %s:\n\tOperation %s (probability: %s):" % (operation_index, operation, operation.probability))
                for operation_attribute, operation_value in operation.__dict__.items():
                    print ("\t\tAttribute: %s (%s)" % (operation_attribute, operation_value))
                operation_index += 1
            print()

        print("There are %s image(s) in the source directory." % len(self.image_list))

        if len(self.image_list) != 0:
            print("Dimensions:")
            for distinct_dimension in self.distinct_dimensions:
                print("\tWidth: %s Height: %s" % (distinct_dimension[0], distinct_dimension[1]))
            print("Formats:")
            for distinct_format in self.distinct_formats:
                print("\t %s" % distinct_format)

        print("\nYou can remove operations using the appropriate index and the remove_operation(index) function.")

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

    def rotate(self, probability, max_left_rotation, max_right_rotation):
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
        self.add_operation(RotateRange(probability=probability, max_left_rotation=max_left_rotation,
                                       max_right_rotation=max_right_rotation))

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

    def random_distortion(self, probability, grid_width, grid_height, magnitude, randomise_magnitude=True):
        """
        Performs a random, elastic distortion on an image.

        This function performs a randomised, elastic distortion controlled
        by the parameters specified. The grid width and height controls how
        fine the distortions are. Smaller sizes will result in larger, more
        pronounced, and less granular distortions. Larger numbers will result
        in finer, more granular distortions. The magnitude of the distortions
        can be controlled using magnitude. This can be random or fixed.

        :param probability: The probability that the function will execute
         when the image is passed through the pipeline.
        :param grid_width: The number of rectangles in the grid's horizontal
         axis.
        :param grid_height: The number of rectangles in the grid's vertical
         axis.
        :param magnitude: The magnitude of the distortions.
        :param randomise_magnitude: Specifies whether the magnitude should be 
         used as a range if True, or as a constant value, if False.
        :return: None
        """
        self.add_operation(Distort(probability=probability, grid_width=grid_width,
                                   grid_height=grid_height, magnitude=magnitude, randomise_magnitude=randomise_magnitude))

    def zoom(self, probability, min_factor, max_factor):
        """
        Zoom in to an image, while maintaining its aspect ratio.
        
        :param probability: 
        :param min_factor: 
        :param max_factor: 
        :return: 
        """
        self.add_operation(Zoom(probability=probability, min_factor=min_factor, max_factor=max_factor))

    def crop_by_size(self, probability, width, height, centre=True):
        """
        Crop an image according to a set of dimensions.

        Crop each image according to :attr:`width` and :attr:`height`, by
        default at the centre of each image, otherwise at a random location
        within the image.

        .. seealso:: See :func:`crop_random` to crop a random, non-centred
         area of the image.
        
        :param probability: The probability that the function will execute
         when the image is passed through the pipeline.
        :param width: The width of the desired crop.
        :param height: The height of the desired crop.
        :param centre: If **True**, crops from the centre of the image,
         otherwise crops at a random location within the image, maintaining
         the dimensions specified.
        :return: None
        """
        self.add_operation(Crop(probability=probability, width=width, height=height, centre=centre))

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

    def crop_random_not_to_scale(self, probability, percentage_area):
        # TODO: Crop an area where the ratio is not kept the same, then resize to uniform dimensions
        raise NotImplementedError

    def crop_random_absolute(self, probability, width, height):
        raise NotImplementedError

    def crop_by_number_of_tiles(self, number_of_crops_per_image):
        # In this function we want to crop images, based on the a number of crops per image
        raise NotImplementedError

    def crop_by_percentage(self, percent_size_of_crop, from_center=True):
        raise NotImplementedError

    def histogram_equalisation(self, probability=1.0):
        if probability != 1:
            warnings.warn("For resizing, it is recommended that the probability is set to 1.", stacklevel=1)
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

        if scale_factor < 1.0:
            print("The scale cannot be lower than 1.0. Operation not added to pipeline.")
        else:
            self.add_operation(Scale(probability=probability,
                                     scale_factor=scale_factor))

    def resize(self, probability, width, height, resample_filter="BICUBIC"):
        """
        Resize an image according to a set of dimensions. 
        
        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed. For resizing,
         it is recommended that probability be set to 1.
        :param width: 
        :param height: 
        :param resample_filter: 
        :return: 
        """

        if probability != 1:
            warnings.warn("For resizing, it is recommended that the probability is set to 1.", stacklevel=1)

        if resample_filter in self._legal_filters:
            self.add_operation(Resize(probability=probability,
                                      width=width,
                                      height=height,
                                      resample_filter=resample_filter))
        else:
            print("The save_filter parameter must be one of ", self._legal_filters)
            print("E.g. save_filter(800, 600, \'BICUBIC\')")

    def skew_left_right(self, probability, magnitude=None):
        """
        Skew an image by tilting it left or right by a random amount. The 
        magnitude of this skew can be set to a maximum using the 
        magnitude parameter. This can be either a scalar representing the
        maximum tilt, or vector representing a range.
        
        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed.
        :param magnitude: The maximum tilt, which must be value between 0.1 
        and 1.0, where 1 represents a tilt of 45 degrees.
        :return: None 
        """
        self.add_operation(Skew(probability=probability,
                                skew_type="TILT_LEFT_RIGHT",
                                magnitude=magnitude))

    def skew_top_bottom(self, probability, magnitude=None):
        """
        Skew an image by tilting it forwards or backwards by a random amount. 
        The magnitude of this skew can be set to a maximum using the 
        magnitude parameter. This can be either a scalar representing the
        maximum tilt, or vector representing a range.

        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed.
        :param magnitude: The maximum tilt, which must be value between 0.1 
        and 1.0, where 1 represents a tilt of 45 degrees.
        :return: None 
        """
        self.add_operation(Skew(probability=probability,
                                skew_type="TILT_TOP_BOTTOM",
                                magnitude=magnitude))

    def skew_tilt(self, probability, magnitude=None):
        """
        Skew an image by tilting in a random direction, either forwards,
        backwards, left, or right, by a random amount. The magnitude of 
        this skew can be set to a maximum using the magnitude parameter.
        This can be either a scalar representing the maximum tilt, or 
        vector representing a range.
        
        :param probability: A value between 0 and 1 representing the
         probability that the operation should be performed. 
        :param magnitude: The maximum tilt, which must be value between 0.1 
        and 1.0, where 1 represents a tilt of 45 degrees.
        :return: 
        """
        self.add_operation(Skew(probability=probability,
                                skew_type="TILT",
                                magnitude=magnitude))

    def skew_corner(self, probability, magnitude=None):
        self.add_operation(Skew(probability=probability,
                                skew_type="CORNER",
                                magnitude=magnitude))

    def skew(self, probability, magnitude=None):
        self.add_operation(Skew(probability=probability,
                                skew_type=random.choice(["TILT", "CORNER"]),
                                magnitude=magnitude))

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

    def add_further_directory(self, new_source_directory, new_output_directory="output",
                              new_ground_truth_source_directory=None):

        if not os.path.exists(new_source_directory):
            raise IOError("The path does not appear to exist.")

        self.augmentor_images += self._populate(source_directory=new_source_directory,
                                                output_directory=new_output_directory,
                                                ground_truth_directory=new_ground_truth_source_directory)

    def apply_pipeline(self, image):
        # Apply the current pipeline to a single image, returning the newly created image.
        # Not yet implemented.

        raise NotImplementedError

    def shear(self, probability, max_shear_left, max_shear_right):
        """
        Shear the image by a specified number of degrees.
        
        :param probability: The probability that the operation is performed. 
        :param max_shear_left: The max number of degrees to shear to the left.
         Cannot be larger than 90 degrees.
        :param max_shear_right: The max number of degrees to shear to the 
         right. Cannot be larger than 90 degrees.
        :return: None
        """
        if max_shear_left >= 90 or max_shear_right >= 90:
            print("Cannot have a value larger than 90 degrees for angle.")
        else:
            self.add_operation(Shear(probability=probability,
                                     max_shear_left=max_shear_left,
                                     max_shear_right=max_shear_right))

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
        :return: A 3-tuple containing the image's file name, extension, and
         root path.
        """
        file_name, extension = os.path.splitext(image_path)
        root_path = os.path.dirname(image_path)

        return file_name, extension, root_path
