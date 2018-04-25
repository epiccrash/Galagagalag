# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Module import
import pygame
# Class import
from GameObject import GameObject

# Superclass Laser object
class Laser(GameObject):
    
    # Initialize data
    def __init__(self, x, y, xradius, yradius, velocity, laserColor):
        # Set basic coordinates and xy radii
        self.x, self.y = x, y
        self.xradius, self.yradius = xradius, yradius
        # Create rectangle to represent laser
        laserImage = pygame.Surface((2 * xradius, 2 * yradius), pygame.SRCALPHA)
        laserImage.fill(laserColor)
        # Call to superclass GameObject
        super(Laser, self).__init__(x, y, laserImage, xradius, yradius)
        # Initialize laser velocity from subclass
        self.velocity = velocity
    
    # Update the laser object; override superclass update method
    def update(self, screenWidth, screenHeight):
        # Get x velocity and y velocity and update the bounding rectangle
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.updateRect()
        # Set vertical padding
        ypadding = 48
        # Kill the laser sprite if it goes out of bounds
        if (self.y + self.yradius < ypadding or 
            self.y - self.yradius > screenHeight - ypadding):
            self.kill()

# Subclass Player Laser object
class PlayerLaser(Laser):
    
    # Initialize data
    def __init__(self, x, y):
        # Get specified x and y, manually set xy radii and velocity
        x, y = x, y
        xradius, yradius = 2, 30
        velocity = 0, -25
        # Make the laser color white
        color = (255, 255, 255)
        # Call to superclass GameObject
        super(PlayerLaser, self).__init__(x, y, xradius, yradius, 
            velocity, color)

# Subclass EnemyLaser object
class EnemyLaser(Laser):
    
    # Initialize data
    def __init__(self, x, y):
        # Get specified x and y, manually set xy radii and velocity
        x, y = x, y
        xradius, yradius = 4, 30
        velocity = 0, 25
        # Make the laser color purple
        color = (255, 0, 255)
        # Call to superclass GameObject
        super(EnemyLaser, self).__init__(x, y, xradius, yradius, 
            velocity, color)