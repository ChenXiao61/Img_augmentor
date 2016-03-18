class ImageSource(object):

    def __init__(self, rootpath='.'):
        self.rootpath = rootpath
        
        scan(rootpath)

    def scan(pathToScan):
        print "Scanning " + pathToScan + " folder."

    def summary(self):
        print "The current directory is " + str(rootpath)

