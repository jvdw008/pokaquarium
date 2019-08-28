# Copyright 2019 by Blackjet
# Graphics done using Aseprite
# Sfx done using BFXR and Audacity
# Code by Jaco van der Walt

# The source code in this file is released under the GNU GPL V3 license.
# Go to https://choosealicense.com/licenses/gpl-3.0/ for the full license details.

import upygame as pygame
import urandom as random
import umachine                             # For on-screen text
import graphics		                        # Graphics
from audio import Audio                     # Audio class to play sounds
from music import Music                     # Music stuff
from interface import Interface             # Game interface
from background import Background           # Background (aquarium)
from player import Player                   # Player class
from bubbles import Bubbles                 # Bubbles class
from fish import Fish                       # Fish class
from coin import Coin                       # Dropping coins
from foodstock import Food                  # Fish food stock
from hunger import Hunger                   # Fish hunger object
from flashtext import Text                  # On-screen text for important messages in-game
from animation import Animation as Anim     # Animation cass for fish, coins, player etc

#import gc
#gc.collect()

# Setup the screen buffer
pygame.display.init(False)
pygame.display.set_palette_16bit([
    000000, 0xf766, 0xdb64, 0x20e6, 0x64df, 0x5b7b, 0xd2ac, 0xa186, 0xd4ec, 0x8aa7, 0x65c5, 0x4b25, 0x4127, 0x9556, 0x83f0, 0xffff
    
]);
screen = pygame.display.set_mode() # default mode of 110x88 @16 cols

# Init audio
g_sound = pygame.mixer.Sound()

# Test for real h/w to prevent simulator from hanging
menuSong = ""
gameSong = ""

gpioPin = umachine.Pin ( umachine.Pin.EXT2, umachine.Pin.ANALOG_IN )
gpioPinValue = gpioPin.value()
if(gpioPinValue == 0):
    isThisRealHardware = False
else:
    isThisRealHardware = True
    menuSong = "pokaquar/mSong.wav"
    gameSong = "pokaquar/gSong.wav"

# Variables
version = 10                    # Version number of current game build

gameState = 0                   # Menu or game
gameOver = False
startGame = False               # Boolean for starting the game
showInstructions = False        # For showing instructions on menu screen
bubbleList = []                 # List of bubbles
fishList = []                   # List of fish in tank
level = 1                       # The level of the game
maxFish = 6                     # Max fish per tank, these changes per level
moveX = 0                       # Default player movement
inertia = 1                     # Initial player speed
coins = 0                       # Player money
medicine = 0                    # Medicine qty for healing fish
score = 0                       # Player score
coinList = []                   # This is the coins dropping down the tank at any given time
chanceOfDrop = 0                # Random value for coin drop chances
playerPos = []                  # Player position for coin drop checks
coinCaught = False              # Boolean for adding coin/score to player
foodStock = 100                 # Max food stock you can have
fishHunger = 100                # Fish at their fullest
foodCost = 1                    # Price of item
medicineCost = 3                # Price of item
fishCost = 10                   # Price of item
upPressed = False               # Modifiers for dpad
downPressed = False             # As above
aPressed = False                # As above
bPressed = False                # As above
cPressed = False                # As above
musicEnabled = True             # Toggle for music
musicIsPlaying = True           # Default to play music on load
hungerMax = 700                 # Start value for rate hunger drops for fish - this is also used to increase feding rate as you level up
fishQty = 0                     # Total fish in tank for checking gameover state
sickFishQty = 0                 # Total sick fish
flashTextTimer = 60             # On-screen text timer
difficulty = 35                 # This value is used to adjust the frequency of coin drops - lower value is harder - keep between 30-40
gameOverPlayed = False          # Trigger to pay gameover sound when dead
aquariumBg = [graphics.bg1, graphics.bg2, graphics.bg3, graphics.bg4, graphics.bg5]

# Init classes
interface = Interface()
bg = Background()
player = Player()
food = Food()
hunger = Hunger(hungerMax)
audio = Audio(g_sound)
tmusic = Music(g_sound, isThisRealHardware)

# Animation setup - Array of graphic images and the speed of the animation (lower = faster)
coinAnim = Anim([graphics.coin, graphics.coin1], 3)
fish1AnimSpeed = random.getrandbits(3) + 1
fish1AnimLeft = Anim([graphics.fish1_left, graphics.fish1_left1], fish1AnimSpeed)
fish1AnimRight = Anim([graphics.fish1_right, graphics.fish1_right1], fish1AnimSpeed)
fish2AnimLeft = Anim([graphics.fish2_left, graphics.fish2_left1], fish1AnimSpeed)
fish2AnimRight = Anim([graphics.fish2_right, graphics.fish2_right1], fish1AnimSpeed)
jellyAnim = Anim([graphics.jelly1, graphics.jelly2], fish1AnimSpeed)
playerAnimLeft = Anim([graphics.crab1_left, graphics.crab2_left], 3)
playerAnimRight = Anim([graphics.crab1_right, graphics.crab2_right], 3)
playerAnimIdle = Anim([graphics.crab_idle1, graphics.crab_idle2, graphics.crab_idle1], 20)

