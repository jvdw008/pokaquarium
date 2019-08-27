# background.py
# This is the class to create and draw the game aquarium graphics itself

import upygame as pygame
import graphics

class Background:
    def __init__(self):
        self.x = 12
        self.y = 16
        
    # Pass in the aquarium graphics
    def draw(self, screen, bg):
        screen.blit(bg, self.x, self.y)