import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from PIL import Image
from Augmentor import Operations


def test_rotate_images(tmpdir):

    original_dimensions = (800, 800)

    im_tmp = tmpdir.mkdir("subfolder").join('test.JPEG')
    im = Image.new('RGB', original_dimensions)
    im.save(str(im_tmp), 'JPEG')

    r = Operations.Rotate(probability=1, rotation=90)
    im_r = r.perform_operation(im)

    assert im_r is not None
    assert im_r.size == original_dimensions


import tempfile
import shutil


def test_rotate_images_custom_temp_files():

    original_dimensions = (800, 800)

    tmpdir = tempfile.mkdtemp()
    tmp = tempfile.NamedTemporaryFile(dir=tmpdir, suffix='.JPEG')
    im = Image.new('RGB', original_dimensions)
    im.save(tmp.name, 'JPEG')

    r = Operations.Rotate(probability=1, rotation=90)
    im_r = r.perform_operation(im)

    assert im_r is not None
    assert im_r.size == original_dimensions

    tmp.close()
    shutil.rmtree(tmpdir)
