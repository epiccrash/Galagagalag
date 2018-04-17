# Joey Perrino, Andrew ID: jperrino; for the 2018 Spring 15-112 Term Project

# This code is used to import Austin's module manager; much thanks to him!
# https://raw.githubusercontent.com/CMU15-112/module-manager/master/module_manager.py
import module_manager
module_manager.review()
import pygame

import random

from pygamegame import PygameGame
from Player import Player
from Attack import PlayerLaser, EnemyLaser
from Enemy import Invader

class Game(PygameGame):
    
    def init(self):
        pRadius = 32
        self.bgColor = (0, 0, 0)
        Player.init()
        player = Player(self.width / 2, self.height - pRadius)
        self.playerGroup = pygame.sprite.GroupSingle(player)

        self.autofireEnabled = False
        self.laserEnabled = True
        self.singleShot = True
        self.doubleShot = False
        self.tripleShot = False # Currently unused
        self.rechargeTime = 25
        self.chargeCount = 0
        self.playerLasers = pygame.sprite.Group()
        
        Invader.init()
        invader = Invader(self.width / 2, pRadius)
        self.enemyGroup = pygame.sprite.Group()
        self.enemyGroup.add(invader)
        
        self.enemyLasers = pygame.sprite.Group()
    
    def timerFired(self, dt):
        self.playerGroup.update(dt, self.isKeyPressed, self.width, self.height)
        
        self.playerLasers.update(self.width, self.height)
        if ((self.isKeyPressed(pygame.K_SPACE) or self.autofireEnabled) 
            and self.laserEnabled):
            player = self.playerGroup.sprites()[0]
            xSpawn, ySpawn = player.x, player.y - player.yradius
            if self.singleShot:
                self.playerLasers.add(PlayerLaser(xSpawn, ySpawn))
            if self.doubleShot:
                self.playerLasers.add(PlayerLaser(
                    xSpawn - (player.xradius - 2), ySpawn + player.yradius))
                self.playerLasers.add(PlayerLaser(
                    xSpawn + (player.xradius - 2), ySpawn + player.yradius))
            self.laserEnabled = False
        
        if not self.laserEnabled:
            if self.chargeCount == self.rechargeTime:
                self.laserEnabled = True
                self.chargeCount = 0
            else:
                self.chargeCount += 1
        
        self.enemyLasers.update(self.width, self.height)
        for enemy in self.enemyGroup:
            if random.randint(0, 30) == 30:
                self.enemyLasers.add(EnemyLaser(enemy.x, enemy.y))
            
        self.enemyGroup.update(self.width, self.height)
        
    def redrawAll(self, screen):
        self.playerLasers.draw(screen)
        self.playerGroup.draw(screen)
        self.enemyGroup.draw(screen)
        self.enemyLasers.draw(screen)

Game(650, 800).run()