import numpy as np
import pygame
import random

class Puck:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.alive = True
        self.isKing = False
    
    def kill(self):
        self.alive = False

    def updatePos(self, newPos):
        self.pos = newPos
        
    def setKing(self, king):
        self.isKing = king
        
    def getPos(self):
        return self.pos    
    
    def __repr__(self):
        return self.color + str(self.pos)
        
        
class Board:
    def __init__(self):
        self.puckBag = []
        self.board = None
        self.resetBoard()
        self.newboard = None
    
    def resetBoard(self):
        self.board = np.ones((3,3))
        self.board = np.zeros((8,8), dtype=int)
        self.board[1::2,::2] = 1
        self.board[1::2,1::2] = 0
        self.board[::2,1::2] = 1
        self.board[::2,0::2] = 0
        self.puckBag = []
    
    def fillPucks(self):
        top = self.board[:3]
        bottom = self.board[-3:]
        for num, line in enumerate(top):
            for num2, square in enumerate(line):
                if square == 1:
                    self.puckBag.append(Puck('White', [num2, num]))
                    
        for num, line in enumerate(bottom):
            for num2, square in enumerate(line):
                if square == 1:
                    self.puckBag.append(Puck('Black', [num2, 7-num]))
                    
    def movePuck(self, puck, newPos):
        puck.setPos(newPos)
        
    def isValidMove(self, puck, newPos):
        current_pos1, current_pos2 = puck.get_pos()[0], puck.get_pos()[1]
        new_pos1, new_pos2 = newPos[0], newPos[1]
        if abs(new_pos1, current_pos2) > 1 or abs(new_pos2, current_pos2) > 1:
            print('greater')
     
        """
        Only for testing 
        """    
    def newBoard(self):
        board_copy = self.board.copy()
        for puck in self.puckBag:
            pos = puck.getPos()
            board_copy[pos[1]][pos[0]] = 3 if puck.color == 'White' else 4
        self.newboard = board_copy 
        
if __name__ == '__main__':
    board = Board()
    board.fillPucks()
    board.newBoard()
                