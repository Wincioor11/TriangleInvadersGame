import pygame


class Drawable:
    """
    Super class for all game objects which will be displayed
    """
    def __init__(self, width, height, x, y, color = (255, 255, 255)):
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=self.x, y=self.y)


    def drawOn(self, surface):
        surface.blit(self.surface, self.rect)

    def getRect(self):
        return self.rect

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height


class Moveable(Drawable):
    """
    Super class for all game objects which will be displayed and moved on screen
    """
    def __init__(self, width, height, x, y, color = (255, 255, 255), speed = 5):
        super().__init__(width, height, x, y, color)
        self.speed = speed
        self.runFlag = True
        self.aliveFlag = True

    def isAlive(self):
        return self.aliveFlag

    def explode(self):
        pass
