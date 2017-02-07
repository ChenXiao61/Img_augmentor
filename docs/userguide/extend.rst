Extending Augmentor
===================

Extending Augmentor to add new functionality is quite simple.

1) First you must create a new class in the ``Operations`` module (``Augmentor/Operations.py``).
2) This new class must inherit from the ``Operation`` superclass.
3) You must overload the ``perform_operation`` method belonging to the superclass.

For example, to add a new operation called FoldImage, you would add this code:

.. code-block:: python

    # Create your new operation by inheriting from the Operation superclass:
    class FoldImage(Operation):
        # Here you can accept as many custom parameters as required:
        def __init__(self, probability, num_of_folds):
            # Call the superclass's constuctor (meaning you must supply a probability value):
            Operation.__init__(self, probability)
            # Set your custom operation's member variables here as required:
            self.num_of_folds = num_of_folds

        # Your class must implement the perform_operation method:
        def perform_operation(self, image):
            # Start of code to perform custom image operation.
            for fold in range(self.num_of_folds):
                pass
            # End of code to perform custom image operation.

            # Return the image so that it can further processed in the pipeline:
            return image

This code should be placed in the ``Operations`` module. You will see that you need to overload the ``perform_operation`` function and you must call the superclass's constructor which requires a ``probability`` value to be set. Ensure you return a PIL Image as a return value.

You can also overload the superclass's ``__str__`` function to return a custom string for the object's description text. This is useful for some methods that display information about the current operation being applied.
