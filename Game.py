# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Main class: updates the different sections of the game and performs most work.

# This code is used to import Austin's module manager; much thanks to him!
# https://raw.githubusercontent.com/CMU15-112/module-manager/master/module_manager.py
import module_manager
module_manager.review()

# Module imports
import pygame
import random
import copy

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
        
        # Enables a joystick to be used, as long as one is connected
        # NOTE: Assumes an Xbox controller is being used. This may not work on 
        # any machine which lacks Xbox drivers, and may only work with the one 
        # specific controller.
        pygame.joystick.init()
        self.jCount = pygame.joystick.get_count() > 0
        if self.jCount:
            self.xbController = pygame.joystick.Joystick(0)
            self.xbController.init()
        
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

        # Create the ship image to edit
        self.shipImage = pygame.image.load("images/galaga_ship.png").convert()
        self.ship_rect = self.shipImage.get_rect(center = (self.width / 2, 
            self.height / 2))
        # Create the final product of drawing (image actually edited)
        self.finalShip = self.shipImage.copy()
        
        # Set default RGB values
        self.redVal, self.blueVal, self.greenVal = 128, 128, 128
        
        # Red value display text
        self.red = self.font.render("RED:%d" % self.redVal, True, 
            (255, 0, 0))
        self.red_rect = self.red.get_rect(topleft = [10, 14])
        # Red increase display
        self.redInc = self.titleFont.render("+", True, (255, 0, 0)) 
        self.redInc_rect = self.redInc.get_rect(topright = 
            (self.red_rect.width / 2, self.ypadding))
        # Red decrease display
        self.redDec = self.titleFont.render("-", True, (255, 0, 0))
        self.redDec_rect = self.redDec.get_rect(topleft = 
            (self.red_rect.width / 2, self.ypadding))
        
        # Green value display text
        self.green = self.font.render("GREEN:%d" % self.greenVal, True, 
            (0, 255, 0))
        self.green_rect = self.green.get_rect(midtop = [self.width / 2, 14])
        # Green increase display
        self.greenInc = self.titleFont.render("+", True, (0, 255, 0)) 
        self.greenInc_rect = self.greenInc.get_rect(topright = 
            (self.width / 2, self.ypadding))
        # Green decrease display
        self.greenDec = self.titleFont.render("-", True, (0, 255, 0))
        self.greenDec_rect = self.greenDec.get_rect(topleft = 
            (self.width / 2, self.ypadding))
        
        # Blue value display text
        self.blue = self.font.render("BLUE:%d" % self.blueVal, True, 
            (0, 0, 255))
        self.blue_rect = self.blue.get_rect(topright = [self.width - 10, 14])
        # Blue increase display
        self.blueInc = self.titleFont.render("+", True, (0, 0, 255)) 
        self.blueInc_rect = self.blueInc.get_rect(topright = 
            (self.width - self.blue_rect.width / 2, self.ypadding))
        # Blue decrease display
        self.blueDec = self.titleFont.render("-", True, (0, 0, 255))
        self.blueDec_rect = self.blueDec.get_rect(topleft = 
            (self.width - self.blue_rect.width / 2, self.ypadding))
        
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
        # Draw the how to play screen
        if self.gameState == self.info:
            self.drawHelpScreen(screen)
        # Draw the editor if it corresponds to the game state
        elif self.gameState == self.editor:
            self.drawEditor(screen)
        # Draw the title screen if it corresponds to the game state
        elif self.gameState == self.titleScreen:
            self.drawTitleScreen(screen)
        # Check to see if the game is being played
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
        # Update the player object ith joystick info if there is one
        if self.jCount:        
            self.playerGroup.update(self.isKeyPressed, self.width, self.height, 
                self.xbController.get_axis(0), self.xbController.get_axis(1),
                self.xbController.get_button(7))
        # Update the player object using only keypresses
        else:
            self.playerGroup.update(self.isKeyPressed, self.width, self.height)
        
        # Helper functions to check on autofire and enemies
        self.autoEnableCheck()
        self.checkEnemies()
        
        # Update the powerups
        self.powerups.update(self.width, self.height)
    
    # Checks to see if any inputs allow autofire enabled
    def autoEnableCheck(self):
        # Enable/Disable autofire depending on caps lock state
        if pygame.key.get_pressed()[pygame.K_CAPSLOCK]:
            self.autofireEnabled = True
        elif self.jCount:
            # Enable autofire if an Xbox controller Y button is pressed
            if self.xbController.get_button(0):
                self.autofireEnabled = True
            # Disable autofire if an Xbox controller X button is pressed
            elif self.xbController.get_button(3):
                self.autofireEnabled = False
        else:
            self.autofireEnabled = False
    
    # Checks status of enemies
    def checkEnemies(self):
        # Give the player's coordinates to enemies
        for enemy in self.enemyGroup:
            enemy.storeDest(enemy, (self.player.x, self.player.y))
        # Update enemies in enemy group
        self.enemyGroup.update(self.width, self.height)
        # Make more enemies if there aren't any remaining and increase wave
        if len(self.enemyGroup) == 0:
            self.wave += 1
            self.generateEnemies()
    
    # Updates the game state according to keypresses
    def updateKeys(self):
        # Check for movement out of help screen
        if self.gameState == self.info:
            self.helpKeyCheck()
        # Change values in the editor
        elif self.gameState == self.editor:
            self.editorKeyCheck()
        # Create the title screen and start playing if Enter is pressed
        elif self.gameState == self.titleScreen:
            self.titleKeyCheck()
        # Check to see if the game is at the "over" stage
        elif self.gameState == self.gameOver:
            self.gameOverKeyCheck()
        
    # Checks keys pressed in the how to play screen
    def helpKeyCheck(self):
        # If B is pressed, go back to the title screen
        if (self.isKeyPressed(pygame.K_b) or 
            (self.jCount and self.xbController.get_button(1))):
            self.gameState = self.titleScreen
    
    # Checks keys pressed in the editor
    def editorKeyCheck(self):
        # Quit the editor if q is pressed
        if self.isKeyPressed(pygame.K_q):
            # Reinitialize to update player sprite
            self.init()
        # Save the image if s is pressed
        elif self.isKeyPressed(pygame.K_s):
            pygame.image.save(self.finalShip, "images/Galaga_ship.png")
        # Reset the ship sprite if r is pressed
        elif self.isKeyPressed(pygame.K_r):
            self.finalShip = self.shipImage.copy()
        # General edit ship call
        self.editShip()
    
    # Checks keys pressed in the game over screen
    def gameOverKeyCheck(self):
        # If Enter or Start is pressed, restart the game
        if (self.isKeyPressed(pygame.K_RETURN) or 
            (self.jCount and self.xbController.get_button(9))):
            self.init(self.gamePlaying, self.stars)
        # If the q key or Select is pressed, quit to the title screen
        elif (self.isKeyPressed(pygame.K_q) or 
            (self.jCount and self.xbController.get_button(8))):
            self.init(self.titleScreen, self.stars)

    # Checks keys pressed in the title screen
    def titleKeyCheck(self):
        # Begin the game if Enter or Start is pressed
        if (self.isKeyPressed(pygame.K_RETURN) or 
            (self.jCount and self.xbController.get_button(9))):
            self.gameState = self.gamePlaying
        # If Tab is pressed, set the game state to be the ship editor
        elif self.isKeyPressed(pygame.K_TAB):
            self.gameState = self.editor
        # If H or Y is pressed, set the game state to be the help popup
        elif (self.isKeyPressed(pygame.K_h) or 
            (self.jCount and self.xbController.get_button(0))):
            self.gameState = self.info
    
    # Updates the player's attacks
    def updatePlayerAttacks(self):
        # Update the player lasers
        self.playerLasers.update(self.width, self.height)
        # Fire lasers if spacebar is pressed or if autofire is enabled
        if (((self.isKeyPressed(pygame.K_SPACE) or 
            (self.jCount and 
            self.xbController.get_button(2))) or self.autofireEnabled) 
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
        if self.wave >= 8:
            upperBound = 7
        else:
            upperBound = self.wave
        # Randomly decide the amount of enemies that can spawn from the bounds
        enemyCount = random.randint(lowerBound, upperBound)
        # If the wave is at least 7, 1/4th chance of spawning a drone
        if self.wave >= 7 and random.randint(0, 3) == 0:
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
        play = self.font.render("[Enter/Start] Play", True, (255, 0, 0))
        play_rect = play.get_rect(center = [self.width / 2, 
            2 * self.height / 3 - 1.5 * self.fontSize])
        # Draw Help option (currently does nothing)
        info = self.font.render("[H/Y] How to Play", True, (0, 255, 0))
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
        redo = self.font.render("[R/Start] Replay", True, (255, 0, 0))
        redo_rect = redo.get_rect(center = [self.width / 2, 
            2 * self.height / 3])
        # Create information on quitting to the title screen
        quit = self.font.render("[Q/Select] Quit to title", True, (0, 0, 255))
        quit_rect = quit.get_rect(center = [self.width / 2, 
            3 * self.height / 4])
        # Draw the words on-screen
        screen.blit(final, final_rect)
        screen.blit(score, score_rect)
        screen.blit(redo, redo_rect)
        screen.blit(quit, quit_rect)
    
    # Draws the screen displayed when the player wants help with controls
    def drawHelpScreen(self, screen):
        # Movement text
        move = self.font.render("Move Ship:", True, (255, 0, 0))
        move_rect = move.get_rect(center = [self.width / 2, self.ypadding])
        screen.blit(move, move_rect)
        
        # Move key text
        moveKeys = self.font.render("WASD/Arrow Keys/Left Stick", True, 
            (255, 255, 255))
        moveKeys_rect = moveKeys.get_rect(center = [self.width / 2, 
            2 * self.ypadding])
        screen.blit(moveKeys, moveKeys_rect)
        
        # Dash text
        dash = self.font.render("Short Dash:", True, 
            (0, 255, 0))
        dash_rect = dash.get_rect(center = [self.width / 2, 4 * self.ypadding])
        screen.blit(dash, dash_rect)
        
        # Dash key text
        dashKeys = self.font.render("Shift/RT + Direction", True, 
            (255, 255, 255))
        dashKeys_rect = dashKeys.get_rect(center = [self.width / 2, 
            5 * self.ypadding])
        screen.blit(dashKeys, dashKeys_rect)
        
        # Firing text
        fire = self.font.render("Firing:", True, (0, 0, 255))
        fire_rect = fire.get_rect(center = [self.width / 2, 7 * self.ypadding])
        screen.blit(fire, fire_rect)
        
        # Fire text
        fireKeys = self.font.render("Spacebar/A", True, (255, 255, 255))
        fireKeys_rect = fireKeys.get_rect(center = [self.width / 2, 
            8 * self.ypadding])
        screen.blit(fireKeys, fireKeys_rect)
        
        # Enable autofire text
        auto = self.smallFont.render("Enable Autofire: Caps Lock/Y", True, 
            (255, 255, 0))
        auto_rect = auto.get_rect(center = [self.width / 2, 
            8.5 * self.ypadding])
        screen.blit(auto, auto_rect)
        
        # Disable Autofire text
        disauto = self.smallFont.render("Disable Autofire: Caps Lock/X", True, 
            (255, 255, 0))
        disauto_rect = disauto.get_rect(center = [self.width / 2, 
            9 * self.ypadding])
        screen.blit(disauto, disauto_rect)
        
        # Back option
        back = self.font.render("Back to title: [B]", True, (0, 255, 255))
        back_rect = back.get_rect(midbottom = [self.width / 2, 
            self.height - self.ypadding])
        screen.blit(back, back_rect)
        
        # Goal text
        goal = self.font.render("Last as long as possible", True, (255, 0, 255))
        goal_rect = goal.get_rect(center = [self.width / 2, 12 * self.ypadding])
        screen.blit(goal, goal_rect)
        
        # More goal text
        goalBottom = self.font.render("and take out the enemies!", True, 
            (255, 0, 255))
        goalBottom_rect = goalBottom.get_rect(center = [self.width / 2, 
            12.5 * self.ypadding])
        screen.blit(goalBottom, goalBottom_rect)
    
    # Makes new stars; first call uses every row; afterward, uses only row 0
    def makeStars(self, row = 0):
        # Iterate through the width of the window and randomly place stars
        starChance = 2 ** 13
        for col in range(0, self.width + 1):
            if random.randint(0, starChance) == 0:
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
    
    # Changes player stats when they hit a powerup
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
    
    # Performs bulk work of ship editor
    def editShip(self):
        # Check if left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            self.rectEval()
            # Get the mouse position
            mouseX, mouseY = pygame.mouse.get_pos()
            # Check if the mouse is within bounds
            if (mouseX >= 261 and mouseX <= 388 or
                mouseY >= 336 and mouseY <= 463):
                    dX, dY = mouseX - 261, mouseY - 336
                    # In case the coordinates are still out of bounds, readjust
                    if dX > 0 and dX < 127 and dY > 0 and dY < 127:
                        # Create the pixels
                        self.createBlock(dX, dY)
    
    # Checks for point collisions within increase/decrease rectangles
    def rectEval(self):
        # Check for the red + being pressed
        if self.redInc_rect.collidepoint(pygame.mouse.get_pos()):
            if self.redVal < 255:
                self.redVal += 1
        # Check for the red - being pressed
        elif self.redDec_rect.collidepoint(pygame.mouse.get_pos()):
            if self.redVal > 0:
                self.redVal -=1
        # Check for the green + being pressed
        elif self.greenInc_rect.collidepoint(pygame.mouse.get_pos()):
            if self.greenVal < 255:
                self.greenVal += 1
        # Check for the green - being pressed
        elif self.greenDec_rect.collidepoint(pygame.mouse.get_pos()):
            if self.greenVal > 0:
                self.greenVal -=1
        # Check for the blue + being pressed
        elif self.blueInc_rect.collidepoint(pygame.mouse.get_pos()):
            if self.blueVal < 255:
                self.blueVal += 1
        # Check for the blue - being pressed
        elif self.blueDec_rect.collidepoint(pygame.mouse.get_pos()):
            if self.blueVal > 0:
                self.blueVal -=1
    
    # Creates an 8-pixel block where the mouse was pressed
    def createBlock(self, dX, dY): 
        for row in range(-3, 5):
            for col in range(-3, 5):
                # Check if the new x and y are within rectangle bounds
                if dX + col >= 0 and dX + col <= 127:
                    if dY + row >= 0 and dY + row <= 127:
                        # Change the color
                        self.finalShip.set_at((dX + col, dY + row), 
                            pygame.Color(self.redVal, self.greenVal, 
                            self.blueVal, 255))
    
    # Draw the editor
    def drawEditor(self, screen):
        # Draw the drawing space and the ship itself
        drawBorder = pygame.Surface((self.ship_rect.width + 8, 
            self.ship_rect.height + 8))
        drawBorder.fill((70, 70, 70))
        drawBorder_rect = drawBorder.get_rect(center = [self.width / 2, 
            self.height / 2])
        drawSpace = pygame.Surface((self.ship_rect.width, 
            self.ship_rect.height), pygame.SRCALPHA)
        drawSpace.fill((100, 100, 100))
        screen.blit(drawBorder, drawBorder_rect)
        screen.blit(drawSpace, self.ship_rect)
        screen.blit(self.finalShip, self.ship_rect)

        # Helper functions for drawing everything on the screen
        self.drawColorBar(screen)
        self.drawText(screen)
        self.drawColorView(screen)
        self.drawOptions(screen)
        self.drawColorUI(screen)
    
    # Draws the color text up at the top of the screen
    def drawColorBar(self, screen):
        # Box to hold the colors
        colorBox = pygame.Surface((self.width, self.ypadding),
            pygame.SRCALPHA)
        colorBox.fill((255, 255, 255))        
        screen.blit(colorBox, [0, 0])
        
        # Draw the RGB font on the screen (updates what was in init)
        # Draw red font
        self.red = self.font.render("RED:%d" % self.redVal, True, 
            (255, 0, 0))
        self.red_rect = self.red.get_rect(topleft = [10, 14])
        
        # Draw green font
        self.green = self.font.render("GREEN:%d" % self.greenVal, True, 
            (0, 255, 0))
        self.green_rect = self.green.get_rect(midtop = [self.width / 2, 14])
        
        # Draw blue font
        self.blue = self.font.render("BLUE:%d" % self.blueVal, True, 
            (0, 0, 255))
        self.blue_rect = self.blue.get_rect(topright = [self.width - 10, 14])
    
    # Draws all text in editor
    def drawText(self, screen):
        # Draw editor text
        editTextTop = self.font.render("Click the + and - above to", True, 
            (255, 255, 255))
        editRectTop = editTextTop.get_rect(center = [self.width / 2, 
            self.height / 6])
        screen.blit(editTextTop, editRectTop)
        editTextBottom = self.font.render("change the RGB color values", True,
            (255, 255, 255))
        editRectBottom = editTextBottom.get_rect(center = [self.width / 2, 
            self.height / 6 + 2 * self.ypadding / 3])
        screen.blit(editTextBottom, editRectBottom)
        
        # Draw text above ship
        shipText = self.font.render("DRAW SHIP HERE", True, (255, 255, 255))
        shipRect = shipText.get_rect(center = [self.width / 2, 
            self.height / 2 - 2 * self.ypadding])
        screen.blit(shipText, shipRect)
        
        # Draw the color preview text
        colorPrev = self.font.render("COLOR", True, (255, 255, 255))
        colorPrev_rect = colorPrev.get_rect(center = 
            [self.width / 2, self.height / 2 + 3.5 * self.ypadding])
        screen.blit(colorPrev, colorPrev_rect)
    
    # Draws the boxes showing the color
    def drawColorView(self, screen):
        # Draw the shape forming the border of the color wrapper
        colorShell = pygame.Surface((96, 96), pygame.SRCALPHA)
        colorShell.fill((255, 255, 255))
        colorS_rect = colorShell.get_rect(center = 
            [self.width / 2, self.height / 2 + 5 * self.ypadding])
        screen.blit(colorShell, colorS_rect)
        
        # Draw the border around the color
        colorWrapper = pygame.Surface((80, 80), pygame.SRCALPHA)
        colorWrapper.fill((0, 0, 0))
        colorW_rect = colorWrapper.get_rect(center = 
            [self.width / 2, self.height / 2 + 5 * self.ypadding])
        screen.blit(colorWrapper, colorW_rect)
        
        # Draw the color
        colorShow = pygame.Surface((64, 64), pygame.SRCALPHA)
        colorShow.fill((self.redVal, self.greenVal, self.blueVal))
        colorShow_rect = colorShow.get_rect(center = 
            [self.width / 2, self.height / 2 + 5 * self.ypadding])
        screen.blit(colorShow, colorShow_rect)
    
    # Draws the options at the bottom of the screen
    def drawOptions(self, screen):
        # Draw the box with the different options shown on it
        optionBox = pygame.Surface((self.width, self.ypadding),
            pygame.SRCALPHA)
        optionBox.fill((125, 125, 125))        
        screen.blit(optionBox, [0, self.height - self.ypadding])
        
        # Draw the quit option
        quit = self.font.render("[Q] Quit", True, (0, 255, 255))
        quit_rect = quit.get_rect(bottomleft = [10, self.height - 10])
        screen.blit(quit, quit_rect)
        
        # Draw the reset option
        reset = self.font.render("[R] Reset", True, (0, 0, 0))
        reset_rect = reset.get_rect(midbottom = 
            [self.width / 2, self.height - 10])
        screen.blit(reset, reset_rect)
        
        # Draw the save option
        save = self.font.render("[S] Save", True, (255, 255, 0))
        save_rect = save.get_rect(bottomright = [self.width - 10, 
            self.height - 10])
        screen.blit(save, save_rect)
    
    # Draws the color values and the increase/decrease icons
    def drawColorUI(self, screen):
        # Draw the red text and the red increases/decreases
        screen.blit(self.red, self.red_rect)
        screen.blit(self.redInc, self.redInc_rect)
        screen.blit(self.redDec, self.redDec_rect)
        
        # Draw the green text and the green increases/decreases
        screen.blit(self.green, self.green_rect)
        screen.blit(self.greenInc, self.greenInc_rect)
        screen.blit(self.greenDec, self.greenDec_rect)
        
        # Draw the blue text and the blue increases/decreases
        screen.blit(self.blue, self.blue_rect)
        screen.blit(self.blueInc, self.blueInc_rect)
        screen.blit(self.blueDec, self.blueDec_rect)
    
# Suggested run (width, height) is (650, 800)
Game(650, 800).run()
