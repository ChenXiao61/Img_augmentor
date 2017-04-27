Main Features
=============

In this section we will describe the main features of Augmentor with example code and output.

All functions described here are made available by the Pipeline object. Create a new Pipeline object by instantiating it with a path to a set of images or image that you wish to augment:

.. code-block:: python

    >>> import Augmentor
    >>> p = Augmentor.Pipeline("/path/to/images")
    Initialised with 100 images found in selected directory.

You can now add operations to this pipeline using the ``p`` Pipeline object. For example, to add a rotate operation:

.. code-block:: python

    >>> p.rotate(probability=1.0, max_left_rotation=5, max_right_rotation=10)

All pipeline operations have at least a probability parameter. 

To see the status of the current pipeline:

.. code-block:: python

    >>> p.status()
    There are 1 operation(s) in the current pipeline.
    Index 0:
        Operation RotateRange (probability: 1):
	        Attribute: max_right_rotation (10)
	        Attribute: max_left_rotation (-5)
	        Attribute: probability (1)

    There are 1 image(s) in the source directory.
    Dimensions:
	    Width: 400 Height: 400
    Formats:
	    PNG

You can remove operations using the ``remove_operation(index)`` function and the appropriate ``index`` indicator from above.

Perspective Skewing
-------------------

Perspective skewing involves transforming the image so that it appears that you are looking at the image from a different angle.

The following main functions are used for skewing:

- ``skew_tilt()``
- ``skew_left_right()``
- ``skew_top_bottom()``
- ``skew_corner()``
- ``skew()``

To skew or tilt an image either left, right, forwards, or backwards, use the ``skew_tilt`` function. The image will be skewed by a random amount in the following directions:

+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Skew Tilt Left                                                                                        | Skew Tilt Right                                                                                        | Skew Tilt Forward                                                                                        | Skew Tilt Backward                                                                                        |
+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/TiltLeft_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/TiltRight_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/TiltForward_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/TilfBackward_s.png |
+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+

Or, to skew an image by a random corner, use the ``skew_corner()`` function. The image will be skewed using one of the following 8 skew types:

+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+
| Skew Type 0                                                                                          | Skew Type 1                                                                                          | Skew Type 2                                                                                          | Skew Type 3                                                                                          |
+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+
| .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner0_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner1_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner2_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner3_s.png |
+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+
| Skew Type 4                                                                                          | Skew Type 5                                                                                          | Skew Type 6                                                                                          | Skew Type 7                                                                                          |
+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+
| .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner4_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner5_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner6_s.png | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/Corner7_s.png |
+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+

If you only wish to skew either left or right, use ``skew_left_right()``. To skew only forwards or backwards, use ``skew_top_bottom()``. 

The function ``skew()`` will skew your image in a random direction of the 12 directions shown above.

Rotating
--------

Rotating can be performed in a number of ways. When rotating by modulo 90, the image is simply rotated and saved. To rotate by arbitrary degrees, then a crop is taken from the centre of the newly rotated image. 

Rotate functions that are available are:

- ``rotate()``
- ``rotate90()``
- ``rotate180()``
- ``rotate270()``
- ``rotate_random_90()``

The ``rotate()`` warrants more discussion and will be desribed here. When an image is rotated,

The ``rotate_random_90()`` function will rotate the image by either 90, 180, or 270 degrees. 

+-----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| Original Image                                                                                            | Rotated 10 degrees                                                                                          |
+-----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/ISIC_0000017_s.jpg | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/ISIC_0000017_r_s.jpg |
+-----------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+

As can be seen above, an arbitrary, non-modulo 90, rotation will unfortunately result in the image being padded in each corner. To allieviate this, Augmentor's default behaviour is to crop the image and retain the largest drop possible while maintaining the image's aspect ratio:

+-----------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
| Original Image                                                                                            | Rotated 10 degrees, cropped                                                                                              |
+-----------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+
| .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/ISIC_0000017_s.jpg | .. image:: https://raw.githubusercontent.com/mdbloice/AugmentorFiles/master/UsageGuide/ISIC_0000017_r_aug_s.jpg          |
+-----------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------+

This will, of course, result in the image being zoomed in. For smaller rotations of between -5 and 5 degrees, this zoom effect is not particularly drastic.

Cropping
--------

Cropping functions which are available are:

- 







