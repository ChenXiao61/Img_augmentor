# Augmentor

[![Documentation Status](https://readthedocs.org/projects/augmentor/badge/?version=latest)](http://augmentor.readthedocs.io/en/latest/?badge=latest) [![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md) [![Project Status: WIP - Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip) [![PyPI](https://img.shields.io/badge/pypi-v0.1-blue.svg?maxAge=2592000)](https://pypi.python.org/pypi/Augmentor) [![Supported Python Versions](https://img.shields.io/badge/python-2.6--2.7%2C%203.3--3.5-orange.svg)](https://pypi.python.org/pypi/Augmentor)

Image augmentation library in Python for machine learning. A Julia version of the package is also being developed as a sister project and is available [here](https://github.com/Evizero/Augmentor.jl).

## Documentation

Complete documentation can be found on Read the Docs: <http://augmentor.readthedocs.io/>

## Installation

Currently, the PyPI version is out of date. Therefore it is currently recommended that you clone the package and install it manually.

```
git clone https://github.com/mdbloice/Augmentor.git
```

Enter the newly created `Augmentor` directory and build the package:

```
cd Augmentor
python setup.py install
```

Installing via `pip` and PyPI will be restored in a future version.

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

Let's perform an augmentation task on a single image, demonstrating the pipeline and several features of Augmentor:

```python
In [1]: import Augmentor

In [2]: p = Augmentor.Pipeline("/home/user/augmentor_data_tests")
Initialised with 1 images found in selected directory.
Output directory set to /home/user/Documents/augmentor_data_tests/output.

In [3]: p.rotate90(probability=0.5)

In [4]: p.rotate270(probability=0.5)

In [5]: p.flip_left_right(probability=0.8)

In [6]: p.flip_top_bottom(probability=0.3)

In [7]: p.crop_random(probability=1, percentage_area=0.5)

In [8]: p.resize(probability=1.0, width=120, height=120)

In [9]: p.sample(100)
Processing ISIC_0000000.jpg: 100%|██████████████████| 100/100 [00:01<00:00, 235.08 Samples/s]
```

Some sample output:

| Input Image                                                                                           | Augmented Images                                                                                      |
|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| ![Original](https://cloud.githubusercontent.com/assets/16042756/23019262/b696e3a6-f441-11e6-958d-17f18f2cd35e.jpg) | ![Augmented](https://cloud.githubusercontent.com/assets/16042756/23018832/cda6967e-f43f-11e6-9082-765c291f1fd6.gif) |

The augmented images may be useful for a region detection task, for example.

## Licence and Acknowledgements

Augmentor is made available under the terms of the MIT Licence. See [`Licence.md`] (https://github.com/mdbloice/Augmentor/blob/master/LICENSE.md).

Image obtained from the ISIC Archive:

- Image id = 5436e3abbae478396759f0cf
- Download: <https://isic-archive.com:443/api/v1/image/5436e3abbae478396759f0cf/download>

You can use `urllib` to obtain the image in order to reproduce the augmented images above:

```python
In [1]: import urllib
In [2]: urllib.urlretrieve("https://isic-archive.com:443/api/v1/image/5436e3abbae478396759f0cf/download", "ISIC_0000000.jpg")
Out[2]: ('ISIC_0000000.jpg', <httplib.HTTPMessage instance at 0x7f7bd949a950>)
```
