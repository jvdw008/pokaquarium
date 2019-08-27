# bubbles.py
# Class to display and manage bubbles on game screen

import upygame as pygame
import graphics
import urandom as random

class Bubbles:
    def __init__(self, bubbleList):
        self.startY = 100
        self.topY = 16
        self.bubbleList = bubbleList        # StartX, y, speed, size image
        self.image = [pygame.surface.Surface(14, 14, graphics.bubble1Pixels), pygame.surface.Surface(8, 7, graphics.bubble2Pixels), pygame.surface.Surface(4, 4, graphics.bubble3Pixels)]
        
    # Draw this bubble
    def draw(self, screen):
        for i in self.bubbleList:
            screen.blit(self.image[i[3] - 1], i[0], i[1])
        
    # Update bubble position
    
    def update(self):
        for i in self.bubbleList:
            #print(str(i[2]))
            i[1] -= i[2]
            
            # Off screen, so pop
            if (i[1] < self.topY):
                i[1] = self.startY
                # Set X
                newX = random.getrandbits(6) + 21
                i[0] = newX
                # Set speed
                i[2] = random.getrandbits(2) + 1
                # Image
                i[3] = random.getrandbits(2)
            