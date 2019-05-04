from Drawable import Moveable
from Bullet import Bullet
import threading
import time
import pygame

MAX_AMMO = 10
BULLET_SIZE = 6

class Player(Moveable):
    """
    Player class
    """
    def __init__(self, width, height, x, y, color = (255, 255, 255), speed = 5 ):
        super().__init__(width, height, x, y, color, speed)
        pygame.draw.polygon(self.surface, self.color, [[0, self.height],[self.width, self.height], [self.width/2, 0]])
        self.bullets = []
        self.ammo = []

    def getBullets(self):
        return self.bullets

    def move(self, dirFlag, board):
        self.runFlag = True
        while self.runFlag:
            if dirFlag == 1:
                self.rect.x += self.speed
                if self.rect.x > board.getWidth() - self.width:
                    self.rect.x = board.getWidth() - self.width
            elif dirFlag == 0:
                self.rect.x -= self.speed
                if self.rect.x < 0:
                    self.rect.x = 0
            time.sleep(0.03)

    def fire(self, enemies,  width, height, board, color = (255, 255, 255), speed = 5):
        if len(self.bullets) < MAX_AMMO:
            self.bullets.append(Bullet(width, height, self.rect.x + self.width/2 - width/2, self.rect.y, color, speed))
            threading.Thread(target = self.bullets[-1].move, args = (1, enemies, board)).start()
            print(MAX_AMMO - len(self.bullets))

    def getAmmo(self):
        self.ammo.clear()
        for x in range(0, MAX_AMMO - len(self.bullets)):
            self.ammo.append(Bullet(BULLET_SIZE, BULLET_SIZE, 10 + x * (BULLET_SIZE + 2), self.rect.y + self.height + 20))

        return self.ammo
