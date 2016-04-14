import os


# Perhaps put all imports in __init__.py
# Because I am not sure if this is where imports go for classes.


class ImageDetails(object):
    def __init__(self, image, filename):
        self.image = image
        self.fullpath = filename
        self.filename = os.path.basename(os.path.splitext(filename)[0])
        self.extension = os.path.splitext(filename)[1]
        self.directory = os.path.dirname(filename)
        (self.dimensions) = image.size
