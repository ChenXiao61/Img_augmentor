# Augmentor

[![Documentation Status](https://readthedocs.org/projects/augmentor/badge/?version=master)](http://augmentor.readthedocs.io/en/master/?badge=master) [![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md) [![Project Status: WIP - Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip) [![PyPI](https://img.shields.io/badge/pypi-v0.1-blue.svg?maxAge=2592000)](https://pypi.python.org/pypi/Augmentor) [![Supported Python Versions](https://img.shields.io/badge/python-2.6--2.7%2C%203.3--3.5-orange.svg)](https://pypi.python.org/pypi/Augmentor)

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
