STUFF = "Hi"
cpdef is_alone(list board, int playerpiece ) : 
    cdef list tower 
    cdef list othertower 
    cdef int a 
    cdef int b 
    cdef int c 
    cdef int d 
    cdef int alone
    cdef int verif 
    alone = 0
    for a in range(9): 
            for b in range(9) :
                tower = board[a][b]
                if tower != [] : 
                    verif = 0
                    while verif == 0 : 
                        for c in range(-1,2) : 
                            for d in range(-1,2) : 
                                if a+c >= 0 and a+c < 9: 
                                    if b+d >= 0 and b+d <9: 
                                        othertower = board[a+c][b+d] 
                                        if othertower != [] :
                                            verif += 1
                    if verif == 0 : 
                        piece = tower[-1]    
                        if piece == playerpiece : 
                            alone += 1 
    return alone
