from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from PIL import Image
import os


class ImageDetails(object):
    def __init__(self, image, filename):
        self.image = None
        self.fullpath = filename
        self.filename = os.path.basename(os.path.splitext(filename)[0])
        self.extension = os.path.splitext(filename)[1]
        self.directory = os.path.dirname(filename)
        self.mode = image.mode
        (self.dimensions) = image.size

    def populateImage(self):
        self.image = Image.open(self.fullpath)
        return self.image

    def clear_image(self):
        self.image = None
