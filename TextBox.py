import pygame
import pygame.locals
from TextLabel import TextLabel


class TextBox:
    def __init__(self, width, height, x, y, fontName='arial', fontSize=20, fontColor=(0, 0, 0), background=(255, 255, 255)):
        self.width = width
        #self.height = height
        self.x = x
        self.y = y
        self.text = ''
        self.fontName = fontName
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.textLabel = TextLabel(self.text, self.x + 5, self.y + 2.5, self.fontName,
                                   self.fontSize, self.fontColor)
        self.height = self.textLabel.getHeight() + 5
        self.surface = pygame.Surface([self.width, self.height])
        self.rect = self.surface.get_rect(x=self.x, y=self.y)
        pygame.draw.rect(self.surface, (143, 142, 160), (0, 0, self.width, self.height))  # frame
        pygame.draw.rect(self.surface, background, (2, 2, self.width - 4, self.height - 4))  # white board in grey frame

        self.textLabelFlag = True


    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def drawOn(self, surface):
        surface.blit(self.surface, self.rect)
        surface.blit(self.textLabel.textLabel, self.textLabel.rect)

    def getRect(self):
        return self.rect

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        # when I want to change the position i need to override the rect property
        self.rect = self.surface.get_rect(x=self.x, y=self.y)

    def getPosition(self):
        return self.x, self.y

    def getText(self):
        return self.text

    def listenKeyboardEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # removing last char from string and replacing it with former
                    print('BACKSPACE!')
                elif event.key == pygame.K_RETURN:  # K_RETURN is an 'big' enter key name
                    if self.text is not '':
                        return True, True
                else:
                    char = event.unicode
                    self.text += char

                self.textLabel = TextLabel(self.text, self.x + 5, self.y + 2.5, self.fontName,
                                           self.fontSize, self.fontColor)
        return False, False
