from Augmentor import Pipeline

## set the path to the folder with images to manipulate
pathToImages = 'C:/Users/Lukas/Pictures/sample'

## create pipeline
pipe = Pipeline.Pipeline(pathToImages)

## add function to pipeline
pipe.addFlipY()
pipe.addFlipX(1)

## add another function to pipeline
pipe.addCrop(45, 45)

## execute the functions in pipline
pipe.execute()

## all images are created in target folder

## print a summary
pipe.image_source.summary()

