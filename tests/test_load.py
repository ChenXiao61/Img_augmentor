import pytest

# Context
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import Augmentor
import tempfile
import io
import shutil
from PIL import Image


def test_initialise_with_no_parameters():
    p = Augmentor.Pipeline()
    assert len(p.augmentor_images) == 0


def test_initialise_with_ten_images():

    tmpdir = tempfile.mkdtemp()
    tmps = []

    for i in range(10):
        tmps.append(tempfile.NamedTemporaryFile(dir=tmpdir, suffix='.JPEG'))

        bytestream = io.BytesIO()

        im = Image.new('RGB', (800,800))
        im.save(bytestream, 'JPEG')

        tmps[i].file.write(bytestream.getvalue())
        tmps[i].flush()

    p = Augmentor.Pipeline(tmpdir)
    assert len(p.augmentor_images) == len(tmps)

    for i in range(len(tmps)):
        tmps[i].close()

    # finally remove the directory, and everything in it
    shutil.rmtree(tmpdir)
