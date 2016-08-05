Examples
========

A number of typical usage scenarios are desribed here. 

Initialising a pipeline
-----------------------

.. code-block:: python
    
     import Augmentor

     path_to_data = "/home/bingolittle/images/dataset1/"

     # Create a pipeline
     pipe = Pipeline.Pipeline(path_to_data)

Adding operations to a pipeline
-------------------------------

.. code-block:: python

    # Add some operations to an existing pipeline
    # add addFlipY operation to the pipeline
    pipe.addFlipY(1)
    # add addCrop operation to the pipeline
    pipe.addCrop(45, 45)
    # add addRotatet90 operation to the pipeline
    pipe.addRotate90()

Executing a pipeline
--------------------

.. code-block:: python

    try:
        pipe.execute()
    except pipe.ProgramFinishedException as e:
        print(str(e))
    
    # Or set a limit
    number_of_images = 12
    try:
        pipe.execute(number_of_images)
    except pipe.ProgramFinishedException as e:
        print(str(e))
