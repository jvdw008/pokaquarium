# interface.py
# This is the class to create and draw the game interface itself and game instructions

import upygame as pygame
import graphics

class Interface:
    def __init__(self):
        self.x = 0  # interface x
        self.y = 0  # interface y
        self.infoX = 4
        self.lines = ["LEFT/RIGHT: move crab", "UP: feed pets", "DOWN: give medicine", "A: buy food (1 coin)", "B: buy medicine (3 coins)", "C: buy pet (10 coins)", "If you run out of hunger", "you lose a pet and all", "your coins.", "Buy required pet qty to", "beat the level."]
        
    # In-game graphics
    def draw(self, screen):
        screen.blit(graphics.interface, self.x, self.y)
        
    # Information text
    def showInstructions(self, umachine):
        self.infoY = 2
        self.colour = 4
        
        for line in self.lines:
            umachine.draw_text(self.infoX, self.infoY, line, self.colour)
            self.infoY += 8
            self.colour += 1