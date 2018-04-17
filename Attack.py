# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

import pygame
from GameObject import GameObject

class Laser(GameObject):
    
    def __init__(self, x, y, xradius, yradius, velocity, laserColor):
        self.x, self.y = x, y
        self.xradius, self.yradius = xradius, yradius
        laserImage = pygame.Surface((2 * xradius, 2 * yradius), pygame.SRCALPHA)
        laserImage.fill(laserColor)
        super(Laser, self).__init__(x, y, laserImage, xradius, yradius)
        self.velocity = velocity
    
    def update(self, screenWidth, screenHeight):
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        if self.y + self.yradius < 0 or self.y - self.yradius > screenHeight:
            self.kill()

class PlayerLaser(Laser):
    
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.xradius, self.yradius = 2, 30
        self.velocity = 0, -25
        self.color = (255, 255, 255)
        super(PlayerLaser, self).__init__(self.x, self.y,
            self.xradius, self.yradius, self.velocity, self.color)

class EnemyLaser(Laser):
    
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.xradius, self.yradius = 4, 30
        self.velocity = 0, 20
        self.color = (255, 0, 255)
        super(EnemyLaser, self).__init__(self.x, self.y,
            self.xradius, self.yradius, self.velocity, self.color)