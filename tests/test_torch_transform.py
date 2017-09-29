import pytest

# Context
import numpy as np
import PIL.Image as Image

import Augmentor

def test_torch_transform():
    torchvision = pytest.importorskip("torchvision")

    red = np.zeros([10, 10, 3], np.uint8)
    red[..., 0] = 255
    red = Image.fromarray(red)

    g = Augmentor.Operations.Greyscale(1)

    p = Augmentor.Pipeline()
    p.greyscale(1)
    transforms = torchvision.transforms.Compose([
        p.torch_transform()
    ])

    assert red != transforms(red)
    assert g.perform_operation(red) == transforms(red)
