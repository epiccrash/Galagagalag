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
        self.invulnTime = 0
        # Store velocity in a list because powerups might increase it
        self.velocity = [8, 8]
        # Define bonus to speed when dashing
        self.dashSpeedBonus = 20
        # Define the speed up time and cooldown time between dashes
        self.speedUpTime = 8
        self.rechargeTime = 7
        # Set a cooldown counter and a boolean for if the dash is enabled
        self.cooldownCount = 0
        self.speedUpEnabled = True
    
    # Update the Player object
    def update(self, dt, keysDown, screenWidth, screenHeight):
        # Invulnerability frame increase; currently unused
        self.invulnTime += 1

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
            # Change player opacity for effect
            Player.playerImage.set_alpha(175)
        
        # If the player has dashed long enough, stop the dash
        if self.cooldownCount == self.speedUpTime:
            # Reset velocity to original values
            self.velocity[0] -= self.dashSpeedBonus
            self.velocity[1] -= self.dashSpeedBonus
            # Reset the cooldown count to 1 and disable the dash
            self.cooldownCount = 1
            self.speedUpEnabled = False
            # Rest the player's opacity
            Player.playerImage.set_alpha(255)
        
        # Check if the dash is not enabled, but the recharge time is hit
        if not self.speedUpEnabled and self.cooldownCount == self.rechargeTime:
            # If so, reset the cooldown count to 0 and enable the dash
            self.cooldownCount = 0
            self.speedUpEnabled = True
        # Otherwise, if the cooldown count can increase, increase it
        elif self.cooldownCount > 0 and self.cooldownCount < self.speedUpTime:
            self.cooldownCount += 1
          
        # Call to superclass GameObject
        super(Player, self).update(screenWidth, screenHeight)
    
    # Check if player is invulnerabile (currently unused, taken from Lukas)
    def isInvulnerable(self):
        return self.maxInvulnTime > self.invulnTime