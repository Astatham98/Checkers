import pygame
import math
from main import Board, Puck
from minimax.algo import minimax


class GUI:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 900
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        
        self.crownImg  = pygame.image.load('crown.png')
        self.crownImg = pygame.transform.scale(self.crownImg, (50, 50))

        self.board = Board()
        self.puckBag = self.board.getPuckBag()
        self.SelectedPuck = None
        self.whosMove = 'White'
        self.completed = False

        # Define Colors 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.TAN = (210, 180, 140)

        pygame.init()  # Start Pygame

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Start the screen
        self.screen.fill(self.WHITE)
        self.main_menu()
       
       
       

    def main_menu(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            play_human_button = self.button(self.screen, (100, 100), 'Play against another player')
            play_ai_button = self.button(self.screen, (100, 200), 'Play against an AI')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # The user closed the window!
                    running = False  # Stop running
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if play_human_button.collidepoint(pygame.mouse.get_pos()):
                        self.checkers_screen()
                    if play_ai_button.collidepoint(pygame.mouse.get_pos()):
                        self.choose_ai_menu()
            
            pygame.display.update()
            self.fpsClock.tick(self.FPS)
        pygame.quit()  # Close the window
            
    
    def checkers_screen(self):
        
        #reset screen
        self.screen.fill(self.WHITE)
        
        self.drawSquares(self.screen)
        self.drawButtons(self.screen)
        self.drawPucks(self.screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # The user closed the window!
                    running = False  # Stop running
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.b2.collidepoint(pygame.mouse.get_pos()):
                        running = False  # Stop running
                    if self.b1.collidepoint(pygame.mouse.get_pos()):
                        self.resetBoard()
                    if x < 800 and y < 800:
                        x, y = math.floor(x / 100), math.floor(y / 100)
                        self.movePuck(x, y)

            pygame.display.update()
            self.fpsClock.tick(self.FPS)
        pygame.quit()  # Close the window
        
    def choose_ai_menu(self):
        
        self.screen.fill(self.WHITE)
        Minmax = self.button(self.screen, (100, 100), 'MinMax')
        negamax = self.button(self.screen, (100, 200), 'Negamax')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # The user closed the window!
                    running = False  # Stop running
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if negamax.collidepoint(pygame.mouse.get_pos()):
                        self.checkers_screen()
                    if Minmax.collidepoint(pygame.mouse.get_pos()):
                        self.ai_checkers_screen()

            pygame.display.update()
            self.fpsClock.tick(self.FPS)
        pygame.quit()  # Close the window

    def ai_checkers_screen(self):
        
        #reset screen
        self.screen.fill(self.WHITE)
        
        self.drawSquares(self.screen)
        self.drawButtons(self.screen)
        self.drawPucks(self.screen)

        running = True
        while running:
            if self.whosMove == 'White':
                value, new_bag = minimax(self.board, 3, True, None)
                print(value, new_bag.getPuckBag())
                #nb = [x for x in new_bag.getPuckBag() if x.getColor() == 'White']
                #pb = [x for x in self.puckBag if x.getColor() == 'White']
                #print(f'value= {value}  new bag: {nb}   and {pb}')
                self.puckBag = self.board.ai_move(new_bag)
                self.switchColors()
                self.redrawScreen()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # The user closed the window!
                    running = False  # Stop running
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.b2.collidepoint(pygame.mouse.get_pos()):
                        running = False  # Stop running
                    if self.b1.collidepoint(pygame.mouse.get_pos()):
                        self.resetBoard()
                    if x < 800 and y < 800:
                        x, y = math.floor(x / 100), math.floor(y / 100)
                        self.movePuck(x, y)

            pygame.display.update()
            self.fpsClock.tick(self.FPS)
        pygame.quit()  # Close the window

    def drawSquares(self, screen):
        for i in range(8):
            for j in range(8):
                if j % 2 == 0:
                    if i % 2 != 0:
                        pygame.draw.rect(screen, self.BLACK, (i * 100, j * 100, 100, 100))
                else:
                    if i % 2 == 0:
                        pygame.draw.rect(screen, self.BLACK, (i * 100, j * 100, 100, 100))

    def button(self, screen, position, text):
        font = pygame.font.SysFont("Arial", 50)
        text_render = font.render(text, 1, (255, 0, 0))
        x, y, w, h = text_render.get_rect()
        x, y = position
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
        pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
        return screen.blit(text_render, (x, y))

    def drawButtons(self, screen):
        self.b1 = self.button(screen, (50, 825), 'New Game.')
        self.b2 = self.button(screen, (525, 825), 'Quit.')
        self.b3 = self.button(screen, (350, 825), self.whosMove)

    def drawPucks(self, screen):
        for i in range(8):
            for j in range(3):
                if j % 2 == 0:
                    if i % 2 != 0:
                        pygame.draw.circle(screen, self.TAN, ((i * 100) + 50, (j * 100) + 50), 45)
                    else:
                        pygame.draw.circle(screen, self.RED, ((i * 100) + 50, (j * 100) + 550), 45)
                else:
                    if i % 2 == 0:
                        pygame.draw.circle(screen, self.TAN, ((i * 100) + 50, (j * 100) + 50), 45)
                    else:
                        pygame.draw.circle(screen, self.RED, ((i * 100) + 50, (j * 100) + 550), 45)

    def getPuckByCoord(self, coord):
        try:
            return [x for x in self.puckBag if list(coord) == x.getPos()][0]
        except IndexError:
            return None

    def movePuck(self, x, y):
        desiredPuck = self.getPuckByCoord((x, y))  # returns the puck or none given the coordinate
        self.reCheckKing()    
    
        if desiredPuck is not None and desiredPuck.getColor() == self.whosMove and not self.completed:
            if self.SelectedPuck is not None:  # If there is already a selected puck return it to its original position
                chosenColor = self.TAN if self.SelectedPuck.getColor() == 'White' else self.RED
                nx, ny = self.SelectedPuck.getPos()
                pygame.draw.rect(self.screen, self.BLACK, (nx * 100, ny * 100, 100, 100))
                pygame.draw.circle(self.screen, chosenColor, ((nx * 100) + 50, (ny * 100) + 50), 45)

            # Draw a green outline around the puck to show its selected
            self.greenOutline(desiredPuck, x, y)

        elif self.SelectedPuck is not None:
            # If there is a selected puck, move it
            nx, ny = self.SelectedPuck.getPos()
            if self.board.isValidMove(self.SelectedPuck, [x, y]):
                
                self.middlePuck(x, y)
                
                self.board.movePuck(self.SelectedPuck, [x, y])
                
                
            
                self.redrawScreen()    
                self.checkConds(x, y)
                self.switchColors()
                self.drawButtons(self.screen)
            else:
                pass

    def greenOutline(self, puck, x, y):
        self.SelectedPuck = puck
        self.board.getValidMoves(self.SelectedPuck)

        chosenColor = self.TAN if self.SelectedPuck.getColor() == 'White' else self.RED
        pygame.draw.rect(self.screen, self.GREEN, (x * 100, y * 100, 100, 100))
        pygame.draw.circle(self.screen, chosenColor, ((x * 100) + 50, (y * 100) + 50), 45)
        if self.SelectedPuck.getKing():
            self.screen.blit(self.crownImg, ((x*100)+20, (y*100)+20))
            
    def middlePuck(self, x, y):
        middlePuck = self.board.isValidMove(self.SelectedPuck, [x, y]) if type(
                    self.board.isValidMove(self.SelectedPuck, [x, y])) is not bool else None
        
        if middlePuck is not None:
            nnx, nny = middlePuck.getPos()
            pygame.draw.rect(self.screen, self.BLACK, (nnx * 100, nny * 100, 100, 100))
            self.puckBag.remove(middlePuck)

    def checkConds(self, x, y):
        if not self.checkEndCond():
                    self.completedGame()
                    print('end game condition is: ' + str(self.checkEndCond()))
        else:
            if self.checkKingCond(self.SelectedPuck):
                self.screen.blit(self.crownImg, ((x*100)+20, (y*100)+20))
    
    def completedGame(self):
        self.completed = True
        text = self.whosMove + " Wins!"
        font = pygame.font.SysFont("Arial", 75)
        text_render = font.render(text, 1, (0, 255, 0))
        self.screen.blit(text_render, (250, 300))
        

    def switchColors(self):
        if self.whosMove == 'White':
            self.whosMove = 'Black'
        else:
            self.whosMove = 'White'

    def checkEndCond(self):
        first = self.puckBag[0]
        canMove = False
        for x in self.puckBag:
            if x.getColor() != first.getColor():
                return False
            if len(self.board.getValidMoves(x)) > 0: 
                canMove = True
                break
        #return canMove
        return True
    
    def checkKingCond(self, puck):
        if puck.getColor() == 'White':
            if puck.getPos()[1] == 7:
                puck.setKing()
                return True
    
        elif puck.getColor() == 'Black':
            if puck.getPos()[1] == 0:
                puck.setKing()
                return True
    
    def reCheckKing(self):
        for puck in self.puckBag:
            if puck.getKing():
                x,y = puck.getPos()
                self.screen.blit(self.crownImg, ((x*100)+20, (y*100)+20))
    
    def resetBoard(self):
        # Resets the screen
        self.screen.fill(self.WHITE)
        self.drawSquares(self.screen)
        self.drawButtons(self.screen)
        self.drawPucks(self.screen)
        self.SelectedPuck = None
        self.board.resetBoard()
        self.puckBag = self.board.getPuckBag()
        self.whosMove = 'White'
        self.completed = False

    def drawPuckBag(self):
        for puck in self.puckBag:
            x, y = puck.getPos()[0], puck.getPos()[1]
            if puck.getColor() == 'White':
                pygame.draw.circle(self.screen, self.TAN, ((x * 100) + 50, (y * 100) + 50), 45)
            else:
                pygame.draw.circle(self.screen, self.RED, ((x * 100) + 50, (y * 100) + 50), 45)

    def redrawScreen(self):
        self.drawSquares(self.screen)
        self.drawPuckBag()

if __name__ == '__main__':
    b = GUI()
