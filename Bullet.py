from Drawable import Moveable
import time
import pygame


class Bullet(Moveable):
    """
    Bullet class
    """
    def __init__(self, width, height, x, y, color = (255, 255, 255), speed = 5 ):
        super().__init__(width, height, x, y, color, speed)
        pygame.draw.ellipse(self.surface, self.color, (0, 0, width, height))

    def move(self, dirFlag, enemies, board = None):
        self.runFlag = True
        while self.runFlag:
            if dirFlag == 1:  # player's bullet's move
                self.rect.y -= self.speed
                if self.rect.y < 0:
                    self.runFlag = False
                    self.aliveFlag = False
            else:  # enemy's bullet's move
                self.rect.y += self.speed
                if self.rect.y > board.getHeight():
                    self.runFlag = False
                    self.aliveFlag = False

            # this loop must search for collisions every time,
            # coz enemies parameter can be also a one-item list with player
            for enemy in enemies:
                if self.rect.colliderect(enemy.getRect()):
                    self.runFlag = False
                    #enemy.explode() ##################### napisac to
                    self.aliveFlag = False
                    enemy.aliveFlag = False
                    print('KABOOM')

            time.sleep(0.02)
