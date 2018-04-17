# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project
# NOTE: This file was made by Lukas Peraza. 
# It has been modified from the original work, but the main structure is his.

'''
GameObject.py

implements the base GameObject class, which defines the wraparound motion
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame


class GameObject(pygame.sprite.Sprite):
    # xradius and yradius added to better make rectangles
    def __init__(self, x, y, image, xradius, yradius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.xradius, self.yradius \
            = x, y, image, xradius, yradius
        w, h = image.get_size()
        self.updateRect()
        self.velocity = (0, 0)

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.updateRect()
        if self.rect.right > screenWidth:
            self.x = screenWidth - self.width / 2
        elif self.rect.left < 0:
            self.x = self.width / 2
        if self.rect.bottom > screenHeight:
            self.y = screenHeight - self.height / 2
        elif self.rect.top < 0:
            self.y = self.height / 2
        self.updateRect()
