class ImageFormat(object):
    def __init__(self):
        self.format_dict = {'1': 'Black White', 'L': 'Grayscale', 'P': 'Palette', "RGB": "RGB",
                            'RGBA': 'RGB with Transparency', 'CMYK': 'CMYK', 'YCbCr': 'YCbCr', 'LAB': 'LAB',
                            'HSV': 'HSV', 'I': 'Integer Pixels', 'F': 'Float Pixels'}

    def get_format_printable(self, mode):
        return self.format_dict[mode]
