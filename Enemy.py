# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Module imports
import pygame
import copy
import math
# Class import
from GameObject import GameObject

# Superclass Enemy object
class Enemy(GameObject):
    
    # Initialize data
    def __init__(self, x, y, image, xradius, yradius, hp, velocity, attChance, 
        score):
        # Set x, y, image, and xy radii
        self.x, self.y = x, y
        self.image = image
        self.xradius, self.yradius = xradius, yradius
        # Call to superclass GameObject
        super(Enemy, self).__init__(x, y, image, xradius, yradius)
        # Set the enemy's hp and score value
        self.hp = hp
        self.score = score
        # Set velocity and attack chance
        self.velocity = velocity
        self.attChance = attChance
        # Allow initial movement of crawling in from a side
        self.offScreen = True
        # Initialize padding, destX, and destY
        self.padding = 48
        self.destX, self.destY = 0, 0
    
    # Update the Enemy objects
    def update(self, screenWidth, screenHeight):
        self.updateRect()
        # Kill the enemy if it goes offscreen (bottom)
        if self.y - self.yradius > screenHeight:
            self.kill()
        # Update the enemy while it hasn't gone offscreen (bottom)
        if self.y + self.yradius < screenHeight - self.padding:
            super(Enemy, self).update(screenWidth, screenHeight)
    
    # Stores the player's x position by updating the self.destX variable
    @staticmethod
    def storeDest(self, playerPos):
        self.destX, self.destY = playerPos

# Subclass Invader object
class Invader(Enemy):
    
    # Init to create image, made static for main game calling
    @staticmethod
    def init():
        # Image from: 
        # https://ih1.redbubble.net/image.373193027.3451/flat,800x800,070,f.u4.jpg
        Invader.invaderImage = pygame.transform.scale(
            pygame.image.load("images/flat,800x800,075,f.u4.jpg"), \
            (82, 60)).convert_alpha()
        # Copy the invader image
        newInvaderImage = Invader.invaderImage.copy()
        # Remove all white from image using threshold method
        pygame.transform.threshold(Invader.invaderImage, newInvaderImage, 
            (0, 255, 0), (10, 255, 10), (0, 0, 0, 0))
    
    # Initialize data
    def __init__(self, x, y):
        # Set xy radii, hp, and score yield
        xradius, yradius = 41, 30
        hp = 4
        score = 10
        # Set velocity and attack chance
        velocity = [4, 4]
        attChance = 60
        # Call to superclass Enemy
        super(Invader, self).__init__(x, y, Invader.invaderImage, xradius, 
            yradius, hp, velocity, attChance, score)
        # Set empty count of y moves and a boolean allowing movement on x axis
        self.yMoveCount = 0
        self.xMove = True
    
    # Update the Invader object
    def update(self, screenWidth, screenHeight):
        # Only update if all of the Invader is on screen
        if not self.offScreen:
            # Call to superclass Enemy
            super(Invader, self).update(screenWidth, screenHeight)
            # Update Invader movement
            self.updateMovement(screenWidth)
        # Otherwise, update the Invader and its x position
        else:
            self.updateRect()
            # Set Invader status to onscreen after it's crawled in
            if self.x - self.xradius >= 0:
                self.offScreen = False
            else:
                self.x += self.velocity[0]

    # Update the Invader's movement
    def updateMovement(self, screenWidth):
        # Checking for allowing x movement
        if self.xMove:
            # Disable x movement and invert x velocity if on a border
            if self.x - self.xradius == 0 or \
                self.x + self.xradius == screenWidth:
                self.xMove = False
                self.velocity[0] = -self.velocity[0]
            # Increase the x velocity otherwise
            else:
                self.x += self.velocity[0]
        # Increase y position if the Invader hasn't moved its y velocity squared
        elif self.yMoveCount != self.velocity[1] ** 2:
            self.yMoveCount += 1
            self.y += self.velocity[1]
        # When Invader moves y velocity squared, allow it to move on x axis
        elif self.yMoveCount == self.velocity[1] ** 2:
            self.xMove = True
            self.yMoveCount = 0
            self.x += self.velocity[0]
    
    
# Class for the dive bomber enemy
class DiveBomber(Enemy):
    
    # Init to create image, made static for main game calling
    @staticmethod
    def init():
        DiveBomber.dbImage = pygame.image.load("images/divebomber.png")
    
    # Initialize data
    def __init__(self, x, y):
        # Set xy radii, hp, and score yield
        xradius, yradius = 32, 32
        hp = 2
        score = 50
        # Set velocity and attack chance
        velocity = [4, 12]
        attChance = 0
        # Call to superclass Enemy
        super(DiveBomber, self).__init__(x, y, DiveBomber.dbImage, xradius, 
            yradius, hp, velocity, attChance, score)
    
    # Update the DiveBomber object
    def update(self, screenWidth, screenHeight):
        self.updateRect()
        if not self.offScreen:
            # Call to superclass Enemy
            super(DiveBomber, self).update(screenWidth, screenHeight)
        # Set DiveBomber status to onscreen after it's crawled in
        if self.y - self.yradius >= self.padding and self.y - self.yradius <= screenHeight:
            self.offScreen = False
        # Increase y velocity whether it's crawled in or not
        self.y += self.velocity[1]
        # Change x according to the destination x (where the player is)
        if self.x < self.destX:
            self.x += self.velocity[0]
        elif self.x > self.destX:
            self.x -= self.velocity[0]

# Class Drone object
class Drone(Enemy):
    
    # Init to create image, made static for main game calling
    @staticmethod
    def init():
        Drone.droneImage = pygame.image.load("images/drone.png")
    
    # Initialize data
    def __init__(self, x, y):
        # Set xy radii, hp, and score yield
        xradius, yradius = 16, 16
        hp = 2
        score = 50
        # Set unused velocity and attack chance
        velocity = [1, 1]
        attChance = 0
        # Call to superclass Enemy
        super(Drone, self).__init__(x, y, Drone.droneImage, xradius, 
            yradius, hp, velocity, attChance, score)
        # Set starting angle and constant radius
        self.angle = 90
        self.radius = 100
    
    # Update the Drone object
    def update(self, screenWidth, screenHeight):
        halfCircle, fullCircle = 180, 360
        # Reset the angle to be between 0 and 359, inclusive
        self.angle %= fullCircle
        # Circle equations from:
        # https://gamedev.stackexchange.com/questions/9607/moving-an-object-in-a-circular-path
        self.x = self.destX - self.radius * math.cos(
            math.radians(self.angle))
        # Mod the angle by 180 to make the drone move in a semicircle
        self.y = self.destY - self.radius * math.sin(
            math.radians(self.angle % halfCircle))
        # Call to superclass Enemy
        super(Drone, self).update(screenWidth, screenHeight)
        # Increase angle
        self.angle += 1