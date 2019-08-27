# player.py
# Class to handle player control and management

import upygame as pygame
import graphics

# The anial the player controls
class Player:
    def __init__(self):
        self.playerX = 30    # Start X
        self.playerY = 60    # Start Y
        self.min = 9        # Left clamp
        self.max = 70        # Right clamp
        self.direction = 1   # 1 for right, 0 for left
        
    # Draw player
    def draw(self, screen, image):
        screen.blit(image, self.playerX, self.playerY)
        
    # Get current direction
    def getDirection(self):
        return self.direction
        
    # Move player
    def movePlayer(self, x):
        if (x < 0):
            self.direction = 0
        elif (x > 0):
            self.direction = 1
            
        self.playerX += x
        
        if (self.playerX > self.max):
            self.playerX = self.max
            
        if (self.playerX < self.min):
            self.playerX = self.min
            
    # Get player pos for coin capture
    def getPlayerPos(self):
        return (self.playerX, self.playerY)