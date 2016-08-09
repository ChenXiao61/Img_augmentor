from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import next
from builtins import str
from future import standard_library
standard_library.install_aliases()
from Augmentor import glob
from Augmentor import ImageDetails
from Augmentor import ImageFormat
from Augmentor import Image
from Augmentor import GithubFlavoredMarkdownTable
from Augmentor import gcd
from Augmentor import ProgramFinishedException
import os


class ImageSource(object):
    def __init__(self, root_path):
        self.root_path = root_path
        self.list_of_images = []
        self.image_source_slice = None
        self.processed_images = 0
        self.file_extension = ('jpg', 'jpeg', 'png', 'bmp')
        self.dimensions = {}
        self.image_format = ImageFormat.ImageFormat()
        self.scan(root_path)
        self.image_iterator = iter(self.list_of_images)
        if len(self.list_of_images) == 0:
            raise ProgramFinishedException.ProgramFinishedException("Image repository is empty.")

    def scan(self, path_to_scan):
        # for root, subdirs, list_of_files in os.walk(path_to_scan):
        list_of_files = []

        if isinstance(path_to_scan, list):
            print("Processing list of images")
            # List of PIL images
            if all(isinstance(item, Image.Image) for item in path_to_scan):
                for file in path_to_scan:
                    print(file.filename)
                    self.list_of_images.append(ImageDetails.ImageDetails(file, file.filename))
                self.root_path = os.path.dirname(path_to_scan[0].filename)

            # List of images paths
            elif all(os.path.isfile(item) for item in path_to_scan):
                for file in path_to_scan:
                    image = Image.open(file)
                    self.list_of_images.append(ImageDetails.ImageDetails(image, file))
                    del image
                self.root_path = os.path.dirname(path_to_scan[0])
            else:
                raise ProgramFinishedException.ProgramFinishedException(
                    "List contains unsupported formats. Only list of PIL-images or list of direct paths supported!")

        elif isinstance(path_to_scan, Image.Image):
            print("Processing PIL image object")
            self.root_path = os.path.dirname(path_to_scan.filename)
            self.list_of_images.append(ImageDetails.ImageDetails(path_to_scan, path_to_scan.filename))

        elif any(extension in path_to_scan for extension in self.file_extension):
            print("Processing one image")
            self.root_path = os.path.dirname(path_to_scan)
            image = Image.open(path_to_scan)
            self.list_of_images.append(ImageDetails.ImageDetails(image, path_to_scan))
            del image

        elif os.path.isdir(path_to_scan):
            print("Processing directory")
            for extension in self.file_extension:
                list_of_files.extend(glob.glob(path_to_scan + '/**/*.' + extension, recursive=True))
            for file in list_of_files:
                image = Image.open(file)
                self.list_of_images.append(ImageDetails.ImageDetails(image, file))
                del image
        else:
            raise ProgramFinishedException.ProgramFinishedException(
                "Unsupported image source. Please have look at the documentation!")

    def populate_images(self):
        for image in self.list_of_images:
            image.populateImage()
        return 0

    def populate_one_image(self):
        try:
            image = next(self.image_iterator)
            image.populateImage()
            return image
        except StopIteration:
            return -1

    def setup_summary(self):
        for image in self.list_of_images:

            if image.dimensions in self.dimensions:
                self.dimensions[image.dimensions] += 1
            else:
                self.dimensions[image.dimensions] = 1

    def summary(self):
        self.setup_summary()
        file_types = self.process_filetypes()
        table_data = [
            ['ImageSource Summary:', ''],
            ['Image count', str(len(self.list_of_images))],
            ['Dimensions', self.process_dimensions()],
            ['Aspect ratio(s)', self.process_aspect_ratio()],
            ['File type(s)', file_types[1]],
            ['File extension(s)', file_types[0]],
            ['File format(s)', self.process_file_formats()[0]],
        ]
        table = GithubFlavoredMarkdownTable(table_data)
        print(table.table)

    def process_dimensions(self):
        result = ""
        for dimension in sorted(self.dimensions)[:2]:
            result += str(dimension[0]) + 'x' + str(dimension[1]) + '(' + str(self.dimensions.get(dimension)) + ')\n'

        if len(self.dimensions) > 2:
            result += 'and more...\n'

        return result[:-1]

    def process_file_formats(self):
        file_formats = {}
        for image in self.list_of_images:
            if image.mode not in file_formats:
                file_formats[image.mode] = self.image_format.get_format_printable(image.mode)

        return [str(', '.join(str(file_format) for file_format in file_formats.values())), str(len(file_formats))]

    def process_filetypes(self):
        file_types = []
        for image in self.list_of_images:
            if image.extension not in file_types:
                file_types.append(image.extension)

        return [str(', '.join(str(file_type[1:]) for file_type in file_types)), str(len(file_types))]

    def process_aspect_ratio(self):
        aspect_ratios = []
        for width, height in self.dimensions.keys():
            ratio = gcd(width, height)
            if [width // ratio, height // ratio] not in aspect_ratios:
                aspect_ratios.append([width // ratio, height // ratio])

        result = '\n'.join(str(ratio[0]) + ':' + str(ratio[1]) for ratio in aspect_ratios[:2])
        if len(aspect_ratios) > 2:
            result += '\nand more...'

        return result

    def process_list(self, list_of_images):
        if all(isinstance(item, Image.Image) for item in list_of_images):
            return
        elif all(os.path.isfile(item) for item in list_of_images):
            return
        else:
            raise ProgramFinishedException.ProgramFinishedException(
                "List contains unsupported formats. Only list of PIL-images or list of direct paths supported!")
