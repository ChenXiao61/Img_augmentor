# Augmentor

[![Documentation Status](https://readthedocs.org/projects/augmentor/badge/?version=master)](http://augmentor.readthedocs.io/en/master/?badge=master) [![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md) [![Project Status: WIP - Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip) [![PyPI](https://img.shields.io/badge/pypi-v0.1-blue.svg?maxAge=2592000)](https://pypi.python.org/pypi/Augmentor) [![Supported Python Versions](https://img.shields.io/badge/python-2.6--2.7%2C%203.3--3.5-orange.svg)

Image augmentation library in Python for machine learning. A Julia version of the package is also being developed as a sister project and is available [here](https://github.com/Evizero/Augmentor.jl).

## Documentation

Complete documentation can be found on Read the Docs: <http://augmentor.readthedocs.io/>

## Quick Start Guide and Usage
The purpose of _Augmentor_ is to automate image augmentation (artificial data generation) in order to expand datasets as input for machine learning algorithms, especially neural networks and deep learning.

The package works by building an augmentation pipeline by defining a series of operations to perform on a set of images. Operations, such as rotations or transforms, are added piece by piece in order to create an augmentation pipeline: when complete, the pipeline is executed and an augmented dataset is created.

The package currently consists of two basic building blocks that allow for a pipeline to be built, the `ImageSource` class and the `Pipeline` class.

You start by initialising an `ImageSource` object where you define the source of your images. You then create a `Pipeline` object where you define which operations you wish to perform on your dataset.

## Installation
Install via pip:
```python
pip install Augmentor
```

## Usage
A an example can be found in [`Examples.py`](https://github.com/mdbloice/Augmentor/blob/master/Examples.py). This file includes exampeles of creating and importing images, adding image manipulations to a pipeline, executing the operations and saving them.

There are several ways how to import and export images into the program.

###Import images and create Pipeline
Images can be imported by adding a directory, a filename or by adding an image or a list of images to the pipeline.
####Adding a directory and create Pipeline
```python
pathToImages = 'C:/path/to/images'
# create pipeline
pipe = Pipeline.Pipeline(pathToImages)
```
####Adding a filename and create Pipeline
```python
pathToImage = 'C:/path/to/images/image.jpeg'
# create pipeline
pipe = Pipeline.Pipeline(pathToImage)
```
####Adding a list of filenames and create Pipeline
```python
image1 = 'C:/path/to/images/image1.jpeg'
image2 = 'C:/path/to/images/image2.jpeg'
# create pipeline
pipe = Pipeline.Pipeline([image1, image2])
```
####Adding a list of images and create Pipeline
There for images have to be created with pillow for details visit: http://pillow.readthedocs.org/en/3.1.x/reference/Image.html

```python
image1 = Image.open('C:/path/to/images/image1.jpeg')
image2 = Image.open('C:/path/to/images/image2.jpeg')
# create pipeline
pipe = Pipeline.Pipeline([image1, image2])
```

####Adding a single image and create Pipeline
There for images have to be created with pillow for details visit: http://pillow.readthedocs.org/en/3.1.x/reference/Image.html

```python
image = Image.open('C:/path/to/images/image.jpeg')
# create pipeline
pipe = Pipeline.Pipeline(image1)
```

###Add Operations to the pipeline
More details on possible operations and their usage can be found in the *Pipeline* section.
```python
# add addFlipY operation to the pipeline
pipe.addFlipY(1)
# add addCrop operation to the pipeline
pipe.addCrop(45, 45)
# add addRotatet90 operation to the pipeline
pipe.addRotate90()
```

###Execute operations and Export images
Created images can either by directly saved or returned as list of image objects.

####Execute all images at once and save on disk

```python
try:
    pipe.execute()
except pipe.ProgramFinishedException as e:
    print(str(e))
```
####Execute a patch of images in patches and save on disk

```python
number_of_images = 12
try:
    pipe.execute(number_of_images)
except pipe.ProgramFinishedException as e:
    print(str(e))
```

####Execute all images and save in given list
```python
augmented_images = []
try:
    pipe.execute(storage_location=augmented_images)
except pipe.ProgramFinishedException as e:
    print(str(e))
```

####Execute a patch of images in patches and save in given list
```python
number_of_images = 12
augmented_images = []
try:
    pipe.execute(number_of_images, storage_location=augmented_images)
except pipe.ProgramFinishedException as e:
    print(str(e))
```

###Clean used memory
To clean the saved images after processing.
```python
pipe.clean_up(augmented_images)
```

### The `ImageDetails` Class
A container which comprises images, paths, and other necessary information about the data it is pointing to.

### The `ImageOperations` Class
Includes mainly the different image operations and therefore the main functionality.

### The `Pipeline` Class
Defines the operations (rotations, mirroring, transforms, etc.) which should be applied to your original dataset. Once a pipeline has been built, the `execute()` method applies the operations to your images.
The currently implemented image manipulation functions are:

####General remarks
Where chance is available, this parameter adds the possibility of how likely an image will be modified/generated. If nothing is specified the probability of 1 will be used.

####Flip
To flip an image one can choose between two functions. The function ` addFlipX` will flip an image along its x-axis and `addFlipY` will flip an image along its y-axis.
```python
addFlipX(chance=1)
addFlipY(chance=1)
```

####Rotate
To rotate an image on can choose between 4 functions, while for the first 3 functions the degrees are fixed with 90, 180 and 270 degrees. While for addRotate the degrees have to be specified with the degree-Parameter
```python
addRotate90(chance=1)
addRotate180(chance=1)
addRotate270(chance=1)
addRotate(degree, chance=1)
```

####Resize
To create a resized image call the addResize functions. It expects the height and the width as parameters. Both should be given as px-values.
```python
addResize(height, width, chance=1)
addScale(height, width, chance=1)
addCrop(height, width, chance=1)
```
It is also possible to creat cropped and scaled images. Both - addScale and addCrop - expect the same parameters as addResize.

####Grayscale
To convert an image into grayscale use the following function:
```python
addConvertGrayscale(chance=1)
```

####Summary
Use summary() to print a summary which includes the number of functions which will be executed as well as how many images likely will be generated to console.
```python
summary()
```

####ProgramFinishedException
This exceptions signals that the program is finished. Therefore it can be used for while-loops. In _SimpleSample.py_as well as in the _Execute operations and Export images_ section below  examples can be found of how to work with this exception.

### The `ImageSource` Class
Defines the source directory or directories where your original images are stored.

```python
summary()
```
