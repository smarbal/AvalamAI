cpdef wintower(list board, int playerpiece ) : 
    cdef list tower 
    cdef int a 
    cdef int b 
    cdef int i 
    i = 0 
    for a in range(9): 
            for b in range(9) :
                tower = board[a][b]
                if len(tower) == 5 :
                    piece = tower[4]     
                    if piece == playerpiece : 
                        i += 1
    return i 
            