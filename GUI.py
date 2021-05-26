import pygame
import random

from pygame.constants import BUTTON_LEFT

class GUI:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 900
        self.FPS = 30

        # Define Colors 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.TAN = (210, 180, 140)

        pygame.init() #Start Pygame

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) #Start the screen
        self.screen.fill(self.WHITE)
        self.drawSquares(self.screen)
        self.drawButtons(self.screen)
        self.drawPucks(self.screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #The user closed the window!
                    running = False #Stop running
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.b2.collidepoint(pygame.mouse.get_pos()):
                        running = False #Stop running
                    if self.b1.collidepoint(pygame.mouse.get_pos()):
                        self.screen.fill(self.WHITE)
                        self.drawSquares(self.screen)
                        self.drawButtons(self.screen)
            
           
            
           
            
            pygame.display.update()
    
        pygame.quit() #Close the window


    def drawSquares(self, screen):
        for i in range(8): 
            for j in range(8):
                if j % 2 == 0:
                    if i % 2 != 0:
                        pygame.draw.rect(screen, self.BLACK, (i*100, j*100, 100, 100))
                else:
                    if i % 2 == 0:
                        pygame.draw.rect(screen, self.BLACK, (i*100, j*100, 100, 100))
    
    
    def button(self, screen, position, text):
        font = pygame.font.SysFont("Arial", 50)
        text_render = font.render(text, 1, (255, 0, 0))
        x, y, w , h = text_render.get_rect()
        x, y = position
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
        pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
        return screen.blit(text_render, (x, y))
    
    def drawButtons(self, screen):
        self.b1 = self.button(screen, (50, 825), 'New Game.')
        self.b2 = self.button(screen, (525, 825), 'Quit.')
        
    def drawPucks(self, screen):
        for i in range(8): 
            for j in range(3):
                if j % 2 == 0:
                    if i % 2 != 0:
                        pygame.draw.circle(screen, self.TAN, ((i*100)+50, (j*100)+50), 45)
                    else:
                        pygame.draw.circle(screen, self.RED, ((i*100)+50, (j*100)+550), 45)
                else:
                    if i % 2 == 0:
                        pygame.draw.circle(screen, self.TAN, ((i*100)+50, (j*100)+50), 45)
                    else: 
                        pygame.draw.circle(screen, self.RED, ((i*100)+50, (j*100)+550), 45)  
        
                        
        
if __name__ == '__main__':
    b = GUI()