cdef class Parsing_core_Float32:
    cdef readonly str file
    cdef readonly int count
    cdef public list raw
    cdef bint if_report

    cpdef read(self)
    cpdef seek(self, file, long pos, long num)
    cpdef pmsg(self, unsigned char *data)
