Extending Augmentor
===================

Extending Augmentor to add new functionality is quite simple. Merely inherit from the ``Operation`` superclass, and overload its ``perform_operations`` method. In your subclass you must also initialise the superclass, meaning you must provide the ``probability`` member variable at a minimum.

For example:

.. code-block:: python

    class New_Operation(Operation):
        def __init__(self, probability):
            Operation.__init__(self, probability)

        def perform_operation(self, image):
            # Perform image operations here
            return image

This code should be placed in the ``Operations`` module.