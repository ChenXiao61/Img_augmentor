from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from PIL import Image, ImageOps
from .ImageUtilities import extract_paths_and_extensions
from math import floor, ceil

import os
import random

# Python 2-3 compatibility - not currently needed.
# try:
#    from StringIO import StringIO
# except ImportError:
#    from io import StringIO


class Operation(object):
    """
    The class :class:`Operation` represents the Base class for all operations
    that can be performed. Inherit from :class:`Operation`, overload its
    methods, and instantiate super to create a new operation.
    """
    def __init__(self, probability):
        self.probability = probability

    def __str__(self):
        return self.__class__.__name__

    def perform_operation(self, image):
        raise NotImplementedError("Illegal call to base class.")

    @staticmethod
    def extract_paths_and_extensions(image_path):
        file_name, extension = os.path.splitext(image_path)
        root_path = os.path.dirname(image_path)

        return file_name, extension, root_path


class HistogramEqualisation(Operation):
    def __init__(self, probability):
        Operation.__init__(self, probability)

    # TODO: We may need to apply this to each channel:
    # This might be a color image.
    # The histogram will be computed on the flattened image.
    # You can instead apply this function to each color channel.
    # with warnings.catch_warnings():
    #    warnings.simplefilter("ignore")
    def perform_operation(self, image):
        return ImageOps.equalize(image)


class Greyscale(Operation):
    def __init__(self, probability):
        Operation.__init__(self, probability)

    def perform_operation(self, image):
        return ImageOps.grayscale(image)


class Invert(Operation):
    def __init__(self, probability):
        Operation.__init__(self, probability)

    def perform_operation(self, image):
        return ImageOps.invert(image)


class BlackAndWhite(Operation):
    def __init__(self, probability):
        Operation.__init__(self, probability)

    def perform_operation(self, image):
        # TODO: Currently this has been taken from URL below, needs to be changed anyway.
        # http://stackoverflow.com/questions/18777873/convert-rgb-to-black-or-white
        image = ImageOps.grayscale(image)
        image = image.point(lambda x: 0 if x < 128 else 255, '1')
        return image


class Shear(Operation):
    def __init__(self, probability, angle):
        Operation.__init__(self, probability)
        self.angle = angle

    def perform_operation(self, image):
        pass


class Rotate(Operation):
    def __init__(self, probability, rotation):
        Operation.__init__(self, probability)
        self.rotation = rotation

    def __str__(self):
        return "Rotate " + str(self.rotation)

    def perform_operation(self, image):
        return image.rotate(self.rotation, expand=True)  # TODO: We are gonna have to check for 90 and 270 deg rotations


class RotateRange(Operation):
    def __init__(self, probability, rotate_range):
        Operation.__init__(self, probability)
        self.max_left_rotation = -abs(rotate_range[0])  # Ensure always negative
        self.max_right_rotation = abs(rotate_range[1])  # Ensure always positive

    def perform_operation(self, image):
        # This may be of use: http://stackoverflow.com/questions/34747946/rotating-a-square-in-pil
        random_left = random.randint(self.max_left_rotation, -1)
        random_right = random.randint(1, self.max_right_rotation)

        left_or_right = random.randint(0, 1)

        if left_or_right == 0:
            return image.rotate(random_left)
        if left_or_right == 1:
            return image.rotate(random_right)


class Resize(Operation):
    def __init__(self, probability, width, height, resample_filter):
        Operation.__init__(self, probability)
        self.width = width
        self.height = height
        self.resample_filter = resample_filter

    def perform_operation(self, image):
        # TODO: Automatically change this to ANTIALIAS or BICUBIC depending on the size of the file
        return image.resize((self.width, self.height), eval("Image.%s" % self.resample_filter))


class Flip(Operation):
    def __init__(self, probability, top_bottom_left_right):
        Operation.__init__(self, probability)
        self.top_bottom_left_right = top_bottom_left_right

    def perform_operation(self, image):
        if self.top_bottom_left_right == "LEFT_RIGHT":
            return image.transpose(Image.FLIP_LEFT_RIGHT)
        elif self.top_bottom_left_right == "TOP_BOTTOM":
            return image.transpose(Image.FLIP_TOP_BOTTOM)


class Crop(Operation):
    def __init__(self, probability, width, height, centred):
        Operation.__init__(self, probability)
        self.width = width
        self.height = height
        self.centred = centred

    def perform_operation(self, image):
        new_width = self.width / 2.
        new_height = self.height / 2.

        half_the_width = image.size[0] / 2
        half_the_height = image.size[1] / 2

        return image.crop(
            (
                half_the_width - ceil(new_width),
                half_the_height - ceil(new_height),
                half_the_width + floor(new_width),
                half_the_height + floor(new_height)
            )
        )


