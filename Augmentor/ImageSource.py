class ImageSource(object):

    def __init__(self, rootpath='.'):
        self.rootpath = rootpath


    def summary(self):
        print "The current directory is " + str(rootpath)

