from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import str
from future import standard_library
standard_library.install_aliases()
from Augmentor import Image, ImageOps
from Augmentor import random
from Augmentor import BytesIO
from io import StringIO


def calc_chance(percent):
    if percent >= 1:
        return 1
    elif percent <= 0:
        return 0

    random_number = random.random()
    if random_number > percent:
        return 0
    else:
        return 1


class ImageOperations(object):
    def flip_x(self, image_container, storage_location, chance=1):
        if calc_chance(chance):
            generated_image = image_container.image.transpose(Image.FLIP_LEFT_RIGHT)
            file_name = image_container.directory + '/' + image_container.filename + "_flipX" + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def flip_y(self, image_container, storage_location, chance=1):
        if calc_chance(chance):
            generated_image = image_container.image.transpose(Image.FLIP_TOP_BOTTOM)
            file_name = image_container.directory + '/' + image_container.filename + "_flipY" + image_container.extension

            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def rotate_90(self, image_container, storage_location, chance=1):
        if calc_chance(chance):
            generated_image = image_container.image.transpose(Image.ROTATE_90)
            file_name = image_container.directory + '/' + image_container.filename + "_rotate90" + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def rotate_180(self, image_container, storage_location, chance=1):
        if calc_chance(chance):
            generated_image = image_container.image.transpose(Image.ROTATE_180)
            file_name = image_container.directory + '/' + image_container.filename + "_rotate180" + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def rotate_270(self, image_container, storage_location, chance=1):
        if calc_chance(chance):
            generated_image = image_container.image.transpose(Image.ROTATE_270)
            file_name = image_container.directory + '/' + image_container.filename + "_rotate270" + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def resize(self, image_container, height, width, storage_location, chance=1):
        if width == 0 or height == 0:
            return
        if calc_chance(chance):
            generated_image = image_container.image.resize((width, height), Image.ANTIALIAS)
            file_name = image_container.directory + '/' + image_container.filename + "_resize" + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def scale(self, image_container, height, width, storage_location, chance=1):
        if width == 0 or height == 0:
            return

        if calc_chance(chance):
            generated_image = ImageOps.fit(image_container.image, (width, height), Image.ANTIALIAS)
            file_name = image_container.directory + '/' + image_container.filename + "_scale" + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def rotate(self, image_container, degree, storage_location, chance=1):
        if degree < 0:
            return

        if calc_chance(chance):
            generated_image = image_container.image.rotate(degree)
            file_name = image_container.directory + '/' + image_container.filename + "_rotate" + str(
                degree) + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def convert_grayscale(self, image_container, storage_location, chance=1):
        if calc_chance(chance):
            generated_image = image_container.image.convert('L')
            file_name = image_container.directory + '/' + image_container.filename + "_grayscale" + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def crop(self, image_container, height, width, storage_location, chance=1):
        if height <= 0 or width <= 0:
            return

        if calc_chance(chance):
            org_width, org_height = image_container.image.size
            if org_height <= height or org_width <= width:
                return
            y_start = random.randint(0, org_height - height)
            x_start = random.randint(0, org_width - width)
            generated_image = image_container.image.crop((x_start, y_start, x_start + width, y_start + height))
            file_name = image_container.directory + '/' + image_container.filename + '_crop' + str(width) + str(
                height) + image_container.extension
            self.save_image(generated_image, file_name, image_container.extension, storage_location)

    def save_image(self, generated_image, new_file_name, file_extension, storage_location):

        if storage_location is None:
            generated_image.save(new_file_name)
        elif isinstance(storage_location, list):
            buffer = BytesIO()
            img_format = "JPEG"
            if file_extension[1:] == 'PNG':
                img_format = 'PNG'

            generated_image.save(buffer, img_format)
            buffer.seek(0)
            storage_location.append(buffer)
        else:
            print("Unsupported storage type.")
