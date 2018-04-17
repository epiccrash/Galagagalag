import pygame

from GameObject import GameObject

class Player(GameObject):
    
    @staticmethod
    def init():
        # Image from http://chickeninvaders.wikia.com/wiki/File:Galaga_ship.png
        Player.playerImage = pygame.transform.scale(
            pygame.image.load("images/Galaga_ship.png"), (64, 64))
    
    def __init__(self, x, y):
        self.xradius, self.yradius = 32, 32
        super(Player, self).__init__(x, y, Player.playerImage, self.xradius, 
            self.yradius)
        self.invulnTime = 0
        self.velocity = [8, 8]
        self.speed = [0, 0]
        self.dashSpeedBonus = 20
        self.rechargeTime = 7
        self.speedUpTime = 8
        self.speedCount = 0
        self.speedUpEnabled = True
        #self.lastPosition = (x, y)
    
    def update(self, dt, keysDown, screenWidth, screenHeight):
        self.invulnTime += 1      

        if (keysDown(pygame.K_LEFT) or keysDown(pygame.K_a)):
            self.x -= self.velocity[0]
        elif (keysDown(pygame.K_RIGHT) or keysDown(pygame.K_d)):
            self.x += self.velocity[0]
        if (keysDown(pygame.K_UP) or keysDown(pygame.K_w)):
            self.y -= self.velocity[1]
        elif (keysDown(pygame.K_DOWN) or keysDown(pygame.K_s)):
            self.y += self.velocity[1]

        if (keysDown(pygame.K_LSHIFT) and self.speedUpEnabled 
            and self.speedCount == 0):
            self.velocity[0] += self.dashSpeedBonus
            self.velocity[1] += self.dashSpeedBonus
            self.speedCount += 1
            Player.playerImage.set_alpha(200)
        
        if self.speedCount == self.speedUpTime:
            self.velocity[0] -= self.dashSpeedBonus
            self.velocity[1] -= self.dashSpeedBonus
            self.speedCount = 1
            self.speedUpEnabled = False
            Player.playerImage.set_alpha(255)
        
        if not self.speedUpEnabled and self.speedCount == self.rechargeTime:
            self.speedCount = 0
            self.speedUpEnabled = True
        elif self.speedCount > 0 and self.speedCount < self.speedUpTime:
            self.speedCount += 1
          
        super(Player, self).update(screenWidth, screenHeight)
        
        #self.lastPosition = (self.x, self.y)
    
    def isInvulnerable(self):
        return self.maxInvulnTime > self.invulnTime