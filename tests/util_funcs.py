import os
import sys
import tempfile
import io
import shutil

from PIL import Image

def create_temp_JPEG(size):
    tmpdir = tempfile.mkdtemp()
    tmp = tempfile.NamedTemporaryFile(dir=tmpdir, suffix='.JPEG')
    im = Image.new('RGB', size)
    im.save(tmp.name, 'JPEG')

    return tmp, tmpdir
