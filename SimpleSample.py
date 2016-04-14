from Augmentor import Pipeline

## set the path to the folder with images to manipulate
pathToImages = 'path/to/source'

## create pipeline
pipe = Pipeline.Pipeline(pathToImages)

## add functions to pipeline
pipe.addFlipY()
pipe.addFlipX(1)

## add another function to pipeline
pipe.addCrop(45, 45)

## print a summary
pipe.summary()
pipe.image_source.summary()

## execute the functions in pipline
pipe.execute()

## all images are created in target folder
