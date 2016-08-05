Usage
=====

Here we describe the general usage of Augmentor. 


Getting Started
---------------

Overview
^^^^^^^^

Augmentor consists of three major components in order to provide its funcionality. They are the ``ImageSource`` class, the ``ImageOperations`` class, and the ``Pipeline`` class. We will first describe the purpose of each of these classes and how they can be used to augment an image dataset.

General Procedure
^^^^^^^^^^^^^^^^^

In general, a usage pattern consists of the following three steps:

1. You instantiate an ``ImageSource`` object poiting to a directory containing your initial image data set
2. You define a number of operations to perform on this data set using the ``ImageOperations`` class.
3. You execute these operations by using the ``Pipeline`` class.

Each class is explained in detail below. In the next section we shall go over some concrete examples.

.. class:: ImageSource

Some text.

.. class:: ImageOperations

Some text.
