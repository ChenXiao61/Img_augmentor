Extending Augmentor
===================

Extending Augmentor to add new functionality is quite simple, and is performed in two steps: 1) create a custom class which subclasses from the :class:`.Operation` base class, and 2) add an object of your new class to the pipeline using the :func:`add_operation` function.

This allows you to add custom functionality at run-time. Of course, if you have written an operation that may be of benefit to the community, you can of course make a pull request on the GitHub repository.

The following sections describe extending Augmentor in two steps. Step 1 is creating a new :class:`Operation` subclass, and step 2 is using an object of your new custom operation in a pipeline.

Step 1: Create a New Operation Subclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a custom operation and extend Augmentor:

1) First you must create a new class in the :mod:`.Operations` module.
2) This new class must inherit from the :class:`.Operation` base class.
3) You must overload the :func:`~Augmentor.Operations.Operation.perform_operation` method belonging to the superclass.

For example, to add a new operation called ``FoldImage``, you would add this code:

.. code-block:: python

    # Create your new operation by inheriting from the Operation superclass:
    class FoldImage(Operation):
        # Here you can accept as many custom parameters as required:
        def __init__(self, probability, num_of_folds):
            # Call the superclass's constructor (meaning you must
            # supply a probability value):
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

This code should be placed in the :mod:`.Operations` module. You will see that you need to implement the :func:`~Augmentor.Operations.Operation.perform_operation` function and you must call the superclass's constructor which requires a :attr:`probability` value to be set. Ensure you return a PIL Image as a return value.

.. hint::

    You can also overload the superclass's :func:`~Augmentor.Operations.Operation.__str__` function to return a custom string for the object's description text. This is useful for some methods that display information about the current operation being applied.

Step 2: Add a New Function to the Pipeline Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have a new operation which is of type :class:`Operation`, you can add an object of you new operation to an existing pipeline.

.. code-block:: python

    # Instantiate a new object of your custom operation
    fold = Fold(probability = 0.75, num_of_folds = 4)

    # Add this to the current pipeline
    p.add_operation(fold)

    # Executed the pipeline as normal, and your custom operation will be executed
    p.sample(1000)

As you can see, adding custom operations at run-time is possible by subclassing the :class:`Operation` class and adding an object of this class to the pipeline manually using the :func:`add_operation` function.