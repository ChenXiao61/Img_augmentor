class ProgramFinishedException(Exception):
    def __init__(self, message):
        super(ProgramFinishedException, self).__init__(message)
