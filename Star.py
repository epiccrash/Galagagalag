# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Module imports
import pygame
import random
# Class import
from GameObject import GameObject

# Class Star object
class Star(GameObject):
    
    # Initialize data
    def __init__(self, x, y):
        # Set basic coordinates and xy radii (same radius)
        self.x, self.y = x, y
        radius = random.randint(1, 2)
        self.xradius, self.yradius = radius, radius
        # Create square to represent star
        starImage = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        # Randomize the blue component of the star
        blue = random.randint(200, 255)
        # Fill the star with a color between yellow and white
        starColor = (255, 255, blue)
        starImage.fill(starColor)
        # Call to superclass GameObject
        super(Star, self).__init__(x, y, starImage, self.xradius, self.yradius)
        # Initialize star velocity
        self.velocity = [0, 0.5]
    
    # Update the star object
    def update(self, screenWidth, screenHeight):
        # Get x velocity and y velocity and update the bounding rectangle
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.updateRect()
        # Kill the star sprite if it goes out of bounds
        if self.y - self.yradius > screenHeight:
            self.kill()