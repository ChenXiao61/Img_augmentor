# Augmentor

[![Documentation Status](https://readthedocs.org/projects/augmentor/badge/?version=latest)](http://augmentor.readthedocs.io/en/latest/?badge=latest) [![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md) [![Project Status: WIP - Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip) [![PyPI](https://img.shields.io/badge/pypi-v0.1.1-blue.svg?maxAge=2592000)](https://pypi.python.org/pypi/Augmentor) [![Supported Python Versions](https://img.shields.io/badge/python-2.7%2C%203.3--3.6-orange.svg)](https://pypi.python.org/pypi/Augmentor)

Image augmentation library in Python for machine learning. A Julia version of the package is also being developed as a sister project and is available [here](https://github.com/Evizero/Augmentor.jl).

## Installation

Install using `pip` from the command line:

```python
pip install Augmentor
```

See the documentation for building from source.

## Documentation

Complete documentation can be found on Read the Docs: <http://augmentor.readthedocs.io/>

## Quick Start Guide and Usage
The purpose of _Augmentor_ is to automate image augmentation (artificial data generation) in order to expand datasets as input for machine learning algorithms, especially neural networks and deep learning.

The package works by building an augmentation **pipeline** where you define a series of operations to perform on a set of images. Operations, such as rotations or transforms, are added one by one to create an augmentation pipeline: when complete, the pipeline can be executed and an augmented dataset is created.

To begin, instantiate a `Pipeline` object that points to a directory on your file system:

```python
import Augmentor
p = Augmentor.Pipeline("/path/to/images")
```

You can then add operations to the Pipeline object `p` as follows:

```python
p.rotate(probability=0.7, max_left=10, max_right=10)
p.zoom(probability=0.5, min_scale=1.1, max_scale=1.5)
```

Every function requires you to specify a probability, which is used to decide if an operation is applied to an image as it is passed through the augmentation pipeline.

Once you have created a pipeline, you can sample from it like so:

```python
p.sample(10000)
```

which will generate 10,000 augmented images based on your specifications. By default these will be written to the disk in a directory named `output` relative to the path specified when initialising the `p` pipeline object above.

## Example

Let's perform an augmentation task on a single image, demonstrating the pipeline and several features of Augmentor.

First import the package and intialise a Pipeline object by pointing it to a directory containing your images:

```python
import Augmentor

p = Augmentor.Pipeline("/home/user/augmentor_data_tests")
```

This will output some inforation about what the images contained in this directory:

```
Initialised with 1 image(s) found in selected directory.
Output directory set to /home/user/augmentor_data_tests/output.
```

Now you can begin adding operations to the pipeline object:

```python
p.rotate90(probability=0.5)
p.rotate270(probability=0.5)
p.flip_left_right(probability=0.8)
p.flip_top_bottom(probability=0.3)
p.crop_random(probability=1, percentage_area=0.5)
p.resize(probability=1.0, width=120, height=120)
```

Once you have added the operations you require, you can sample images from this pipeline:

```python
p.sample(100)
```

A progress bar provides information about the status of the sampling:

```
Processing ISIC_0000000.jpg: 100%|***************| 100/100 [235.08 Samples/s]
```

Some sample output:

| Input Image<sup>[1]</sup>                                                                                          |   | Augmented Images                                                                                      |
|-------------------------------------------------------------------------------------------------------|---|-------------------------------------------------------------------------------------------------------|
| ![Original](https://cloud.githubusercontent.com/assets/16042756/23019262/b696e3a6-f441-11e6-958d-17f18f2cd35e.jpg) | → | ![Augmented](https://cloud.githubusercontent.com/assets/16042756/23018832/cda6967e-f43f-11e6-9082-765c291f1fd6.gif) |

The augmented images may be useful for a boundary detection task, for example.

## Elastic Distortions

Using elastic distortions, one image can be used to generate many images that are real-world feasible and label preserving:

| Input Image                                                                                                                       |   | Augmented Images                                                                                                        |
|-----------------------------------------------------------------------------------------------------------------------------------|---|-------------------------------------------------------------------------------------------------------------------------|
| ![eight_hand_drawn_border](https://cloud.githubusercontent.com/assets/16042756/23697279/79850d52-03e7-11e7-9445-475316b702a3.png) | → | ![eights_border](https://cloud.githubusercontent.com/assets/16042756/23697283/802698a6-03e7-11e7-94b7-f0b61977ef33.gif) |

The input image has a 1 pixel black border to emphasise that only the interior of the image is being distorted.

## Licence and Acknowledgements

Augmentor is made available under the terms of the MIT Licence. See [`Licence.md`](https://github.com/mdbloice/Augmentor/blob/master/LICENSE.md).

[1] Skin lesion image obtained from the ISIC Archive:

- Image id = 5436e3abbae478396759f0cf
- Download: <https://isic-archive.com:443/api/v1/image/5436e3abbae478396759f0cf/download>

You can use `urllib` to obtain the image in order to reproduce the augmented images above:

```python
In [1]: import urllib
In [2]: im_url = "https://isic-archive.com:443/api/v1/image/5436e3abbae478396759f0cf/download"
In [3]: urllib.urlretrieve(im_url, "ISIC_0000000.jpg")
Out[3]: ('ISIC_0000000.jpg', <httplib.HTTPMessage instance at 0x7f7bd949a950>)
```

## Asciicast

Click the preview below to view a video demonstration of Augmentor in use:

[![asciicast](https://asciinema.org/a/105368.png)](https://asciinema.org/a/105368?autoplay=1&speed=3)
