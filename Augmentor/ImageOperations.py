from Augmentor import Image, ImageOps
from Augmentor import random


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

    def flip_x(self, image_source, chance=1):
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = image_container.image.transpose(Image.FLIP_LEFT_RIGHT)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                     "_flipX" + image_container.extension)

    def flip_y(self, image_source, chance=1):
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = image_container.image.transpose(Image.FLIP_TOP_BOTTOM)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                    "_flipY" + image_container.extension)

    def rotate_90(self, image_source, chance=1):
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = image_container.image.transpose(Image.ROTATE_90)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                     "_rotate90" + image_container.extension)

    def rotate_180(self, image_source, chance=1):
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = image_container.image.transpose(Image.ROTATE_180)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                     "_rotate180" + image_container.extension)

    def rotate_270(self, image_source, chance=1):
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = image_container.image.transpose(Image.ROTATE_270)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                     "_rotate270" + image_container.extension)

    def resize(self, image_source, height, width, chance=1):
        if width == 0 or height == 0:
            return
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = image_container.image.resize((width,height), Image.ANTIALIAS)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                     "_resize" + image_container.extension)

    def scale(self, image_source, height, width, chance=1):
        if width == 0 or height == 0:
            return
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = ImageOps.fit(image_container.image, (width, height), Image.ANTIALIAS)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                    "_scale" + image_container.extension)

    def rotate(self, image_source, degree, chance=1):
        if degree < 0:
            return
        for image_container in image_source.list_of_images:
            if calc_chance(chance):
                generated_image = image_container.image.rotate(degree)
                generated_image.save(image_container.directory+'/' + image_container.filename +
                                     "_rotate" + str(degree) + image_container.extension)

    def convert_grayscale(self, image_source, chance=1):
        for image_container in image_source.list_of_images:
            generated_image = image_container.image.convert('L')
            generated_image.save(image_container.directory+'/' + image_container.filename +
                                "_grayscale" + image_container.extension)

    def crop(self, image_source, height, width, chance=1):
        if height <= 0 or width <= 0:
            return
        for image_container in image_source:
            org_width, org_height = image_container.image.size
            if org_height <= height or org_width <= width:
                return
            y_start = random.randint(0, org_height-height)
            x_start = random.randint(0, org_width-width)
            generated_image = image_container.image.crop((x_start, y_start, x_start+width, y_start+height))
            generated_image.save(generated_image.directory+'/' + image_container.filename + '_crop' +
                                 str(width) + str(height) + image_container.extension)
