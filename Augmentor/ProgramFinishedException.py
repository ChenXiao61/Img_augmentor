
class ProgramFinishedException(Exception):

    def __init___(self, value):
        Exception.__init__(self, value)
        self.value = value

    def __str__(self):
        return repr(self.value)