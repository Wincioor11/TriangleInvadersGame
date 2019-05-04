import pygame


class Board:

    def __init__(self, width, height):
        """
        Constructor that makes a game board
        :param width:
        :param height:
        """
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption('Triangle Invaders Game')

    def drawGUI(self, textLabels, *drawable):
        """
        Draw method for displaying only text fields and buttons
        Used for initial screen and ending one
        :return:
        """
        backgroundColor = (0, 0, 0)  # color in RGb
        self.surface.fill(backgroundColor)
        for textLabel in textLabels:
            textLabel.drawOn(self.surface)

        for drawable in drawable:
            drawable.drawOn(self.surface)

        # display it in game window
        #pygame.display.update()

    def drawGame(self, enemies, player, bullets, textLabels):
        """
        Draw method used for drawing all visual elements of the game
        :param args:
        :return:
        """
        backgroundColor = (30, 29, 50) # color in RGb
        self.surface.fill(backgroundColor)

        for textLabel in textLabels:
            textLabel.drawOn(self.surface)

        player.drawOn(self.surface)
        for drawable in enemies:
            drawable.drawOn(self.surface)
        for drawable in bullets:
            drawable.drawOn(self.surface)

        # display it in game window
        #pygame.display.update()

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def updateScreen(self):
        pygame.display.update()