from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
class ProgramFinishedException(Exception):
    def __init__(self, message):
        super(ProgramFinishedException, self).__init__(message)
