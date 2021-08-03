import numpy as np


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

    def setKing(self):
        self.isKing = True

    def getPos(self):
        return self.pos

    def __repr__(self):
        return self.color + str(self.pos)

    def getColor(self):
        return self.color

    def getKing(self):
        return self.isKing


class Board:
    def __init__(self):
        self.puckBag = []
        self.board = None
        self.resetBoard()
        self.newboard = None

    def resetBoard(self):
        self.board = np.ones((3, 3))
        self.board = np.zeros((8, 8), dtype=int)
        self.board[1::2, ::2] = 1
        self.board[1::2, 1::2] = 0
        self.board[::2, 1::2] = 1
        self.board[::2, 0::2] = 0
        self.puckBag = []
        self.fillPucks()

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
                    self.puckBag.append(Puck('Black', [num2, 7 - num]))

    def movePuck(self, puck, newPos):
        self.isValidMove(puck, newPos)
        puck.updatePos(newPos)
        
        
    def whiteLeft(self):
        sum = 0
        for puck in self.puckBag:
            if puck.getColor() == 'White':
                sum += 1
        return sum
    
    def blackLeft(self):
        sum = 0
        for puck in self.puckBag:
            if puck.getColor() != 'White':
                sum += 1
        return sum
    
    def whiteKings(self):
        sum = 0
        for puck in self.puckBag:
            if puck.getColor() == 'White' and puck.getKing():
                sum += 1
        return sum
    
    def blackKings(self):
        
        sum = 0
        for puck in self.puckBag:
            if puck.getColor() != 'White' and puck.getKing():
                sum += 1
        return sum
            
    def whitePos(self):
        sum = 0
        for puck in self.puckBag:
            if puck.getColor() == 'White':
                sum += 7 - puck.getPos()[1]
        return sum
    
    def blackPos(self):
        sum = 0
        for puck in self.puckBag:
            if puck.getColor() == 'Black':
                sum += puck.getPos()[1]
        return sum
    
    def evaluate(self):
        return (self.whiteLeft() - self.blackLeft()) + (self.whiteKings() * 0.5 - self.blackKings() * 0.5)
    #+ (self.whitePos() - self.blackPos())
        
    def get_all_pieces(self, colour):
        pieces = []
        for puck in self.puckBag:
            if puck.getColor() == colour:
                pieces.append(puck)
        return pieces
        
    def  isValidMove(self, puck, newPos):
        current_pos1, current_pos2 = puck.getPos()[0], puck.getPos()[1]
        new_pos1, new_pos2 = newPos[0], newPos[1]
        
        if  not 0 <= new_pos1 < 8 or not 0 <= new_pos2 < 8:
            return False
        if abs(new_pos1 - current_pos1) > 1 or abs(new_pos2 - current_pos2) > 1:
            if abs(new_pos1 - current_pos1) > 2 or abs(new_pos2 - current_pos2) > 2:
                return False
            elif self.getPuckByCoord((new_pos1, new_pos2)) is not None:
                return False
            elif not self.isNotKnight(current_pos1, current_pos2, new_pos1, new_pos2):
                return False

            else:
                # Finds the middle tile and returns the middle puck or None
                if self.isDiagonal(new_pos1, new_pos2, current_pos1, current_pos2) and self.correctDirection(puck,
                                                                                                             current_pos2,
                                                                                                             new_pos2):
                    middle1, middle2 = int((current_pos1 + new_pos1) / 2), int((current_pos2 + new_pos2) / 2)
                    middle_puck = self.getPuckByCoord((middle1, middle2))
                    if middle_puck is None:
                        return False
                    elif middle_puck.getColor() == puck.getColor():
                        return False
                    else:
                        print(middle_puck)
                        return middle_puck
                else:
                    return False
        elif not self.isDiagonal(new_pos1, new_pos2, current_pos1, current_pos2):
            return False
        elif not self.correctDirection(puck, current_pos2, new_pos2):
            return False
        elif self.getPuckByCoord((new_pos1, new_pos2)) is not None:
            return False
        return True
    
    def getValidMoves(self, puck):
        x, y = puck.getPos()[0], puck.getPos()[1]
        
        validMoves = []
        moveSet = [[1,-1], [1, 1], [-1, 1], [1, -1], [2, -2,], [2,2], [-2, 2], [-2, -2]] 
        
        
        for move in moveSet:
            move = [x+move[0], y+move[1]]
            if self.isValidMove(puck, move):
                validMoves.append(move)
        return validMoves

    def isDiagonal(self, new_pos1, new_pos2, current_pos1, current_pos2):
        if abs(new_pos1 - current_pos1) < 1 or abs(new_pos2 - current_pos2) < 1:
            return False
        return True

    def correctDirection(self, puck, current_pos2, new_pos2):
        if puck.getColor() == 'White' and not puck.getKing():
            if current_pos2 > new_pos2:
                return False
        elif puck.getColor() == 'Black' and not puck.getKing():
            if current_pos2 < new_pos2:
                return False
        return True

    def isNotKnight(self, current_pos1, current_pos2, new_pos1, new_pos2):
        if abs(current_pos1 - new_pos1) != abs(current_pos2 - new_pos2):
            return False
        return True

    def getPuckBag(self):
        return self.puckBag

    def getPuckByCoord(self, coord):
        try:
            return [x for x in self.puckBag if list(coord) == x.getPos()][0]
        except IndexError:
            return None
        
    def ai_move(self, board):
        self.puckBag = board.getPuckBag()
        return self.puckBag

    def removePiece(self, puck):
        self.puckBag.remove(puck)
        