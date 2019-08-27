# audio.py
# This class plays the sfx for the game

import upygame as pygame
import sounds               # The sound data

class Audio:
    def __init__(self, g_sound):
        self.sound = g_sound
        
    # Play Sfx
    def playButtonPress(self):
        self.sound.play_sfx(sounds.buttonPress8, len(sounds.buttonPress8), False)
        
    def playCoinCollected(self):
        self.sound.play_sfx(sounds.coinCollected8, len(sounds.coinCollected8), False)
        
    def playFishBought(self):
        self.sound.play_sfx(sounds.fishBought8, len(sounds.fishBought8), False)
        
    def playFishDeath(self):
        self.sound.play_sfx(sounds.fishDeath8, len(sounds.fishDeath8), False)
        
    def playGameOver(self):
        self.sound.play_sfx(sounds.gameOver8, len(sounds.gameOver8), False)
        
    def playHunger(self):
        self.sound.play_sfx(sounds.hunger8, len(sounds.hunger8), False)
        
    def playLevelUp(self):
        self.sound.play_sfx(sounds.levelUp8, len(sounds.levelUp8), False)
    