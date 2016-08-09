from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
class ImageFormat(object):
    def __init__(self):
        self.format_dict = {'1': 'Black White', 'L': 'Grayscale', 'P': 'Palette', "RGB": "RGB",
                            'RGBA': 'RGB with Transparency', 'CMYK': 'CMYK', 'YCbCr': 'YCbCr', 'LAB': 'LAB',
                            'HSV': 'HSV', 'I': 'Integer Pixels', 'F': 'Float Pixels'}

    def get_format_printable(self, mode):
        return self.format_dict[mode]
