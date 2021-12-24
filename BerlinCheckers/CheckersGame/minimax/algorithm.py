from copy import deepcopy
from math import floor
#black = 0, red = 1
places = [7,9,14,18,-7,-9,-14,-18]

def add_move(position, i, j):
    cpposition = deepcopy(position)
    id = cpposition[j]
    cpposition[j].square_value = None
    cpposition[j].isKing = False
    if i == 14 or i == 18 or i == -14 or i == -18:
        if cpposition[j+floor(i/2)].square_value != None:
           cpposition[j+floor(i/2)].isKing = False
           cpposition[j+floor(i/2)].square_value = None
    cpposition[j+i] =  id
    return cpposition

def get_all_moves(position, player):
    if position == None:
        return []
    moves = []
    if player == 0:
        for j in range(0,64,1):
            square = position[j]
            if square != None and square.square_value != None and square.square_value > 11:
                if square.isKing: 
                    for i in places:
                        # print(i)
                        if j+i > -1 and j+i <64 and position[i+j] != None and position[j+i].square_value == None:
                            moves.append(add_move(position, i, j))
                else:
                    for i in places:
                        # if i+j < 64 and i+j > -1:
                        #     print(position[j+i].square_value == None)
                        if (i == -7 or i == -9) and j+i > -1 and j+i <64 and position[i+j] != None and position[j+i].square_value == None:
                            print("I am here")
                            moves.append(add_move(position, i, j))
    else:
        for j in range(0,64,1):
            square = position[j]
            if square != None and square.square_value != None and square.square_value < 12:
                if square.isKing: 
                    for i in places:
                        if j+i > -1 and j+i <64 and position[i+j] != None and position[j+i] == None:
                            moves.append(add_move(position, i, j))
                else:
                    for i in places:
                        if (i == 7 or i == 9) and j+i > -1 and j+i <64 and position[i+j] != None and position[j+i] == None:
                            moves.append(add_move(position, i, j))
    print('returning moves:')
    print(moves)
    return moves

def calc_score(position, player):
    count_red = 0
    count_black = 0
    count_king_red = 0
    count_king_black = 0
    for square in position:
        if square != None:
            if square.square_value != None and square.square_value < 12:
                if square.isKing:
                    count_king_red = count_king_red+1
                else:
                    count_red = count_red+1
            elif square.square_value != None and square.square_value > 11:
                if square.isKing:
                    count_king_black = count_king_black+1
                else:
                    count_black = count_black+1
    if player == 1:
        return count_red
    else:
        return count_black 

def evaluate(position):
    count_red = 0
    count_black = 0
    count_king_red = 0
    count_king_black = 0
    for square in position:
        if square != None:
            if square.square_value != None and square.square_value < 12:
                if square.isKing:
                    count_king_red = count_king_red+1
                else:
                    count_red = count_red+1
            elif square.square_value != None and square.square_value > 11:
                if square.isKing:
                    count_king_black = count_king_black+1
                else:
                    count_black = count_black+1
    return count_black-count_red + (count_king_black - count_king_red)*0.5

def winner(position):
    count_red = 0
    count_black = 0
    count_king_red = 0
    count_king_black = 0
    for square in position:
        if square != None:
            # print(square.square_value)
            if square != None and square.square_value != None and square.square_value < 12:
                if square.isKing:
                    count_king_red = count_king_red+1
                else:
                    count_red = count_red+1
            elif square != None and square.square_value != None and square.square_value > 11:
                if square.isKing:
                    count_king_black = count_king_black+1
                else:
                    count_black = count_black+1
    if count_red+count_king_red == 0:
        return 0
    elif count_black+count_king_black == 0:
        return 1
    else:
        return None
    

def minimax(position, depth, max_player):
    # print('Inside in minimax algo')
    # print(depth)
    # print(position)
    if depth == 0 or winner(position) != None:
        return evaluate(position), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, 0):
            # print('calculating moves')
            evaluation = minimax(move, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, 1):
            evaluation = minimax(move, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move