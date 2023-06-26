# distutils: language = c++

cimport parsing_core
from parsing_core import Parsing_core
cimport parsing_core_Float32
from parsing_core_Float32 import Parsing_core_Float32

cdef class Picoscenes:
    cdef readonly str file
    cdef readonly int count
    cdef public list raw

    def __cinit__(self, file, *argv, **kw):
        self.file = file
        self.raw = list()
        self.select()

    def __init__(self, file):
        pass

    def select(self):
        try:
            temp = Parsing_core(self.file)
            self.file = temp.file
            self.count = temp.count
            self.raw = temp.raw

        except:
            pass

        if not self.raw:
            temp = Parsing_core_Float32(self.file)
            self.file = temp.file
            self.count = temp.count
            self.raw = temp.raw

    cpdef pmsg(self, unsigned char *data):
        return Parsing_core.pmsg(data)
