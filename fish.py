# fish.py
# Class to create and manage fish

import upygame as pygame
import graphics
import urandom as random

class Fish:
    def __init__(self, speed, type):
        self.x = random.getrandbits(6) + 20
        self.y = random.getrandbits(4) + 20
        self.min = 14
        self.max = 76
        self.maxY = 45
        self.minY = 17
        self.moveCounter = 0
        self.moveMax = speed
        self.directionX = 1
        self.directionY = 1
        self.ill = False
        self.type = type
       
    # Draw fish - to do: add dead fish image
    def draw(self, screen, illness):
        if (self.directionX == 1):
            screen.blit(illness, self.x + 1, self.y + 7)
        else:
            screen.blit(illness, self.x + 2, self.y + 5)
            
    # Update movements of fish
    def update(self):
        self.moveCounter += 1
        moveOrNot = random.getrandbits(2) + 1
                
        if (self.moveCounter > self.moveMax):
            self.moveCounter = 0
            
            # Only move if random value is enough
            if (moveOrNot > 1):
                moveOrNot = 1
                
            # If value of random illness = 1
            illStart = random.getrandbits(7)
            if (illStart == 127):
                illness = random.getrandbits(7)
                if (illness > 120):
                    self.ill = True
                
            # X movement
            if (self.directionX == 1):
                self.x += moveOrNot
            else:
                self.x -= moveOrNot
        
            # Max X
            if (self.x > self.max):
                self.x = self.max
                self.directionX = -1
        
            # Min X 
            if (self.x < self.min):
                self.x = self.min
                self.directionX = 1
        
            # Max Y
            if (self.y > self.maxY):
                self.y = self.maxY
                self.directionY = -1
                
            # Min Y
            if (self.y < self.minY):
                self.y = self.minY
                self.directionY = 1
                
            # Y movement
            if (self.directionY == 1):
                self.y += random.getrandbits(1)
            else:
                self.y -= random.getrandbits(1)
                
        if (self.ill):
            return True
        else:
            return False
                
    # Get X and Y pos to spawn coin
    def getFishPos(self):
        return (self.x, self.y)

    # Set fish state
    def healFish(self):
        self.ill = False
        
    # Get fish health
    def getHealth(self):
        return self.ill
        
    # Get direction
    def getDirection(self):
        return self.directionX
        
    # Get fish type to render the right fish anim in the animation class
    def getType(self):
        return self.type