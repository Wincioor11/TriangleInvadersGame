import pygame
import pygame.locals
import Board
from Enemy import Enemy
from Player import Player
from Bullet import Bullet
from threading import Timer
from TextLabel import TextLabel
from TextBox import TextBox
import threading
import time
import random
from DataBase import DataBase

TRIANGLE_SIZE = 40
BULLET_SIZE = 6
MAX_ROW_OF_ENEMIES = 6
START_LEVEL = 1
#MAX_LEVEL = 24



class SpaceInvadersGame:
    """
    Game class
    """
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.board = Board.Board(width, height)
        self.player = Player(TRIANGLE_SIZE, TRIANGLE_SIZE, width/2 - TRIANGLE_SIZE/2, height*5/6)

        self.level = START_LEVEL
        self.enemies = self.getEnemies(self.level)
        self.bulletToDisplay = []
        self.ammoToDisplay = []
        self.clock = pygame.time.Clock()

        self.gameFlag = False
        self.timerFlag = False

        self.moveThread = ''
        self.enemiesMovementThread = ''

        self.gameTime = 0  # don't know why, but I created some kind of game timer
        self.levelTime = 0
        self.currFps = 0

        self.TextFieldLabels = []
        self.textBoxEnter = ''
        self.playerName = ''

        self.db = DataBase('scores.db')
        self.db.connect()
        self.db.addScoreTable('scoresTable')
        self.db.close()

    def run(self):
        """
        Main loop
        """
        self.setGUI(0)
        while not self.gameFlag:
            # self.handleEvents()
            self.gameFlag, self.timerFlag = self.textBoxEnter.listenKeyboardEvents()
            self.board.drawGUI(
                self.TextFieldLabels,
                self.textBoxEnter,
            )
            self.board.updateScreen()
            self.clock.tick(60)  # 60 fps

        if self.textBoxEnter.getText() is not '':
            self.playerName = self.textBoxEnter.getText()

        pygame.time.set_timer(pygame.USEREVENT+1, 1000) # timer that calls user event nr 25 that can be handled
        self.enemiesMovementThread = threading.Thread(target=self.startEnemiesMovement)
        self.enemiesMovementThread.start()

        while self.gameFlag:
            self.handleEvents()
            self.ammoCheck()
            self.currFps = self.clock.get_fps()
            self.board.drawGame(
                self.enemies,
                self.player,
                self.bulletToDisplay + self.ammoToDisplay,
                [   # I dont addd dependency between text size and their position on the screen coz
                    # I want to dynamic change the text inside these text fields and I would need another method to doit
                    TextLabel('Level: {}'.format(self.level), 10, 10, 'comic', 20, (222, 127, 233)),
                    TextLabel('Time: {} s'.format(self.gameTime), self.width - 80, self.height - 30, 'comic', 20, (222, 127, 233)),
                    TextLabel('Fps: {}'.format(int(self.currFps)), self.width - 60, 10, 'comic', 20, (222, 127, 233))
                 ],
             )
            self.board.updateScreen()
            self.gameLogic()
            self.clock.tick(60)  # 60 fps

        self.db.connect()
        bestScoreRow = self.db.getRowsWhereNameIs('scoresTable', self.playerName)
        if len(bestScoreRow)>0:
            if self.level > bestScoreRow[0][2]:
                self.db.updateRow('scoresTable', self.playerName, (self.playerName, self.level))
        else:
            self.db.addRow('scoresTable', (self.playerName, self.level))
        self.db.close()

        self.cleanAfterDeath()

        while not self.gameFlag:
            self.handleEvents()
            self.board.drawGUI(
                self.TextFieldLabels,
            )
            self.board.updateScreen()
            self.clock.tick(60)  # 60 fps

    def restart(self):
        self.gameFlag = True
        self.timerFlag = True
        # revieve a player :)
        self.player = Player(TRIANGLE_SIZE, TRIANGLE_SIZE, self.width/2 - TRIANGLE_SIZE/2, self.height*5/6)
        self.level = START_LEVEL
        self.gameTime = 0
        self.enemies = self.getEnemies(self.level)
        self.TextFieldLabels.clear()
        self.run()

    def cleanAfterDeath(self):
        self.timerFlag = False
        self.enemies.clear()
        self.setGUI(1)
        for bullet in self.bulletToDisplay:
            bullet.aliveFlag = False
            bullet.runFlag = False
        # self.bulletToDisplay.clear()
        self.board.drawGUI(
            self.TextFieldLabels,
        )
        self.board.updateScreen()
        time.sleep(1)
        self.setGUI(2)
        pygame.event.clear()

    def setGUI(self, whichGUI):
        self.TextFieldLabels.clear()
        if whichGUI is 0:
            triangleText = TextLabel('TRIANGLE', 0,0, 'comic', 80, (255, 255, 255))
            triangleText.setPosition(self.width / 2 - triangleText.getWidth() / 2, 100)
            self.TextFieldLabels.append(triangleText)

            invadersText = TextLabel('INVADERS', 0, 0, 'comic', 80, (255, 255, 255))
            invadersText.setPosition(self.width / 2 - invadersText.getWidth() / 2,
                                 triangleText.getPosition()[1] + triangleText.getHeight())
            self.TextFieldLabels.append(invadersText)

            gameText = TextLabel('GAME', 0,0, 'comic', 80, (255, 255, 255))
            gameText.setPosition(self.width / 2 - gameText.getWidth() / 2,
                                 invadersText.getPosition()[1] + invadersText.getHeight())
            self.TextFieldLabels.append(gameText)

            enter = TextLabel('Please enter your name', 0,0, 'comic', 30, (255, 255, 255))
            enter.setPosition(self.width / 2 - enter.getWidth() / 2,
                              gameText.getPosition()[1] + gameText.getHeight()*2)
            self.TextFieldLabels.append(enter)

            self.textBoxEnter = TextBox(triangleText.getWidth(), None,
                                        self.width / 2 - triangleText.getWidth() /2,
                                        enter.getPosition()[1] + enter.getHeight()*2)

            # checkbox info here
        elif whichGUI is 1 or whichGUI is 2:
            gameOver = TextLabel('GAME OVER!', 0, 0, 'comic', 80, (255, 255, 255))
            gameOver.setPosition(self.width / 2 - gameOver.getWidth() / 2, 100)
            self.TextFieldLabels.append(gameOver)

            score = TextLabel('Your score: {}'.format(self.level), 0, 0, 'comic', 80, (255, 255, 255))
            score.setPosition(self.width / 2 - score.getWidth() / 2, gameOver.getPosition()[1] + gameOver.getHeight())
            self.TextFieldLabels.append(score)

            if whichGUI is 2:
                pressSpace = TextLabel('Press SPACE to restart game', 0, 0, 'comic', 50, (255, 255, 255))
                pressSpace.setPosition(self.width / 2 - pressSpace.getWidth() / 2, self.height / 2)
                self.TextFieldLabels.append(pressSpace)

                pressTab = TextLabel('Hold TAB to see best scores', 0, 0, 'comic', 50, (255, 255, 255))
                pressTab.setPosition(self.width / 2 - pressTab.getWidth() / 2,
                                     pressSpace.getPosition()[1] + pressSpace.getHeight() * 2)
                self.TextFieldLabels.append(pressTab)
        elif whichGUI is 3:
            bestScores = TextLabel('BEST SCORES:', 0, 0, 'comic', 60, (255, 255, 255))
            bestScores.setPosition(self.width / 2 - bestScores.getWidth() / 2, 50)
            self.TextFieldLabels.append(bestScores)

            # connecting to database and reading TOP 10 scores!
            self.db.connect()
            rows = self.db.getTop10('scoresTable')
            self.db.close()
            fakeName = TextLabel(str(rows[0][1]), 0, 0, 'comic', 30, (255, 255, 255))
            fakeName.setPosition(bestScores.getPosition()[0],
                                  bestScores.getPosition()[1] + bestScores.getHeight() * 2)
            self.TextFieldLabels.append(fakeName)

            fakeScore = TextLabel(str(rows[0][2]), 0, 0, 'comic', 30,
                                  (255, 255, 255))
            fakeScore.setPosition(bestScores.getPosition()[0] + bestScores.getWidth() - fakeScore.getWidth(),
                                  bestScores.getPosition()[1] + bestScores.getHeight() * 2)
            self.TextFieldLabels.append(fakeScore)
            for x in range(1, len(rows)):
                previousName = fakeName
                previousScore = fakeScore
                fakeName = TextLabel(str(rows[x][1]), 0, 0, 'comic', 30, (255, 255, 255))
                fakeName.setPosition(bestScores.getPosition()[0],
                                     previousName.getPosition()[1] + previousName.getHeight() * 2)
                self.TextFieldLabels.append(fakeName)

                fakeScore = TextLabel(str(rows[x][2]), 0, 0, 'comic', 30,
                                      (255, 255, 255))
                fakeScore.setPosition(bestScores.getPosition()[0] + bestScores.getWidth() - fakeScore.getWidth(),
                                      previousScore.getPosition()[1] + previousScore.getHeight() * 2)
                self.TextFieldLabels.append(fakeScore)

    def tickTime(self):
        self.gameTime += 1
        self.levelTime += 1

    def bulletsLogic(self):
        for bullet in self.bulletToDisplay:
            if not bullet.isAlive():
                self.bulletToDisplay.remove(bullet)
                if bullet in self.player.getBullets():
                    self.player.getBullets().remove(bullet)
                else:
                    for enemy in self.enemies:
                        if bullet in enemy.getBullets():
                            enemy.getBullets().remove(bullet)

    def enemiesLogic(self):
        for enemy in self.enemies:
            if not enemy.isAlive():
                self.enemies.remove(enemy)
                self.levelLogic()  # levelLogic method checks if it has to spawn new enemies only when some of them dies

    def playerLogic(self):
        if not self.player.isAlive():
            self.gameFlag = False

    def levelLogic(self):
        if len(self.enemies) == 0:
            Timer(1.5, self.levelUp).start() # timer waits 1.5 seconds in background before spawning new enemies

    def ammoCheck(self):
        self.ammoToDisplay.clear()
        self.ammoToDisplay += self.player.getAmmo()

    def randomEnemyShots(self):
        for enemy in self.enemies:
            if random.randrange(0,100) <= 10:
                enemy.fire([self.player], BULLET_SIZE, BULLET_SIZE, self.board, (240, 20, 20))
                self.bulletToDisplay += enemy.getBullets()

    def gameLogic(self):
        self.bulletsLogic()
        self.enemiesLogic()
        self.playerLogic()

    def levelUp(self):
        self.level += 1
        self.enemies = self.getEnemies(self.level)

    def handleEvents(self):
        """
        Events handling method for e.g. MOUSEMOTION
        """
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                self.gameFlag = False
                self.timerFlag = False

            # events which can be handled only if game is running
            if self.gameFlag:
                if event.type == pygame.USEREVENT+1:
                    self.tickTime()
                    self.randomEnemyShots()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        print('RIGHT KEY DOWN')
                        self.dirFlag = 1
                        self.moveThread = threading.Thread(target = self.player.move, args = [self.dirFlag, self.board])
                        self.moveThread.start()
                    if event.key == pygame.K_LEFT:
                        print('LEFT KEY DOWN')
                        self.dirFlag = 0
                        self.moveThread = threading.Thread(target=self.player.move, args = [self.dirFlag, self.board])
                        self.moveThread.start()
                    if event.key == pygame.K_SPACE:
                        print('SPACE DOWN')
                        self.player.fire(self.enemies, BULLET_SIZE, BULLET_SIZE, self.board)
                        self.bulletToDisplay += self.player.getBullets()
                        #self.ammoToDisplay.pop()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        print('RIGHT KEY UP!')
                        if self.moveThread.is_alive():
                            self.player.runFlag = False
                    if event.key == pygame.K_LEFT:
                        print('LEFT KEY UP!')
                        if self.moveThread.is_alive():
                            self.player.runFlag = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('RESTART')
                        self.restart()
                    if event.key == pygame.K_TAB:
                        self.setGUI(3)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        self.setGUI(2)

    def getRandomColor(self):
        """
        Method for creating random colors for enemies
        :return randomColor: tuple with random RGB values
        """
        randomColor = [0, 0, 0]
        for x in range(0, 3):
            randomColor[x] = random.randrange(100, 255, 1)
        return randomColor

    def getEnemies(self, level):
        """
        Method which creates a list of enemies (with their positions) to spawn, from center, continuously, to sides
        The algorithm after reaching the boundary of max number of enemies in single row, creates another rows,
        starting from the center again :)
        :param level: player's level in game
        :return enemiesList: list of currently spawned enemies
        """
        enemiesList = []
        for x in range(0, level):
            x += 1
            y = 1 + int((x - 1) / MAX_ROW_OF_ENEMIES)

            denominator = level + 1
            if x <= MAX_ROW_OF_ENEMIES * int((level-1) / MAX_ROW_OF_ENEMIES):
                denominator = MAX_ROW_OF_ENEMIES + 1
            else:
                denominator -= int((level-1) / MAX_ROW_OF_ENEMIES) * MAX_ROW_OF_ENEMIES

            x -= MAX_ROW_OF_ENEMIES * int((x - 1) / MAX_ROW_OF_ENEMIES)
            # between enemies but only to value which depends on MAX_ROW_OF_ENEMIES
            # denominator = level+1 - MAX_ROW_OF_ENEMIES * int((level-1)/MAX_ROW_OF_ENEMIES)

            enemiesList.append(Enemy(TRIANGLE_SIZE, TRIANGLE_SIZE, (self.width * x / denominator) - TRIANGLE_SIZE / 2,
                                     (self.height * y / 6) - TRIANGLE_SIZE / 2, self.getRandomColor()))

        self.levelTime = 0
        return enemiesList

    def startEnemiesMovement(self):
        """
        Method that imitates movements of enemies
        Should be run in thread
        """
        iteration = 0
        while self.gameFlag:
            time.sleep(0.1)
            for enemy in self.enemies:
                threading.Thread(target=enemy.move, args=[iteration % 2 == 0, self.board]).start()
                if self.levelTime % 5 == 0 and self.levelTime != 0:
                    threading.Thread(target=enemy.move, args=[2, self.board, self.player]).start()

            time.sleep(0.4)
            for enemy in self.enemies:
                enemy.runFlag = False


            iteration += 1
            if iteration >= 2:
                iteration = 0




if __name__ == "__main__":
    game = SpaceInvadersGame(600, 600)
    game.run()
