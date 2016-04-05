from Augmentor import Pipeline
from Augmentor import ImageSource


pathToImages = 'C:/Users/Lukas/Pictures/sample'
pipe = Pipeline.Pipeline(pathToImages)
#pipe.addFlipY(0.4)
#pipe.addFlipX(0.4)
#pipe.addRotate90(0.4)
#pipe.addRotate180(0.4)
#pipe.addRotate270(0.4)
#pipe.addResize(90,180)
#pipe.addScale(90,180)
#pipe.addRotate(45)
pipe.addCrop(90,90)
pipe.execute()
pipe.imageSource.summary()