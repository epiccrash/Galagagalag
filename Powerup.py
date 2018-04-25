# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Module import
import pygame
# Class import
from GameObject import GameObject

# Superclass Powerup object
class Powerup(GameObject):
    
    # Initialize data
    def __init__(self, x, y, image, xradius, yradius):
        # Set x, y, image, and xy radii of powerup
        self.x, self.y = x, y
        powerupImage = image
        self.xradius, self.yradius = xradius, yradius
        # Call to superclass GameObject
        super(Powerup, self).__init__(x, y, powerupImage, xradius, yradius)
        # Initialize y velocity; used for falling
        self.yvelocity = 6
    
    # Update the powerup objects
    def update(self, screenWidth, screenHeight):
        # Increase position by velocity (x does not actually increase)
        if self.y - self.yradius > screenHeight:
            self.kill()
        # Increase y velocity and update the sprite
        self.y += self.yvelocity
        self.updateRect()

# Speed increase powerups
# Super- and subclass SpeedPower object; used to set xy radii
class SpeedPower(Powerup):
    
    # Initialize data
    def __init__(self, x, y, image):
        # Initialize xy radii and call superclass Powerup
        xradius, yradius = 30, 32
        super(SpeedPower, self).__init__(x, y, image, xradius, yradius)

# Subclass SpeedUp object
class SpeedUp(SpeedPower):
    
    # Initialize data
    def __init__(self, x, y):
        # Load image and call superclass SpeedPower
        image = pygame.image.load("images/speedup.png")
        super(SpeedUp, self).__init__(x, y, image)

# Subclass SpeedDown object
class SpeedDown(SpeedPower):
    
    # Initialize data
    def __init__(self, x, y):
        # Load image and call superclass SpeedPower
        image = pygame.image.load("images/speeddown.png")
        super(SpeedDown, self).__init__(x, y, image)

# Shot increase powerups
# Super- and subclass ShotIncrease object; used to set xy radii
class ShotIncrease(Powerup):
    
    # Initialize data
    def __init__(self, x, y, image):
        # Initialize xy radii and call superclass Powerup
        xradius, yradius = 29, 29
        super(ShotIncrease, self).__init__(x, y, image, xradius, yradius)

# Subclass DoubleShot object
class DoubleShot(ShotIncrease):
    
    # Initialize data
    def __init__(self, x, y):
        # Load image and call superclass ShotIncrease
        image = pygame.image.load("images/doubleshot.png")
        super(DoubleShot, self).__init__(x, y, image)

# Subclass TripleShot object
class TripleShot(ShotIncrease):
    
    # Initialize data
    def __init__(self, x, y):
        # Load image and call superclass ShotIncrease
        image = pygame.image.load("images/tripleshot.png")
        super(TripleShot, self).__init__(x, y, image)
