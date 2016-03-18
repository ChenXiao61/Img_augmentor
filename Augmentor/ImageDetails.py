import os

class ImageDetails(object):
    
    def __init__(self, image, fullpath, filename, extension, dimensions)
    
    self.image = image
    self.fullpath = os.path.abspath(image)
    self.filename = os.path.splitext(filename)[0]
    self.extension = os.path.splitext(filename)[1]
    self.dimensions = (image.x, image.y)