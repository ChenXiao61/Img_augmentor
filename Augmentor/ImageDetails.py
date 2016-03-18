import os 
# Perhaps put all imports in __init__.py
# Because I am not sure if this is where imports go for classes.


class ImageDetails(object):
    
    def __init__(self, image, fullpath, filename, extension, dimensions)
    
    self.image = image
    self.fullpath = os.path.abspath(image)
    self.filename = os.path.splitext(filename)[0]
    self.extension = os.path.splitext(filename)[1]
    self.dimensions = (image.x, image.y)