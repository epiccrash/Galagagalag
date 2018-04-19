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
from Player import Player
from Attack import PlayerLaser, EnemyLaser
from Enemy import Invader

# Main Game object; used for running the game
class Game(PygameGame):
    
    # Initializing data
    def init(self):
        # Background color of window
        self.bgColor = (0, 0, 0)
        # Load custom font
        # Downloaded from https://fonts.google.com/specimen/Press+Start+2P?selection.family=Press+Start+2P
        # Created by CodeMan38; license included in folder
        self.font = pygame.font.Font(
            "Press_Start_2P/PressStart2P-Regular.ttf", 24)
        # Life counter; currently unused
        self.lives = 3
        # Used for spawning and top/bottom padding (currently enemies still use it)
        self.ypadding = 48
        # Set the player's score
        self.score = 0
        
        # Create the Player object, place in a single group
        Player.init()
        self.player = Player(self.width / 2, self.height - self.ypadding)
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
        
        # Create Invader object, place on screen, add to enemy group
        # For now, something of a placeholder until actual enemy looping
        Invader.init()
        invader = Invader(self.width / 2, self.ypadding)
        self.enemyGroup = pygame.sprite.Group()
        self.enemyGroup.add(invader)
        
        # Create enemy laser group
        self.enemyLasers = pygame.sprite.Group()
        
    # Changing game or game data
    def timerFired(self, dt):
        # Update attacks
        self.updatePlayerAttacks()
        self.updateEnemyAttacks()

        # Check for object collisions
        self.checkCollisions()
        
        # Update the player object, check for keypresses
        self.playerGroup.update(dt, self.isKeyPressed, self.width, self.height)
        
        # Enable/Disable autofire depending on caps lock state
        if pygame.key.get_pressed()[pygame.K_CAPSLOCK]:
            self.autofireEnabled = True
        else:
            self.autofireEnabled = False
        
        # Update enemies in enemy group
        self.enemyGroup.update(self.width, self.height)
        
    # Draw everything onto screen
    def redrawAll(self, screen):
        self.playerLasers.draw(screen)
        self.playerGroup.draw(screen)
        self.enemyLasers.draw(screen)
        self.enemyGroup.draw(screen)

        self.drawScore(screen)

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
                    xSpawn - (self.player.xradius - 2), ySpawn + self.player.yradius))
                self.playerLasers.add(PlayerLaser(
                    xSpawn + (self.player.xradius - 2), ySpawn + self.player.yradius))
            # Disable laser firing for cooldown
            self.laserEnabled = False
            
        # Check if cooldown time count equals the recharge time
        if not self.laserEnabled:
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
            if random.randint(0, enemy.attChance) == enemy.attChance:
                self.enemyLasers.add(EnemyLaser(enemy.x, 
                    enemy.y + enemy.yradius / 2))
    
    # Check for collisions between objects
    def checkCollisions(self):
        # Collision detection: Remove a player laser if it hits an enemy
        for enemy in pygame.sprite.groupcollide(
            self.enemyGroup, self.playerLasers, False, True,
            pygame.sprite.collide_rect):
            # Reduce enemy HP; enemy is removed if HP drops to zero
            enemy.hp -= 1
            if enemy.hp == 0:
                # Increase score and kill sprite if enemy is killed
                self.score += enemy.score
                enemy.kill()
        
        # Collision detection: Remove an enemy laser if if hits the player
        if (not self.player.isInvulnerable() and not 
            self.player.dashing and 
            pygame.sprite.groupcollide(self.playerGroup, 
            self.enemyLasers, False, True, 
            pygame.sprite.collide_rect)):
                # Reduce player lives
                self.lives -= 1
                self.player.invulnTime = 0
        
        # Collision detection: Hurt player if they hit an enemy
        if (not self.player.isInvulnerable() and not 
            self.player.dashing and
            pygame.sprite.groupcollide(
            self.playerGroup, self.enemyGroup, False, False,
            pygame.sprite.collide_rect)):
                # Reduce player lives
                self.lives -= 1
                self.player.invulnTime = 0
        
        # Game ends if player has no lives left; currently unused
        if self.lives == 0:
            pass
    
    # Draws the score
    def drawScore(self, screen):
        # Draw the score
        score = self.font.render('SCORE: %d' % self.score, 
            True, (255, 255, 255))
        # Create a black score box
        scoreBox = pygame.Surface((self.width, self.ypadding), pygame.SRCALPHA)
        scoreBox.fill((0, 0, 0))
        # Place the box and score on the screen
        screen.blit(scoreBox, [0, 0])
        screen.blit(score, [12, 12])
    
# Suggested run (width, height) is (650, 800), but these can be changed
Game(650, 800).run()
