from Augmentor import Pipeline
from Augmentor import Image

# These are the possibilities to create a pipeline:
# set the path to the folder with images to manipulate
pathToOneImage = 'path/to/image'

# Example of how to hand over images to the pipeline.
# Details on creating an image with pillow see: http://pillow.readthedocs.org/en/3.1.x/reference/Image.html
im1 = Image.open('path/to/image1')
im2 = Image.open('path/to/image2')
# Specifying a list of images with image paths
listOfImagePaths = ['path/to/image1', 'path/to/image2']
# Specifying a list of images with PIL Images
listOfImages = [im1, im2]
# Specifying a path to one image
pathToImages = 'path/to/source'
# create pipeline
pipe = Pipeline.Pipeline(listOfImagePaths)

# add functions to pipeline
pipe.addFlipY()
pipe.addFlipX(1)
# add another function to pipeline
pipe.addCrop(45, 45)

# print a summary
pipe.summary()
pipe.image_source.summary()

# execute the functions in pipline
pipe.execute()
