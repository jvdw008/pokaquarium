# flashtext.py
# This class displays in-game text and moves it up slowly before disappearing

import upygame as pygame
import umachine

class Text:
    def __init__(self, timer, text):
        self.startY = 55
        self.x = (120 - (len(text) * 5)) // 2   # Try center the text dynamically
        self.y = self.startY
        self.text = ""
        self.timer = timer  # Display duration
        self.moveTimer = 1  # Move text up timer
        self.text = text
        
    # Display text
    def draw (self):
        if (self.timer > 0):
            umachine.draw_text(self.x, self.y, self.text, 15)
        
    # Update display timer
    def update(self):
        self.timer -= 1
        if (self.moveTimer > 0):
            self.moveTimer -= 1
        else:
            self.moveTimer = 2
            self.y -= 1