from copy import deepcopy
import pygame
from main import Board

board = Board()

def minimax(board_, depth, max_player, game):
    board_ = deepcopy(board_)
    if depth == 0:
        return board_.evaluate(), board_
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        
        for move in get_all_moves(board_, 'White', game): 
            evaluation = minimax(move, depth-1, False, game)[0]
            print(f'maxeval {maxEval},curr_eval {evaluation}, currentDepth {depth}')
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        
        for move in get_all_moves(board_, 'Black', game): 
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move
    
def get_all_moves(board_, color, game):
    moves = []
    moves_readable = []
    
    for piece in board_.get_all_pieces(color):
        valid_moves = board_.getValidMoves(piece)
        skip = None
        print(piece)
        if len(valid_moves) > 0:
            for move in valid_moves:
                temp_board = deepcopy(board_)
                new_board = simulate_move(piece, move, temp_board, skip)
                moves.append(new_board)
                moves_readable.append([piece, move])
    print(f'readable moves: {moves_readable}')
    return moves
            
def simulate_move(piece, move, board_, skip=None):
    board_.movePuck(piece, move)
    if skip:
        board_.removePiece(piece)
    return board_