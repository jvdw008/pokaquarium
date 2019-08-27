# coin.py
# Class to handle the coins tumbling down the game screen

import upygame as pygame
import graphics
import urandom as random

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
    
    # Draw
    def draw(self, screen, image):
        screen.blit(image, self.x, self.y)
    
    # Update coin
    def update(self):
        self.y += self.speed
        
        if (self.y > 90):
            return False
        else:
            return True
    
    # Has coin been caught by player?
    def checkCapture(self, x, y):
        # Is player underneath?
        if ((x - 2 < self.x) and (x + 34 > self.x)):
            if (self.y > y - 5):
                return True
            else:
                return False
        else:
            return False
            
    # Get X pos
    def returnX(self):
        return self.x
        
    # Get Y pos
    def returnY(self):
        return self.y