cimport km_unitig
from libc.stdlib cimport malloc, free
from libc.string cimport strdup

def py_main_unitig(list argv):
    cdef int argc = len(argv)
    
    if argc == 0:
        # Handle empty argv gracefully
        return
    
    cdef char **c_argv = <char **>malloc((argc+1) * sizeof(char *))
    if c_argv is NULL:
        # Handle allocation failure
        raise MemoryError("Failed to allocate memory")
    
    try:
        for i in range(argc):
            if argv[i] is None:
                # Handle invalid argument
                raise ValueError("Invalid argument at index {}".format(i))
            c_argv[i] = strdup(argv[i].encode('utf-8'))
            if c_argv[i] is NULL:
                # Handle strdup failure
                raise MemoryError("Failed to allocate memory for argument {}".format(i))
        c_argv[argc] = NULL
        
        return km_unitig.main_unitig(argc, c_argv)
    finally:
        for i in range(argc):
            if c_argv[i] is not NULL:
                free(c_argv[i])
        free(c_argv)
