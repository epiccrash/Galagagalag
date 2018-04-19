# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Module import
import pygame
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
    
    # Update the Enemy objects
    def update(self, screenWidth, screenHeight):
        # Call to superclass GameObject
        super(Enemy, self).update(screenWidth, screenHeight)

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
        # Set xy radii
        xradius, yradius = 41, 30
        # Invader HP and score value
        hp = 5
        score = 10
        # Set velocity and attack chance
        velocity = [4, 4]
        attChance = 30
        # Call to superclass Enemy
        super(Invader, self).__init__(x, y, Invader.invaderImage, xradius, 
            yradius, hp, velocity, attChance, score)
        # Set empty count of y moves and a boolean allowing movement on x axis
        self.yMoveCount = 0
        self.xMove = True
    
    # Update the Invader object
    def update(self, screenWidth, screenHeight):

        # Call to superclass Enemy
        super(Invader, self).update(screenWidth, screenHeight)
        
        # Checking for aloowing x movement
        if self.xMove:
            # Disable x movement and invert x velocity if on a border
            if self.x - self.xradius == 0 or \
                self.x + self.xradius == screenWidth:
                self.xMove = False
                self.velocity[0] = -self.velocity[0]
            # Increase the x velocity otherwise
            else:
                self.x += self.velocity[0]
        # Increase y position if the enemy hasn't moved its y velocity squared
        elif self.yMoveCount != self.velocity[1] ** 2:
            self.yMoveCount += 1
            self.y += self.velocity[1]
        # When enemy moves y velocity squared, allow it to move on x axis again
        elif self.yMoveCount == self.velocity[1] ** 2:
            self.xMove = True
            self.yMoveCount = 0
            self.x += self.velocity[0]
                