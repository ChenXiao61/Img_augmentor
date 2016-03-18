import glob

class ImageSource(object):

    def __init__(self, rootpath='.'):
        self.rootpath = rootpath

        self.scan(rootpath)

    def scan(self, pathToScan):
        print "Scanning " + pathToScan + " folder."
        self.listOfFiles = glob.glob('./*')
        

    def summary(self):
        print "The current directory is " + str(self.rootpath)
