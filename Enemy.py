from Drawable import Moveable
from Bullet import Bullet
import threading
import time
import pygame


class Enemy(Moveable):
    """
    Enemy class
    """
    def __init__(self, width, height, x, y, color=(255, 255, 255), speed=2):
        super().__init__(width, height, x, y, color, speed)
        pygame.draw.polygon(self.surface, self.color,
                            [[0, 0], [self.width, 0], [self.width / 2, self.height]])
        self.bullets = []

    def getBullets(self):
        return self.bullets

    def move(self, dirFlag, board, player=None):
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
            elif dirFlag is 2:
                self.rect.y += self.speed
                #time.sleep(0.02)
                #print('zapinkaamww!!!!!!!!!!!!!!!')
                if self.aliveFlag and (self.rect.y + self.height) >= player.getRect().y:
                    self.rect.y = (player.getRect().y - self.height)
                    print("COLLISION!!!!!!!!!!!!!!!!!!")
                    #self.aliveFlag = False
                    self.runFlag = False
                    player.aliveFlag = False
            time.sleep(0.03)

    def fire(self, enemies,  width, height, board, color = (255, 255, 255), speed = 5):
        self.bullets.append(Bullet(width, height, self.rect.x + self.width/2 - width/2, self.rect.y + self.height, color, speed))
        threading.Thread(target = self.bullets[-1].move, args = (0, enemies, board)).start()
