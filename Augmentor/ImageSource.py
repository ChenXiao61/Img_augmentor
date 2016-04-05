from Augmentor import glob
from Augmentor import ImageDetails
from Augmentor import Image
from Augmentor import AsciiTable


class ImageSource(object):

    def __init__(self, root_path='.'):
        self.root_path = root_path
        self.list_of_images = []
        self.file_extension = ('jpg', 'jpeg', 'png', 'bmp')
        self.scan(root_path)

    def scan(self, path_to_scan):
        #for root, subdirs, list_of_files in os.walk(path_to_scan):
        list_of_files = []
        for type in self.file_extension:
            list_of_files.extend(glob.glob(path_to_scan + '/**/*.' + type, recursive=True))

        for file in list_of_files:
            image = Image.open(file)
            self.list_of_images.append(ImageDetails.ImageDetails(image, file))

    def summary(self):
        table_data = [
        ['ImageSource Summary:'],
        [str(len(self.list_of_images)) + ' images found'],
        ['TODO: Print additional information'],
        ]
        table = AsciiTable(table_data)
        print(table.table)