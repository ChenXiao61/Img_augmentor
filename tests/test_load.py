import pytest

# Context
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import Augmentor


def test_initialise_with_no_parameters():
    p = Augmentor.Pipeline()
    assert len(p.augmentor_images) == 0
