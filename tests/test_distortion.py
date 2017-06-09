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

from util_funcs import create_temp_JPEG

def test_in_memory_distortions():
    tmp, tmpdir = create_temp_JPEG((800, 800))

    assert tmp is not None
    assert tmpdir is not None

    tmp.close()
    shutil.rmtree(tmpdir)
