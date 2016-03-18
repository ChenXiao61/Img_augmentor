import glob
# Perhaps put all imports in __init__.py
# Because I am not sure if this is where imports go for classes.

class ImageSource(object):

    def __init__(self, rootpath='.'):
        self.rootpath = rootpath

        self.scan(rootpath)

    def scan(self, pathToScan):
        print "Scanning " + pathToScan + " folder."
        self.listOfFiles = glob.glob('./*')
        

    def summary(self):
        print "The current directory is " + str(self.rootpath)
