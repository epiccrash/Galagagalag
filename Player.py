# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Module import
import pygame
# Class import
from GameObject import GameObject

# Class Player object
class Player(GameObject):
    
    # Init to create image, made static for main game calling
    @staticmethod
    def init():
        # Image from http://chickeninvaders.wikia.com/wiki/File:Galaga_ship.png
        # Shrink image to 64x64
        Player.playerImage = pygame.transform.scale(
            pygame.image.load("images/Galaga_ship.png"), (64, 64))
    
    # Initialize data
    def __init__(self, x, y):
        # Set xy radii equal as half of image width or height
        self.radius = 32
        # Call to superclass GameObject
        super(Player, self).__init__(x, y, Player.playerImage, self.radius, 
            self.radius)
        # Create invulnerability time counter; currently unused
        self.invulnTime = 1000
        self.maxInvulnTime = 1000
        # Store velocity in a list because powerups might increase it
        self.velocity = [8, 8]
        # Define bonus to speed when dashing
        self.dashSpeedBonus = 20
        # Define the speed up time and cooldown time between dashes
        self.speedUpTime = 10
        self.rechargeTime = 8
        # Set a cooldown counter and a boolean for if the dash is enabled
        self.cooldownCount = 0
        self.speedUpEnabled = True
        # Set a boolean to track if player is dashing
        self.dashing = False
    
    # Update the Player object
    def update(self, keysDown, screenWidth, screenHeight):
        # Invulnerability frame increase
        self.invulnTime += 5

        # Update player based on keypresses
        self.updateKeys(keysDown)

        # Change player opacity for effect
        if self.dashing:
            Player.playerImage.set_alpha(175)
        
        # Update player and dash state
        self.updateDash()
          
        # Call to superclass GameObject
        super(Player, self).update(screenWidth, screenHeight)
    
    # Updates player movement based on keypresses
    def updateKeys(self, keysDown):
        # Check for key holds to change x, y position
        if (keysDown(pygame.K_LEFT) or keysDown(pygame.K_a)):
            self.x -= self.velocity[0]
        elif (keysDown(pygame.K_RIGHT) or keysDown(pygame.K_d)):
            self.x += self.velocity[0]
        if (keysDown(pygame.K_UP) or keysDown(pygame.K_w)):
            self.y -= self.velocity[1]
        elif (keysDown(pygame.K_DOWN) or keysDown(pygame.K_s)):
            self.y += self.velocity[1]

        # If Left Shift is pressed and the player can speed up, make ship dash
        if (keysDown(pygame.K_LSHIFT) and self.speedUpEnabled 
            and self.cooldownCount == 0):
            # Increase x and y velocity
            self.velocity[0] += self.dashSpeedBonus
            self.velocity[1] += self.dashSpeedBonus
            # Increase the cooldown count (not actually cooling down yet)
            self.cooldownCount += 1
            self.dashing = True
    
    # Update the state of the player's dash and whether player is dashing
    def updateDash(self):
        # If the player has dashed long enough, stop the dash
        if self.cooldownCount == self.speedUpTime:
            # Reset velocity to original values
            self.velocity[0] -= self.dashSpeedBonus
            self.velocity[1] -= self.dashSpeedBonus
            # Reset the cooldown count to 1 and disable the dash
            self.cooldownCount = 1
            self.speedUpEnabled = False
            # Say player is not dashing
            self.dashing = False
            # Rest the player's opacity
            if not self.isInvulnerable():
                Player.playerImage.set_alpha(255)
        # Check if the dash is not enabled, but the recharge time is hit
        if not self.speedUpEnabled and self.cooldownCount == self.rechargeTime:
            # If so, reset the cooldown count to 0 and enable the dash
            self.cooldownCount = 0
            self.speedUpEnabled = True
        # Otherwise, if the cooldown count can increase, increase it
        elif self.cooldownCount > 0 and self.cooldownCount < self.speedUpTime:
            self.cooldownCount += 1
    
    # Check if player is invulnerable
    def isInvulnerable(self):
        # Change the sprite's opacity (causing a flashing motion) if so
        if self.maxInvulnTime > self.invulnTime:
            if self.invulnTime % 10 >= 0 and self.invulnTime % 10 <= 4:
                Player.playerImage.set_alpha(0)
            else:
                Player.playerImage.set_alpha(145)
            # The player is invulnerable
            return True
        # Otherwise, reset the opacity; the player is not invulnerable
        Player.playerImage.set_alpha(255)
        return False
    