# Set up bubbles
for i in range(6):
    startX = random.getrandbits(2) * 10 + 10
    startY = 100
    bubbleSpd = random.getrandbits(2)
    bubbleSize = random.getrandbits(2)
    bubbleList.append([startX, startY, bubbleSpd, bubbleSize])

bubbles = Bubbles(bubbleList)
        		        
# Set up single fish
fishList.append(Fish(random.getrandbits(1) + 1, random.getrandbits(2)))
coinList.append(Coin(0, 89))    # Nasty hack to spawn the initial coin, as you can't catch the first one!!!?

# Start music
tmusic.playMenuMusic(menuSong)
                                
#print ("free",gc.mem_free())
# Main loop
while True:
    # Read keys
    eventtype = pygame.event.poll()
    if eventtype != pygame.NOEVENT:

        # Keydown events
        if eventtype.type == pygame.KEYDOWN:
            if (not gameOver):
                if (eventtype.key == pygame.K_UP):
        		    if (gameState == 1):
        		        # Feed fish
        		        if (not upPressed):
        		            # Only add food if you have stock and fish hunger is less than full
        		            if (food.getStock() > 0 and hunger.getHunger() < 10):
        		                hunger.addFood()
        		                food.removeFood()
        		                upPressed = True
        		                audio.playHunger()
        		                
                if (eventtype.key == pygame.K_RIGHT):
                    moveX += inertia
                
                if (eventtype.key == pygame.K_DOWN):
                    if (gameState == 1):
                        if (medicine > 0):
                            medicine -= 1
                            
                            # Apply medicine to fish
                            for fish in fishList:
                                fish.healFish()
                                
                            # Tell player
                            flashText = Text(flashTextTimer, "PETS HEALED")
                
                if (eventtype.key == pygame.K_LEFT):
        		    moveX -= inertia

            if (eventtype.key == pygame.BUT_C):
                if (gameState == 1):
    		        # Buy fish
                    if (len(fishList) < maxFish and coins >= fishCost):
                        fishList.append(Fish(random.getrandbits(1) + 1, random.getrandbits(2)))
                        coins -= fishCost
                        audio.playButtonPress()
                        if (len(fishList) < maxFish):
                            flashText = Text(flashTextTimer, "NEW PET PURCHASED")
                            audio.playFishBought()
    		            
                    #########################################################################################
                    # Check if player has maxFish fish, if so, win level
                    #########################################################################################
                    if (len(fishList) >= maxFish):
                        level += 1
                        if (level > 5):
                            # You won!
                            gameState = 3
                            
                        else:
                            audio.playLevelUp()
                            maxFish += 1
                            coinList = []   # Empty dropping coins objects
                            coinList.append(Coin(0, 89))
                            gameState = 2
                            flashText = Text(flashTextTimer, "- BUY " + str(maxFish) + " PETS -")
                            
                if (gameState == 0):
                    if (not musicEnabled and not cPressed):
                        if (not musicIsPlaying):
                            musicIsPlaying = True
                            musicEnabled = True
                            cPressed = True
                            tmusic.playMenuMusic(menuSong)
                            
                    if (musicEnabled and not cPressed):
                        if (musicIsPlaying):
                            musicIsPlaying = False
                            musicEnabled = False
                            cPressed = True
                            tmusic.stopMusic()
    		        
            if (eventtype.key == pygame.BUT_B):
                audio.playButtonPress()
                if (gameState == 0):
    		        # Show info
    		        showInstructions = True
    		        
                else:
                    if (not gameOver):
        		        if (coins >= medicineCost):
        		            medicine += 1
        		            coins -= medicineCost
                    
            if (eventtype.key == pygame.BUT_A):
                if (gameState == 0):
                    #########################################################################################
                    # Start game
                    #########################################################################################
                    if (not startGame):
        		        startGame = True
        		        gameState = 1
        		        gameOver = False
        		        flashText = Text(1, "")
        		        flashText = Text(flashTextTimer, "- BUY " + str(maxFish) + " PETS -")
        		        audio.playButtonPress()
        		        if (musicEnabled):
        		            tmusic.playGameMusic(gameSong)
    		        
                elif (gameState == 1):
                    #########################################################################################
                    # Reset game
                    #########################################################################################
                    if (gameOver):
                        gameState = 0
                        startGame = False
                        maxFish = 6
                        fishList = []
                        fishList.append(Fish(random.getrandbits(1) + 1, random.getrandbits(2)))
                        food = Food()
                        hunger = Hunger(hungerMax)
                        coins = 0
                        medicine = 0
                        score = 0
                        level = 1
                        sickFishQty = 0
                        if (musicEnabled):
        		            tmusic.playMenuMusic(menuSong)
                        
                    else:
                        # Buy food
                        if (coins > 0):
                            food.addFood()
                            coins -= foodCost
                elif (gameState == 2):
                    #########################################################################################
                    # gameState 2 - set up next level graphics etc TO DO ***
                    #########################################################################################
                    bubbleList = []
                    fishList = []
                    fishList.append(Fish(random.getrandbits(1) + 1, random.getrandbits(2)))
                    food = Food()
                    hunger = Hunger(hungerMax)
                    gameState = 1
                
                else:
                    #########################################################################################
                    # PLAYER WON
                    #########################################################################################
                    gameState = 0
                    startGame = False
                    maxFish = 6
                    fishList = []
                    fishList.append(Fish(random.getrandbits(1) + 1, random.getrandbits(2)))
                    food = Food()
                    hunger = Hunger(hungerMax)
                    coins = 0
                    medicine = 0
                    score = 0
                    level = 1
                    sickFishQty = 0
                    
    		
        # Keyup events
        if eventtype.type == pygame.KEYUP:

            if (eventtype.key == pygame.K_UP):
    		    upPressed = False
    		    
            if (eventtype.key == pygame.K_RIGHT):
                moveX = 0
    		        
            if (eventtype.key == pygame.K_LEFT):
                moveX = 0

            if (eventtype.key == pygame.BUT_C):
                cPressed = False
                
            if (eventtype.key == pygame.BUT_B):
                if (gameState == 0):
                    showInstructions = False
            
            if (eventtype.key == pygame.BUT_A):
                if (gameState == 1):
                    if (not gameOver):
                        aPressed = False
                        
	# Update
    if (gameState == 1):
        player.movePlayer(moveX)
        if (moveX < 0):
            playerAnimLeft.update()
            
        if (moveX > 0):
            playerAnimRight.update()
            
        if (not moveX):
            playerAnimIdle.update()
        
        bubbles.update()
        fishQty = len(fishList)
        hunger.update(fishQty)
        flashText.update()
        sickFishQty = 0
        # Check for game over state
        if (hunger.getHunger() <= 0):
            # Lose a fish, lose your coins
            if (len(fishList) > 0):
                del fishList[fishQty - 1]
                hunger.resetHunger()
                coins = 0
                flashText = Text(flashTextTimer, "PET LOST")
                audio.playFishDeath()
                
        # No fish in tank
        if (fishQty <= 0):
            gameOver = True
            if (not gameOverPlayed):
                audio.playGameOver()
                gameOverPlayed = True
        
        # Update fish
        for fish in fishList:
            fishType = fish.getType()
            # Update fish positions
            fish.update()
            # Update animation of fish
            if (fish.getDirection() == -1):
                if (fishType >= 2):
                    fish1AnimLeft.update()
                elif (fishType == 1):
                    fish2AnimLeft.update()
                else:
                    jellyAnim.update()
            else:
                if (fishType >= 2):
                    fish1AnimRight.update()
                elif (fishType == 1):
                    fish2AnimRight.update()
                else:
                    jellyAnim.update()
                
            # Get X/Y co-ord to see if we spawn a coin
            fishPos = fish.getFishPos()
            if (fishPos[1] < (difficulty - (fishQty * 2))):
                #################################################################
                # COIN DROP - Create new coin at x/y pos of fish and only if fish is not sick
                #################################################################
                chanceOfDrop = random.getrandbits(7)
                if (len(fishList) > 1):
                    if (fish.getHealth() == False and chanceOfDrop < 1):     # ie, fish healthy
                            coinList.append(Coin(fishPos[0], fishPos[1]))
                else:
                    # Only one fish, don't stop the fish from dropping a coin
                    if (chanceOfDrop < 1):
                        # If your only fish is sick, unsick it.
                        if (fish.getHealth()):
                            fish.healFish()
                            
                        coinList.append(Coin(fishPos[0], fishPos[1]))
                        
            # Add up total sick fish
            if (fish.getHealth()):
                sickFishQty += 1
            
        # Check if player caught coin
        playerPos = player.getPlayerPos()
        
        # Update coin list
        coinID = 0
        removeCoinId = 0
        for coin in coinList:
            # Animate it
            coinAnim.update()
            if (coin.checkCapture(playerPos[0], playerPos[1])):
                coinCaught = True
                removeCoinId = coinID
                audio.playCoinCollected()
                
            coinOnScreen = coin.update()
            # Is coin on screen still?
            if (not coinOnScreen):
                removeCoinId = coinID
                
            coinID += 1
            
        # Del coin
        if (removeCoinId != 0):
            del coinList[removeCoinId]
            
            if (coinCaught):
                coins += 1
                score += 10
                coinCaught = False
                    
    else:
        # Move fish on menu to improve random - this is also moving the fish when reachign 10 fish in aquarium, ie gameState 3
        for fish in fishList:
            fish.update()
        
	###########################################################################
	# Render
    screen.fill(0)  # Clear screen
    if (gameState == 0):
        if (showInstructions):
            interface.showInstructions(umachine)
        else:
            screen.blit(graphics.logo, 10, 10)
            umachine.draw_text(30, 40, "A: START", 1)
            umachine.draw_text(30, 47, "B: INFO (hold)", 15)
            umachine.draw_text(30, 54, "C: TOGGLE MUSIC", 2)
            umachine.draw_text(16, 62, "by Blackjet in 2019", 8)
            umachine.draw_text(87, 82, "v0." + str(version), 14)
    elif (gameState == 1):
        
        # Draw aquarium
        bg.draw(screen, aquariumBg[level - 1])
        # Draw falling coins
        if (len(coinList) > 0):
            for coin in coinList:
                coinAnim.draw(screen, coin.returnX(), coin.returnY())
        
        # Draw interface
        interface.draw(screen)
        # Draw coins
        umachine.draw_text(29, 4, str(coins), 15)
        # Draw medicine
        umachine.draw_text(63, 4, str(medicine), 15)
        # Draw score
        umachine.draw_text(74, 7, str(score), 10)
        # Draw food stock
        food.draw(screen, [graphics.food, graphics.warning, graphics.danger])
        # Draw hunger
        hunger.draw(screen, [graphics.hunger, graphics.warning, graphics.danger])
        # Draw fish qty
        umachine.draw_text(13, 16, "Pets: " + str(fishQty) + "/" + str(maxFish), 1)
        # Draw sick fish
        umachine.draw_text(70, 16, "Sick: " + str(sickFishQty), 15)
        # Draw level
        umachine.draw_text(68, 81, "Level: " + str(level), 15)
        
        # Draw fish
        for fish in fishList:
            fishType = fish.getType()
            if (fish.getDirection() == -1):
                # Left
                if (fishType >= 2):
                    fish1AnimLeft.draw(screen, fish.getFishPos()[0], fish.getFishPos()[1])
                elif (fishType == 1):
                    fish2AnimLeft.draw(screen, fish.getFishPos()[0], fish.getFishPos()[1])
                else:
                    jellyAnim.draw(screen, fish.getFishPos()[0], fish.getFishPos()[1])
            else:
                # right
                if (fishType >= 2):
                    fish1AnimRight.draw(screen, fish.getFishPos()[0], fish.getFishPos()[1])
                elif (fishType == 1):
                    fish2AnimRight.draw(screen, fish.getFishPos()[0], fish.getFishPos()[1])
                else:
                    jellyAnim.draw(screen, fish.getFishPos()[0], fish.getFishPos()[1])
                
            # Draw illness if needed
            if (fish.getHealth()):
                fish.draw(screen, graphics.ick)
        
        # Draw player
        if (player.getDirection() == 1):
            if (not moveX):
                #player.draw(screen, graphics.crab1_right)
                playerAnimIdle.draw(screen, playerPos[0], playerPos[1])
            else:
                playerAnimRight.draw(screen, playerPos[0], playerPos[1])
                
        else:
            if (not moveX):
                #player.draw(screen, graphics.crab1_left)
                playerAnimIdle.draw(screen, playerPos[0], playerPos[1])
            else:
                playerAnimLeft.draw(screen, playerPos[0], playerPos[1])
        
        # Draw bubbles
        bubbles.draw(screen)
        
        # Draw flash text
        flashText.draw()
        # Draw game over text
        if (gameOver == True):
            umachine.draw_text(34, 45, "GAME OVER", 15)
            
    elif (gameState == 2):
        # gameState 2
        screen.blit(graphics.winLevel, 0, 0)
        umachine.draw_text(20, 66, "AQUARIUM COMPLETE", 15)
        umachine.draw_text(20, 74, "Press A for level " + str(level), 1)
        
    else:
	    # Beat the game
	    screen.blit(graphics.winGame, 0, 0)
	    umachine.draw_text(38, 59, "YOU WON!", 10)
	    umachine.draw_text(12, 67, "Your final score was:", 1)
	    umachine.draw_text(40, 74, ">> " + str(score) + " <<", 4)
	    umachine.draw_text(20, 82, "Press A for menu", 15)
	    
	# Sync screen
    pygame.display.flip()
    