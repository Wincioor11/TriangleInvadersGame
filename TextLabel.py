import pygame


class TextLabel:
    def __init__(self, text, x = 10, y = 10, fontName='arial', size=20, color=(255, 255, 255)):
        self.text = text
        self.x = x
        self.y = y
        self.myFont = pygame.font.SysFont(fontName, size)
        self.textLabel = self.myFont.render(str(text), 1, color)
        self.rect = self.textLabel.get_rect(x=self.x, y=self.y)
        self.textLabelFlag = True

    def getWidth(self):
        return self.myFont.size(self.text)[0]

    def getHeight(self):
        return self.myFont.size(self.text)[1]

    def drawOn(self, surface):
        surface.blit(self.textLabel, self.rect)

    def getRect(self):
        return self.rect

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        # when I want to change the position i need to override the rect property
        self.rect = self.textLabel.get_rect(x=self.x, y=self.y)

    def getPosition(self):
        return self.x, self.y



