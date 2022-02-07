"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math
from sys import getrecursionlimit
from random import sample

X = 'X'
O = 'O'
EMPTY = None
alpha = float('-inf')
beta = float('inf')

def initial_state():
    """
    Returns starting state of the board.
    """   
    return   [[EMPTY,EMPTY, EMPTY],
        [EMPTY,EMPTY,EMPTY],
        [EMPTY,EMPTY, EMPTY]]

def player(board):
    turnX, turnO = (0,0)
    for row in board:
        for cell in row:
            if cell == X:
                turnX +=1
            elif cell == O:
                turnO += 1
    
    if turnX > turnO:
        return O
    elif not terminal(board) and turnX == turnO:
        return X
    else:
        return None
   
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    position = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == None:
                position.add((i,j))
    
    return position

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = deepcopy(board)
    i,j = action
    
    if board_copy[i][j] != None:
        raise Exception('Position in use')
    
    board_copy[i][j] = player(board)
    
    return board_copy
    
def resultO(board,i, j, empty_home):
    if i == 0 and j == 0:
        if board[i][j] == 'O':
            if not (i, j+1) in empty_home and not (i, j+2) in empty_home:
                if board[i][j+1] == 'O' and board[i][j+2] == 'O':
                    return 'O'
                    
            if not (i+1, j) in empty_home and not (i+2, j) in empty_home:
                if board[i+1][j] == 'O' and board[i+2][j] == 'O':
                    return 'O'
                    
            if not (i+1, i+1) in empty_home and not (i+2, i+2) in empty_home:
                if board[i+1][i+1] == 'O' and board[i+2][i+2] == 'O':
                    return 'O'
    
    if i == 1 and j == 0:
        if board[i][j] == 'O':
            if not (i, j+1) in empty_home and not (i, j+2) in empty_home:
                if board[i][j+1] == 'O' and board[i][j+2] == 'O':
                    return 'O'
                            
    if i == 2 and j == 0:
        if board[i][j] == 'O':
            if not (i, j+1) in empty_home and not (i, j+2) in empty_home:
                if board[i][j+1] == 'O' and board[i][j+2] == 'O':
                    return 'O'
                    
            if not (i-1, i-1) in empty_home and not (i-2, i) in empty_home:
                if board[i-1][i-1] == 'O' and board[i-2][i] == 'O':
                    return 'O'
                
    if i == 1 and j == 1:
        if board[i][j] == 'X':
            if not (i, j - 1) in empty_home and not (i, j+1) in empty_home:
                if board[i][j-1] == 'X' and board[i][j+1] == 'X':
                    return 'X'
                
            if not (i-1, j) in empty_home and not (i+1, j) in empty_home:
                if board[i-1][j] == 'X' and board[i+1][j] == 'X':
                    return 'X'
    
    if i == 0 and j == 2:
        if board[i][j] == 'O':
            if not (i+1, j) in empty_home and not (i+2, j) in empty_home:
                if board[i+1][j] == 'O' and board[i+2][j] == 'O':
                    return 'O'
    return None
                    
def resultX(board,i, j, empty_home):
    if i == 0 and j == 0:
        if board[i][j] == 'X':
            if not (i, j+1) in empty_home and not (i, j+2) in empty_home:
                if board[i][j+1] == 'X' and board[i][j+2] == 'X':
                    return 'X'
                    
            if not (i+1, j) in empty_home and not (i+2, j) in empty_home:
                if board[i+1][j] == 'X' and board[i+2][j] == 'X':
                    return 'X'
                    
            if not (i+1, i+1) in empty_home and not (i+2, i+2) in empty_home:
                if board[i+1][i+1] == 'X' and board[i+2][i+2] == 'X':
                    return 'X'
                    
    if i == 1 and j == 0:
        if board[i][j] == 'X':
            if not (i, j+1) in empty_home and not (i, j+2) in empty_home:
                if board[i][j+1] == 'X' and board[i][j+2] == 'X':
                    return 'X'
                            
    if i == 2 and j == 0:
        if board[i][j] == 'X':
            if not (i, j+1) in empty_home and not (i, j+2) in empty_home:
                if board[i][j+1] == 'X' and board[i][j+2] == 'X':
                    return 'X'
                    
            if not (i-1, i-1) in empty_home and not (i-2, i) in empty_home:
                if board[i-1][i-1] == 'X' and board[i-2][i] == 'X':
                    return 'X'
                    
    if i == 1 and j == 1:
        if board[i][j] == 'X':
            if not (i, j - 1) in empty_home and not (i, j+1) in empty_home:
                if board[i][j-1] == 'X' and board[i][j+1] == 'X':
                    return 'X'
                
            if not (i-1, j) in empty_home and not (i+1, j) in empty_home:
                if board[i-1][j] == 'X' and board[i+1][j] == 'X':
                    return 'X'
                
    if i == 0 and j == 2:
        if board[i][j] == 'X':
            if not (i+1, j) in empty_home and not (i+2, j) in empty_home:
                if board[i+1][j] == 'X' and board[i+2][j] == 'X':
                    return 'X'
    
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    coordinate = [(0,0), (1,0), (2,0), (0,2), (1,1)]
                              
    for i,j in coordinate:
        x = resultX(board, i, j, actions(board))
        if x:
            return x
        
        o = resultO(board, i, j, actions(board))
        if o:
            return o

    return None               

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    if len(actions(board)) == 0:
        return True
    
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    
    return 0

def maxValueAB(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, minValueAB(result(board, action), alpha, beta))
        if v >= beta: return v
        alpha = max(alpha, v)
    
    return v

def minValueAB(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, maxValueAB(result(board, action), alpha, beta))
        if v <= alpha: return v
        beta = min(beta, v)
    
    return v

def alphaBetaSearch(board):
    """
    Returns the optimal action for the current player on the board.
    """
    turn = player(board)
    if turn == X:
        v = float('-inf')
        move = None
        for action in actions(board):
            x = minValueAB(result(board, action), alpha, beta)
            if x > v:
                v = x
                move = action
        return move
    
    if turn == O:
        v = float('inf')
        move = None
        for action in actions(board):
            x = maxValueAB(result(board, action), alpha, beta)
            if x < v:
                v = x
                move = action
        
        return move