from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import Augmentor
import tempfile
import io
import shutil
import glob
import random
import numpy as np

from PIL import Image

from Augmentor import ImageUtilities

def test_keras_generator_from_disk():

    batch_size = random.randint(1, 50)
    width = 80
    height = 80

    tmpdir = tempfile.mkdtemp()
    tmps = []

    for i in range(10):
        tmps.append(tempfile.NamedTemporaryFile(dir=tmpdir, suffix='.JPEG'))

        bytestream = io.BytesIO()

        im = Image.new('RGB', (width, height))
        im.save(bytestream, 'JPEG')

        tmps[i].file.write(bytestream.getvalue())
        tmps[i].flush()

    p = Augmentor.Pipeline(tmpdir)
    assert len(p.augmentor_images) == len(tmps)

    p.rotate(probability=0.5, max_left_rotation=5, max_right_rotation=5)
    p.flip_left_right(probability=0.333)
    p.flip_top_bottom(probability=0.5)

    g = p.keras_generator(batch_size=batch_size, image_data_format="channels_last")

    X, y = next(g)

    assert len(X) == batch_size
    assert len(X) == batch_size
    assert len(X) == len(y)

    assert np.shape(X) == (batch_size, width, height, 3)

    # Call next() more than the total number of images in the pipeline
    for i in range(20):
        X, y = next(g)
        assert len(X) == batch_size
        assert len(X) == batch_size
        assert len(X) == len(y)
        assert np.shape(X) == (batch_size, width, height, 3)

    g2 = p.keras_generator(batch_size=batch_size, image_data_format="channels_first")

    X2, y2 = next(g2)

    assert len(X2) == batch_size
    assert len(X2) == batch_size
    assert len(X2) == len(y2)

    assert np.shape(X2) == (batch_size, 3, width, height)

    # Close all temporary files which will also delete them automatically
    for i in range(len(tmps)):
        tmps[i].close()

    # Finally remove the directory (and everything in it) as mkdtemp does
    # not delete itself after closing automatically
    shutil.rmtree(tmpdir)


def test_generator_with_array_data():

    batch_size = random.randint(1, 100)
    width = 800
    height = 800

    image_matrix = np.zeros((100, width, height, 3), dtype='uint8')
    labels = np.zeros(100)

    p = Augmentor.Pipeline()
    p.rotate(probability=1, max_right_rotation=10, max_left_rotation=10)

    g = p.keras_generator_from_array(image_matrix, labels, batch_size=batch_size)

    X, y = next(g)

    assert len(X) == batch_size
    assert len(y) == batch_size

    for i in range(len(y)):
        assert y[i] == 0

    for i in range(len(X)):
        im_pil = Image.fromarray(X[i])
        assert im_pil is not None

    image_matrix_2d = np.zeros((100, width, height), dtype='uint8')
    labels_2d = np.zeros(100)

    p2 = Augmentor.Pipeline()
    p2.rotate(probability=0.1, max_left_rotation=5, max_right_rotation=5)

    g2 = p2.keras_generator_from_array(image_matrix_2d, labels_2d, batch_size=batch_size)

    X2, y2 = next(g2)

    assert len(X2) == batch_size
    assert len(y2) == batch_size

    for i in range(len(y2)):
        assert y2[i] == 0

    for i in range(len(X2)):
        im_pil = Image.fromarray(X2[i].reshape(width, height))
        assert im_pil is not None
