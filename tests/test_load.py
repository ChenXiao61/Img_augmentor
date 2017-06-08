import pytest

# Context
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# Imports
import Augmentor
import tempfile
import io
import shutil
from PIL import Image


def test_initialise_with_no_parameters():
    p = Augmentor.Pipeline()
    assert len(p.augmentor_images) == 0
    assert isinstance(p, Augmentor.Pipeline)


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

    # Check if we can re-read all these images using PIL.
    # This will fail for Windows, as you cannot open a file that is already open.
    if os.name != "nt":
        for i in range(len(tmps)):
            im = Image.open(p.augmentor_images[i].image_path)
            assert im is not None

    # Check if the paths found during the scan are exactly the paths
    # stored by Augmentor after initialisation
    for i in range(len(tmps)):
        p_paths = [x.image_path for x in p.augmentor_images]
        assert tmps[i].name in p_paths

    # Check if all the paths stored by the Pipeline object
    # actually exist and are valid paths
    for i in range(len(tmps)):
        assert os.path.exists(p.augmentor_images[i].image_path)

    # Close all temporary files which will also delete them automatically
    for i in range(len(tmps)):
        tmps[i].close()

    # Finally remove the directory (and everything in it) as mkdtemp does
    # not delete itself after closing automatically
    shutil.rmtree(tmpdir)
