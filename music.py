# music.py

class Music:
    def __init__(self, snd, isThisRealHardware):
        self.isThisRealHardware = isThisRealHardware
        self.snd = snd
        
    def stopMusic(self):
        if (self.isThisRealHardware):
            self.snd.play_from_sd("dummy.raw")   # This file does not exist
        else:
            print ("music stopped")
        
    def playMenuMusic(self, menuSong):
        if (self.isThisRealHardware):
            self.snd.play_from_sd(menuSong)
        else:
            print ("menu song")
        
    def playGameMusic(self, gameSong):
        if (self.isThisRealHardware):
            self.snd.play_from_sd(gameSong)
        else:
            print ("game song")