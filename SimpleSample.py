from Augmentor import Pipeline
from Augmentor import Image

# These are the possibilities to create a pipeline:
# set the path to the folder with images to manipulate
# pathToOneImage = 'path/to/image'

# Example of how to hand over images to the pipeline.
# Details on creating an image with pillow see: http://pillow.readthedocs.org/en/3.1.x/reference/Image.html
# im1 = Image.open('path/to/image1')
# im2 = Image.open('path/to/image2')
# Specifying a list of images with image paths
# listOfImagePaths = ['path/to/image1', 'path/to/image2']
# Specifying a list of images with PIL Images
# listOfImages = [im1, im2]
# Specifying a path to one image


pathToImages = 'C:/Users/Jonny/Pictures/Camera Roll'
# create pipeline
pipe = Pipeline.Pipeline(pathToImages)

# add functions to pipeline
pipe.addFlipX()
pipe.addFlipY(1)
# add another function to pipeline
pipe.addCrop(45, 45)
pipe.addRotate90()
pipe.addRotate180()
pipe.addRotate270()
pipe.addResize(100, 100)
pipe.addScale(50, 50)
pipe.addRotate(25)
pipe.addConvertGrayscale()

# print a summary
# pipe.summary()
# pipe.image_source.summary()

# execute the functions in pipline
# pipe.image_source.summary()

# list where augmented images are stored
# if a number of chunks is specified, the chunks will be appended
augmented_images = []

try:
    # loop until all images processed
    while 1:
        # execute() -> process all images at once and store them in the on disk
        # execute(number_of_images) -> process in patches and store them on disk
        # execute(storage_location=augmented_images) -> process all images at once and store them in the given list
        # execute(number_of_images, storage_location=augmented_images) -> process all images in patches and store them in the given list

        pipe.execute(storage_location=augmented_images)

except pipe.ProgramFinishedException as e:
    print(str(e))
# show the augmented images
Image.open(augmented_images[0]).show()
Image.open(augmented_images[1]).show()
Image.open(augmented_images[2]).show()
# and so on

# close used memory
pipe.clean_up(augmented_images)
