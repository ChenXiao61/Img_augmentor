Extending Augmentor
===================

Extending Augmentor to add new functionality is quite simple, and is performed in two steps: 1) create a custom class which subclasses from the :class:`.Operation` base class, and 2) add a user facing function in the :class:`.Pipeline` class to handle parameters.

Both steps are outlined in the proceeding sub-sections.

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

After a new class has been written, you must create the interface by which users will interact with it by plugging a function into the :class:`.Pipeline` class (part of the :mod:`Augmentor.Pipeline` **module**).

This function must:

1) Handle the parameters, if any, of your new operation. At a minimum you must accept a :attr:`probability` parameter.
2) Append an object of your new operation to the :class:`.Pipeline`'s :attr:`operations` member variable.

An example of this is shown below:

.. code-block:: python

    def fold(probability, folds):
        # Handle anything regarding user input, i.e. the minimum number of folds.
        if len(folds) > 10:
            pass

        # Append an object of the Fold class to the operations member variable.
        self.operations.append(Fold(probability=probability, folds=folds))

Note, the new function :func:`fold` is inserted into the :class:`.Pipeline` class, This allows you to handle how parameters are dealt with, and so on.