# foodstock.py
# Class to handle food bar 

import upygame as pygame
import graphics

class Food:
    def __init__(self):
        self.rungs = 10
        self.start = 81
        self.x = 3
        self.y = self.start
        self.space = 7
        
    # Draw
    def draw(self, screen, image):
        # Start at bottom and work up
        self.y = self.start
        for rungs in range(self.rungs):
            if (self.rungs < 4):
                screen.blit(image[2], self.x, self.y)
            elif (self.rungs < 6):
                screen.blit(image[1], self.x, self.y)
            else:
                screen.blit(image[0], self.x, self.y)
            self.y -= self.space
        
    # Remove a rung
    def removeFood(self):
        if (self.rungs > 0):
            self.rungs -= 1
    
    # Add a rung
    def addFood(self):
        if (self.rungs < 10):
            self.rungs += 1
            
    # Get stock
    def getStock(self):
        return self.rungs