class CropPercentage(Operation):
    def __init__(self, probability, percentage_area, centre):
        Operation.__init__(self, probability)
        self.percentage_area = percentage_area
        self.centre = centre

    def perform_operation(self, image):
        w, h = image.size
        w_new = int(floor(w * self.percentage_area))  # TODO: Floor might return 0, so we need to check this.
        h_new = int(floor(h * self.percentage_area))

        if self.centre:
            left_shift = floor(w_new / 2.)
            down_shift = floor(h_new / 2.)
            return image.crop((left_shift, down_shift, w_new + left_shift, h_new + down_shift))
        else:
            random_left_shift = random.randint(0, (w - w_new))  # Note: randint() is from uniform distribution.
            random_down_shift = random.randint(0, (h - h_new))
            return image.crop((random_left_shift, random_down_shift, w_new + random_left_shift, h_new + random_down_shift))


class CropRandom(Operation):
    def __init__(self, probability, percentage_area):
        Operation.__init__(self, probability)
        self.percentage_area = percentage_area

    def perform_operation(self, image):
        w, h = image.size

        # TODO: Fix this, as it is currently 1/4 of the area for 0.5 rather than 1/2.
        w_new = int(floor(w * self.percentage_area))  # TODO: Floor might return 0, so we need to check this.
        h_new = int(floor(h * self.percentage_area))

        random_left_shift = random.randint(0, (w - w_new))  # Note: randint() is from uniform distribution.
        random_down_shift = random.randint(0, (h - h_new))

        return image.crop((random_left_shift, random_down_shift, w_new + random_left_shift, h_new + random_down_shift))


class Skew(Operation):
    def __init__(self, probability, max_skew_left, max_skew_right):
        Operation.__init__(self, probability)
        self.max_skew_left = max_skew_left
        self.max_skew_right = max_skew_right

    def perform_operation(self, image):
        pass


class Scale(Operation):
    """
    Class to increase or decrease images by a certain factor. The ``Resize`` class handles images \
    that need to be re-sized with different **dimensions**, which may not maintain aspect ratio.
    """
    def __init__(self, probability, x_scale_factor, y_scale_factor):
        Operation.__init__(self, probability)
        self.x_scale_factor = x_scale_factor
        self.y_scale_factor = y_scale_factor

    # Resize by a certain factor (*not* dimensions - which would uniformly resize all
    # images to X*Y while scale depends on the size of the input)
    def perform_operation(self, image):
        pass


class Distort(Operation):
    def __init__(self, probability, approximate_grid_size, sigma):
        Operation.__init__(self, probability)
        self.approximate_grid_size = approximate_grid_size
        self.sigma = sigma

    def perform_operation(self, image):
        w, h = image.size
        dx = self.approximate_grid_size
        dy = self.approximate_grid_size
        return image.transform(image.size, Image.MESH,
                            [((0, 0, w // 2, h // 2),  # Specifies xy top left, xy bottom right DESTINATION
                              (0, 0, 0, h // 2,
                               w // 2 + dx, h // 2 + dy, w // 2, 0)),  # SOURCE polygon of xy top left, xy bottom left, xy bottom right, xy top right

                             ((w // 2, 0, w, h // 2),
                              (w // 2, 0, w // 2 + dx, h // 2 + dy,
                               w, h // 2, w, 0)),

                             ((0, h // 2, w // 2, h),
                              (0, h // 2, 0, h,
                               w // 2, h, w // 2 + dx, h // 2 + dy)),

                             ((w // 2, h // 2, w, h),
                              (w // 2 + dx, h // 2 + dy, w // 2, h,
                               w, h, w, h // 2))],
                            )


class Zoom(Operation):
    # TODO: Zoom dimensions and do not crop, so that the crop can be applied manually later
    def __init__(self, probability, min_factor, max_factor):
        Operation.__init__(self, probability)
        self.min_factor = min_factor
        self.max_factor = max_factor

    def perform_operation(self, image):
        factor = round(random.uniform(self.min_factor, self.max_factor), 2)
        original_width, original_height = image.size
        # TODO: Join these two functions together so that we don't have this image_zoom variable lying around.
        image_zoomed = image.resize((int(round(image.size[0] * factor)), int(round(image.size[1] * factor))))

        # Return the centre of the zoomed image, so that it is the same dimensions as the original image
        half_the_width = image_zoomed.size[0] / 2
        half_the_height = image_zoomed.size[1] / 2
        return image_zoomed.crop(
            (
                half_the_width - ceil((original_width / 2.)),
                half_the_height - ceil((original_height / 2.)),
                half_the_width + floor((original_width / 2.)),
                half_the_height + floor((original_height / 2.))
            )
        )
