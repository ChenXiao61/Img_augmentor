Usage
=====

Here we describe the general usage of Augmentor. 

Getting Started
---------------

To use Augmentor, the following general procedure is followed:

1. You instantiate a ``Pipeline`` object pointing to a directory containing your initial image data set.
2. You define a number of operations to perform on this data set using your pipeline object.
3. You execute these operations by calling the pipeline's ``sample`` method.

We will go through each of these steps in order in the proceeding 3 sub-sections.

Step 1: Create a New Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let us first create an empty pipeline. In other words, to begin any augmentation task, you must first initialise a ``Pipeline`` object, that points to a directory where your original image dataset is stored:

.. code-block:: python

    >>> import Augmentor
    >>> p = Augmentor.Pipeline("/path/to/images")
    Initialised with 100 images found in selected directory.

The variable ``p`` now contains a ``Pipeline`` object, and has been initialised with a list of images found in the source directory.

Step 2: Add Operations to the Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have created a pipeline we can begin by adding operations to the pipeline. For example, we shall begin by adding a rotate operation:

.. code-block:: python

    >>> p.rotate(probability=0.7, max_left=10, max_right=10)

In this case, we have added a rotate operation, that will execute with a probability of 70%, and have defined the maximum range by which an image will be rotated from between -10 and 10 degrees.

Next, we add a further operation, in this case a zoom operation:

.. code-block:: python

    >>> p.zoom(probability=0.3, min_scale=1.1, max_scale=1.6)

This time, we have specified that we wish the operation to be applied with a probability of 30%, while the scale should be randomly selected from between 1.1 and 1.6

Step 3: Execute and Sample From the Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have added the operations that you require, you can generate new, augmented data by using the ``sample`` function and specify the number of images you require, in this case 10,000:

.. code-block:: python

    >>> p.sample(10000)

A progress bar will appear providing a number of metrics while your samples are generated. Newly generated, augmented images will by default be saved into an ``output`` directory, relative to the directory which contains your initial image data set.

.. hint::

    A full list of operations can be found in the ``Operations`` module documentation.
