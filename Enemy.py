import pygame

from GameObject import GameObject

class Invader(GameObject):
    
    @staticmethod
    def init():
        Invader.invaderImage = pygame.transform.scale(
            pygame.image.load("images/flat,800x800,075,f.u4.jpg"), \
            (82, 60)).convert_alpha()
        newInvaderImage = Invader.invaderImage.copy()
        pygame.transform.threshold(Invader.invaderImage, newInvaderImage, 
            (0, 255, 0), (10, 255, 10), (0, 0, 0, 0))
    
    def __init__(self, x, y):
        self.hp = 5
        self.x, self.y = x, y
        self.xradius, self.yradius = 41, 30
        super(Invader, self).__init__(x, y, Invader.invaderImage, self.xradius, 
            self.yradius)
        self.velocity = [4, 4]
        self.yMoveCount = 0
        self.xMove = True
    
    def update(self, screenWidth, screenHeight):
        
        super(Invader, self).update(screenWidth, screenHeight)
                
        if self.xMove:
            if self.x - self.xradius == 0 or self.x + self.xradius == screenWidth:
                self.xMove = False
                self.velocity[0] = -self.velocity[0]
            else:
                self.x += self.velocity[0]
        elif self.yMoveCount != self.velocity[1] ** 2:
            self.yMoveCount += 1
            self.y += self.velocity[1]
        elif self.yMoveCount == self.velocity[1] ** 2:
            self.xMove = True
            self.yMoveCount = 0
            self.x += self.velocity[0]
                