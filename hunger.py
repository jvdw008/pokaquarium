# hunger.py
# Class to handle the hunger bar of fish in aquarium

import upygame as pygame
import graphics

class Hunger:
    def __init__(self, max):
        self.rungs = 10
        self.start = 81
        self.x = 101
        self.y = self.start
        self.space = 7
        self.counterMax = max
        self.counter = self.counterMax
        self.state = 1      # 1 for alive, 0 for dead
        
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
        
    # Update - drops the food stock based on the qty of fish in tank
    def update(self, qtyFish):
        if (qtyFish > 0):
            self.counter -= 1
            if (self.counter <= 0):
                # Take off one hunger
                if (self.rungs > 0):
                    self.rungs -= 1
                    self.counter = self.counterMax // qtyFish
                else:
                    self.state = 0
    
    # Add a rung
    def addFood(self):
        if (self.rungs < 10):
            self.rungs += 2
            if (self.rungs > 10):
                self.rungs = 10
            
    # Add medicine
    def addMedicine(self):
        for i in range (4):
            if (self.rungs < 10):
                self.rungs += 1
            
    # Get hunger level
    def getHunger(self):
        return self.rungs
        
    # Reset hunger after fish death
    def resetHunger(self):
        self.rungs = 10