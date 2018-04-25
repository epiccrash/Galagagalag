# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# This code is used to import Austin's module manager; much thanks to him!
# https://raw.githubusercontent.com/CMU15-112/module-manager/master/module_manager.py
import module_manager
module_manager.review()

# Module imports
import pygame
import random

# Class imports
from pygamegame import PygameGame
from Star import Star
from Player import Player
from Attack import *
from Enemy import *
from Powerup import *

# Main Game object; used for running the game
class Game(PygameGame):
    
    # Initializing data; set a default game state for easy reset
    def init(self, givenState = 1, stars = pygame.sprite.Group()):
        # Background color of window and basic small font size
        self.bgColor = (0, 0, 0)
        self.fontSize = 24
        # Load custom font
        # Downloaded from https://fonts.google.com/specimen/Press+Start+2P?selection.family=Press+Start+2P
        # Created by CodeMan38; license included in folder
        self.font = pygame.font.Font(
            "Press_Start_2P/PressStart2P-Regular.ttf", self.fontSize)
        self.titleFont = pygame.font.Font(
            "Press_Start_2P/PressStart2P-Regular.ttf", 2 * self.fontSize + 8)
        self.smallFont = pygame.font.Font(
            "Press_Start_2P/PressStart2P-Regular.ttf", 16)
        # Set the wave count
        self.wave = 1
        # Life counter; currently unused
        self.lives = 3
        # Used for spawning and top/bottom padding (currently enemies use it)
        self.ypadding = 48
        # Set the player's score
        self.score = 0
        # Define the states of the game
        self.info = -1
        self.editor = 0
        self.titleScreen = 1
        self.gamePlaying = 2
        self.gameOver = 3
        # Set a variable to track the state of the game
        self.gameState = givenState
        # Make a variable of the stars to draw, depending on whether any exist
        self.stars = stars

        # Create a new initial group of stars if none exist
        if len(self.stars) == 0:        
            for row in range(0, self.height + 1):
                self.makeStars(row)
        
        # Create the Player object, place in a single group
        Player.init()
        self.player = Player(self.width / 2, self.height - self.ypadding - 32)
        self.playerGroup = pygame.sprite.GroupSingle(self.player)

        # Booleans for autofiring and laser control
        self.autofireEnabled = False
        self.laserEnabled = True
        self.singleShot = True
        self.doubleShot = False
        # Recharge time on lasers, along with counting variable
        self.rechargeTime = 25
        self.cooldownCount = 0
        # Initialize group for lasers
        self.playerLasers = pygame.sprite.Group()

        # Create a sprite group for the enemies
        self.enemyGroup = pygame.sprite.Group()
        
        # Create drone sprite group
        self.droneGroup = pygame.sprite.GroupSingle()
        
        # Generate enemies
        self.generateEnemies()
        
        # Create enemy laser group
        self.enemyLasers = pygame.sprite.Group()
        
        # Create powerups group
        self.powerups = pygame.sprite.Group()
        
    # Changing game or game data
    def timerFired(self, dt):
        # Generate stars again and then update them
        self.makeStars()
        self.stars.update(self.width, self.height)
        
        # Check to see if at the "game" stage
        if self.gameState == self.gamePlaying:
            self.updatePlay()
        else:
            self.updateKeys()
        
    # Draw everything onto screen
    def redrawAll(self, screen):
        self.stars.draw(screen)
        # Draw the title screen if it corresponds to the game state
        if self.gameState == self.titleScreen:
            self.drawTitleScreen(screen)
        # check to see if the game is being played
        elif self.gameState == self.gamePlaying:
            # Draw all entities
            self.playerLasers.draw(screen)
            self.playerGroup.draw(screen)
            self.enemyLasers.draw(screen)
            self.enemyGroup.draw(screen)
            self.powerups.draw(screen)
            # Draw the player's score and lives on the screen
            self.drawScore(screen)
            self.drawLives(screen)
        # Check to see if player lost game
        elif self.gameState == self.gameOver:
            self.drawLoseScreen(screen)
    
    # Updates the game when it's being played
    def updatePlay(self):
        # Update attacks
        self.updatePlayerAttacks()
        self.updateEnemyAttacks()
        # Check for object collisions
        self.checkCollisions()
        # Update the player object, check for keypresses
        self.playerGroup.update(self.isKeyPressed, self.width, self.height)
        # Enable/Disable autofire depending on caps lock state
        if pygame.key.get_pressed()[pygame.K_CAPSLOCK]:
            self.autofireEnabled = True
        else:
            self.autofireEnabled = False
        # Give the player's coordinates to enemies
        for enemy in self.enemyGroup:
            enemy.storeDest(enemy, (self.player.x, self.player.y))
        # Update enemies in enemy group
        self.enemyGroup.update(self.width, self.height)
        # Make more enemies if there aren't any remaining and increase wave
        if len(self.enemyGroup) == 0:
            self.wave += 1
            self.generateEnemies()
        # Update the powerups
        self.powerups.update(self.width, self.height)
    
    # Updates the game state according to keypresses
    def updateKeys(self):
        # Create the title screen and start playing if Enter is pressed
        if self.gameState == self.titleScreen:
            if self.isKeyPressed(pygame.K_RETURN):
                self.gameState = self.gamePlaying
            # If Tab is pressed, set the game state to be the ship editor
            elif self.isKeyPressed(pygame.K_TAB):
                self.gameState = self.editor
            # If H is pressed, set the game state to be the help popup
            elif self.isKeyPressed(pygame.K_h):
                self.gameState = self.info
        # Check to see if the game is at the "over" stage
        elif self.gameState == self.gameOver:
            # If the r key is pressed, restart the game
            if self.isKeyPressed(pygame.K_r):
                self.init(self.gamePlaying, self.stars)
            # If the q key is pressed, quit to the title screen
            elif self.isKeyPressed(pygame.K_q):
                self.init(self.titleScreen, self.stars)

    # Updates the player's attacks
    def updatePlayerAttacks(self):
        # Update the player lasers
        self.playerLasers.update(self.width, self.height)
        # Fire lasers if spacebar is pressed or if autofire is enabled
        if ((self.isKeyPressed(pygame.K_SPACE) or self.autofireEnabled) 
            and self.laserEnabled):
            # Get player sprite, set laser spawns accordingly
            xSpawn, ySpawn = self.player.x, self.player.y - self.player.yradius
            # Fire lasers on whether single shot and/or double shot are enabled
            if self.singleShot:
                self.playerLasers.add(PlayerLaser(xSpawn, ySpawn))
            if self.doubleShot:
                self.playerLasers.add(PlayerLaser(
                    xSpawn - (self.player.xradius - 2), 
                    ySpawn + self.player.yradius))
                self.playerLasers.add(PlayerLaser(
                    xSpawn + (self.player.xradius - 2), 
                    ySpawn + self.player.yradius))
            # Disable laser firing for cooldown
            self.laserEnabled = False
        # Check if cooldown time count equals the recharge time
        if not self.laserEnabled:
            self.updateLaserCooldown()
    
    # Updates the laser cooldown
    def updateLaserCooldown(self):
        # If so, enable firing again
        if self.cooldownCount == self.rechargeTime:
            self.laserEnabled = True
            self.cooldownCount = 0
        # Otherwise, just increase the cooldown time count
        else:
            self.cooldownCount += 1
    
    # Update all enemy attacks
    def updateEnemyAttacks(self):
        # Update the enemy lasers
        self.enemyLasers.update(self.width, self.height)
        # Loop through enemies in group and fire lasers at their position
        # Placeholder: random chance not conditioning on time
        for enemy in self.enemyGroup:
            if enemy.attChance != 0:
                if random.randint(0, enemy.attChance) == enemy.attChance:
                    self.enemyLasers.add(EnemyLaser(enemy.x, 
                        enemy.y + enemy.yradius / 2))
    
    # Check for collisions between objects
    def checkCollisions(self):
        # Check collisions between player, attacks, and enemies
        self.checkPrimaryEnemyCollisions()
        # Check collisions between drone, player, attacks, and enemies
        self.checkDroneCollisions()
        
        # Affect player if they hit a powerup
        for powerup in (pygame.sprite.groupcollide(
            self.powerups, self.playerGroup, True, False,
            pygame.sprite.collide_rect)):
                self.changePlayer(powerup)
        
        # Game ends if player has no lives left
        if self.lives == 0:
            self.gameState = self.gameOver
            
        # Remove enemy if its HP is at or below 0
        for enemy in self.enemyGroup:
            if enemy.hp <= 0:
                # Spawn a powerup/powerdown
                if random.randint(0, 1) == 0:
                    self.spawnPowerup(enemy.x, enemy.y)
                # Increase score and kill sprite if enemy is killed
                self.score += enemy.score
                enemy.kill()        
    
    # Checks collisions occurring between player, attacks, and enemies
    def checkPrimaryEnemyCollisions(self):
        # Remove a player laser if it hits an enemy
        for enemy in pygame.sprite.groupcollide(
            self.enemyGroup, self.playerLasers, False, True,
            pygame.sprite.collide_rect):
            # Reduce enemy HP; enemy is removed if HP drops to zero
            enemy.hp -= 1
        
        # Remove an enemy laser if if hits the player
        if (not self.player.isInvulnerable() and not 
            self.player.dashing and 
            pygame.sprite.groupcollide(
            self.playerGroup, self.enemyLasers, False, True,
            pygame.sprite.collide_rect)):
                # Reduce player lives
                self.lives -= 1
                self.player.invulnTime = 0
        
        # Hurt player if they hit an enemy
        if (not self.player.isInvulnerable() and not 
            self.player.dashing and
            pygame.sprite.groupcollide(
            self.playerGroup, self.enemyGroup, False, False,
            pygame.sprite.collide_rect)):
                # Reduce player lives
                self.lives -= 1
                self.player.invulnTime = 0
    
    # Checks collisions occurring between drone, player, attacks, and enemies
    def checkDroneCollisions(self):
        # Performs same function as enemy group above, but removes drone sprite
        if (pygame.sprite.groupcollide(
            self.playerGroup, self.droneGroup, False, True,
            pygame.sprite.collide_rect)):
                pass

        # Remove drone from overall enemy group
        self.enemyGroup.remove(self.droneGroup)        
        # Checks if drone hits another enemy
        for enemy in pygame.sprite.groupcollide(
            self.enemyGroup, self.droneGroup, False, True,
            pygame.sprite.collide_rect):
                # If so, reduce the enemy's hp by 2
                enemy.hp -= 2
        # Re-add drone
        self.enemyGroup.add(self.droneGroup)
        
        # Checks if an enemy laser hits a drone; if so, remove both from game
        if pygame.sprite.groupcollide(
            self.enemyLasers, self.droneGroup, True, True,
            pygame.sprite.collide_rect):
                pass
    
    # Generates enemies in the window (currently only respawns Invader)
    def generateEnemies(self):
        # Initialize enemies
        Invader.init()
        DiveBomber.init()        
        Drone.init()
        # Set the lower and upper bounds of how many enemies can spawn
        if self.wave >= 5:
            lowerBound = 4
        else:
            lowerBound = self.wave
        if self.wave >= 9:
            upperBound = 8
        else:
            upperBound = self.wave
        # Randomly decide the amount of enemies that can spawn from the bounds
        enemyCount = random.randint(lowerBound, upperBound)
        # If the wave is at least 8, 1/5th chance of spawning a drone
        if self.wave >= 8 and random.randint(0, 4) == 0:
            drone = Drone(self.player.x, self.player.y - 100)
            self.droneGroup.add(drone)
            self.enemyGroup.add(self.droneGroup)
        for enemyNum in range(1, enemyCount + 1):
            # Decide which enemy to spawn
            enemyChance = random.randint(0, 3)
            # If the wave is at least 3, 1/4th chance of spawning a divebomber
            if self.wave >= 3 and enemyChance == 0:
                bomber = DiveBomber(self.player.x, -32 * enemyNum ** 3)
                self.enemyGroup.add(bomber)
            # Otherwise, spawn in an Invader
            else:
                invader = Invader(-41 * 2.5 * enemyNum, self.ypadding + 30)
                self.enemyGroup.add(invader)
    
    # Draws the score
    def drawScore(self, screen):
        # Draw the score and the wave number
        score = self.font.render("SCORE: %d" % self.score, True, 
            (255, 255, 255))
        wave = self.font.render("WAVE: %d" % self.wave, True, (255, 255, 255))
        wave_rect = wave.get_rect(topright = [self.width - 14, 14])
        # Create a black score box
        scoreBox = pygame.Surface((self.width, self.ypadding), pygame.SRCALPHA)
        scoreBox.fill((50, 100, 50))
        # Place the box, score, and wave number on the screen
        screen.blit(scoreBox, [0, 0])
        screen.blit(score, [14, 14])
        screen.blit(wave, wave_rect)
    
    # Draw the number of lives remaining
    def drawLives(self, screen):
        # Draw the lives remaining
        lives = self.font.render("LIVES: %d" % self.lives, True, 
            (255, 255, 255))
        lives_rect = lives.get_rect(bottomleft = [14, self.height - 10])
        # Create a boxc for the lives remaining
        livesBox = pygame.Surface((self.width, self.height - self.ypadding),
            pygame.SRCALPHA)
        livesBox.fill((50, 50, 100))
        # Place the box and lives on the screen
        screen.blit(livesBox, [0, self.height - self.ypadding])
        screen.blit(lives, lives_rect)
    
    # Draws the title screen
    def drawTitleScreen(self, screen):
        # Easy definition for the color white
        white = (255, 255, 255)
        # Draw main title
        title = self.titleFont.render("Galagagalag", True, white)
        title_rect = title.get_rect(center = [self.width / 2, self.height / 4])
        # Draw subtitle
        subtitle = self.font.render("A Galaga-style Shooter", True, white)
        subtitle_rect = subtitle.get_rect(center = [self.width / 2, 
            self.height / 3])
        # Draw the title options
        self.drawTitleOptions(screen)
        # Draw author text
        author = self.smallFont.render("Joey Perrino", True, white)
        author_rect = author.get_rect(center = [self.width / 2, 
            self.height - 2 * self.fontSize])
        # Draw term project text
        tpText = self.smallFont.render("CMU 15-112 Spring 2018 Term Project", 
            True, (255, 255, 0))
        tpText_rect = tpText.get_rect(center = [self.width / 2, 
            self.height - self.fontSize])
        
        # Place the title, subtitle, and TP info on screen
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)
        screen.blit(author, author_rect)
        screen.blit(tpText, tpText_rect)
    
    # Draws the options on the title screen
    def drawTitleOptions(self, screen):
        # Draw Play option
        play = self.font.render("[Enter] Play", True, (255, 0, 0))
        play_rect = play.get_rect(center = [self.width / 2, 
            2 * self.height / 3 - 1.5 * self.fontSize])
        # Draw Help option (currently does nothing)
        info = self.font.render("[H] Help", True, (0, 255, 0))
        info_rect = info.get_rect(center = [self.width / 2,
            2 * self.height / 3])
        # Draw Edit option (currently does nothing)
        edit = self.font.render("[Tab] Ship Editor", True, (0, 0, 255))   
        edit_rect = edit.get_rect(center = [self.width / 2, 
            2 * self.height / 3 + 1.5 * self.fontSize])
        
        # Place the options on screen
        screen.blit(play, play_rect)
        screen.blit(info, info_rect)
        screen.blit(edit, edit_rect)
    
    # Draws the screen displayed when the game is lost
    def drawLoseScreen(self, screen):
        # Referenced for centering text: https://stackoverflow.com/questions/23982907/python-library-pygame-centering-text
        # Create text for final score
        final = self.font.render("Final score:", True, (255, 255, 255))
        final_rect = final.get_rect(center = [self.width / 2, self.height / 3])
        score = self.font.render(str(self.score), True, (255, 255, 255))
        score_rect = score.get_rect(center = [self.width / 2, self.height / 3 
            + 1.5 * self.fontSize])
        # Create information on replaying the game
        redo = self.font.render("[R] Replay", True, (255, 0, 0))
        redo_rect = redo.get_rect(center = [self.width / 2, 
            2 * self.height / 3])
        # Create information on quitting to the title screen
        quit = self.font.render("[Q] Quit to title", True, (0, 0, 255))
        quit_rect = quit.get_rect(center = [self.width / 2, 
            3 * self.height / 4])
        # Draw the words on-screen
        screen.blit(final, final_rect)
        screen.blit(score, score_rect)
        screen.blit(redo, redo_rect)
        screen.blit(quit, quit_rect)
    
    # Draws the screen displayed when the player wants help with controls
    def drawHelpScreen(self, screen):
        # Controls
        pass
    
    # Makes new stars; first call uses every row; afterward, uses only row 0
    def makeStars(self, row = 0):
        # Iterate through the width of the window and randomly place stars
        for col in range(0, self.width + 1):
            if random.randint(0, 2 ** 12 - 1) == 0:
                self.stars.add(Star(col, row))
    
    # Spawns a powerup at an enemy death point
    def spawnPowerup(self, enemyX, enemyY):
        # Spawns a powerup/powerdown from the options available
        powerupType = random.randint(0, 4)
        # 0: Shot up
        if powerupType == 0:
            # If 0, spawn a triple shot; otherwise, double shot
            if random.randint(0, 9) == 0:
                self.powerups.add(TripleShot(enemyX, enemyY))
            else:
                self.powerups.add(DoubleShot(enemyX, enemyY))
        # Otherwise: Speed change
        else:
            # If 0, spawn a speed down; otherwise, a speed up
            if random.randint(0, 2) == 0:
                self.powerups.add(SpeedDown(enemyX, enemyY))
            else:
                self.powerups.add(SpeedUp(enemyX, enemyY))
    
    # Changes player stats whn they hit a powerup
    def changePlayer(self, powerup):
        # If the powerup is a speed up, increase the player's velocity
        if isinstance(powerup, SpeedUp) and self.player.velocity != [20, 20]:
            self.player.velocity[0] += 1
            self.player.velocity[1] += 1
        # If the powerup is a speed down, decrease the player's velocity
        elif isinstance(powerup, SpeedDown) and self.player.velocity != [2, 2]:
            self.player.velocity[0] -= 1
            self.player.velocity[1] -= 1
        # If the powerup is 2x shot, disable single fire and enable double fire
        elif isinstance(powerup, DoubleShot):
            # Check if double shot is disabled to avoid overwriting 3x shot
            if not self.doubleShot:
                self.singleShot = False
            self.doubleShot = True
        # If the powerup is 2x shot, enable both single fire and double fire
        elif isinstance(powerup, TripleShot):
            self.singleShot = True
            self.doubleShot = True
    
# Suggested run (width, height) is (650, 800), but these can be changed
Game(650, 800).run()
