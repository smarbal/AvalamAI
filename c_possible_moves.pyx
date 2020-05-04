cpdef list possible_moves(list body) : 
    cdef list board 
    cdef list tower 
    cdef list other_tower
    cdef list moves  
    cdef int a 
    cdef int b 
    cdef int c 
    cdef int d  
    board = body
    moves = []
    for a in range(9): 
        for b in range(9) :
            tower = board[a][b]
            if tower != [] : 
                for c in range(-1,2) : 
                    for d in range(-1,2) : 
                        if a+c >= 0 and a+c < 9: 
                            if b+d >= 0 and b+d <9: 
                                othertower = board[a+c][b+d] 
                                if othertower != [] :
                                    if c == d == 0 : 
                                        pass
                                    elif len(tower) + len(othertower) <= 5 : 
                                        moves.append([[a,b],[a+c,b+d], len(tower)])  
                                            # on ajoute aux moves possibles les coordonées de respectivement la première et deuxième tour. exemple de move : [[0, 3], [0, 4]]
    return moves
    print(moves)