# Augmentor
Image augmentation library in Python for Machine Learning practioners. 

## Usage
The package works by building an augmentation pipeline as a series of operations to perform on a set of images. Operations, such as rotations or transforms, are added piece by piece in order to create an augmentation pipeline, which can then be executed in order to create an augmented dataset.

The package currently consists of two basic building blocks that allow for a pipeline to be built, the `ImageSource` class and the `Pipeline` class.

You start by initialising an `ImageSource` object where you define the source of your images. Then you define a `Pipeline` object that defines what operations you wish to perform on your dataset (defined in your `ImageSource` object).

### `ImageSource`
Defines the source directory or directories where your original images are stored. 

### `Pipeine`
Defines the operations (rotations, mirroring, tranforms, etc.) which should be applied to your original dataset. Once a pipeline has been built, the `execute()` method applies the operations to your images.

## Installation
__Not yet implemented.__

```bash
# This is not yet implemented.
pip install Augmentor
```
