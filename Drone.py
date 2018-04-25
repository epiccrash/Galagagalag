# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# Module import
import pygame
# Class import
from GameObject import GameObject

# Class Drone object
class Drone(GameObject):
    
    # Initialize data
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.image.load("images/drone.png")
        radius = 16
        xradius, yradius = radius, radius
        super(Drone, self).__init__(x, y, image, xradius, yradius)
        self.velocity = [3, 3]
    
    def update(self, screenWidth, screenHeight):
        
        