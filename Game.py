"""
Created on Fri Jan 11 08:09:12 2019

@author: 
"""

import constants as const
import colors
import Level
import Wall
import Character
import random
from pathlib import Path
import pygame


class Game(object):

    '''
    This is the game object
    '''
    def __init__(self):

        #initialize pygame
        pygame.init()

        #setup music
        file = str(Path.cwd() / "sounds" / "music1.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(file)

        #setup misc pygame settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.start_ticks = 0

        #setup game state variables
        self.gameRunning = True
        self.gameState = const.GAME_STATE_RUNNING
        self.musicOn = False
        self.soundOn = False

        #setup screen
        self.screenWidth = const.MAP_WIDTH * const.TILE_SIZE + const.SCREEN_OFFSET_X_LEFT + const.SCREEN_OFFSET_X_RIGHT
        self.screenHeight = const.MAP_HEIGHT * const.TILE_SIZE + const.SCREEN_OFFSET_Y_TOP + const.SCREEN_OFFSET_Y_BOTTOM
        self.screenSize = self.screenWidth, self.screenHeight
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("BomberDude")
        self.screenImage = pygame.Surface(self.screenSize)    #used to store the screen to an image, useful for transparent menus

        #load starting level
        self.levelNum = 1
        self.level, self.player, self.enemies = Level.startNewLevel(self.levelNum)
        ##enemySprites = pygame.sprite.Group()
        self.spritePlayer = pygame.sprite.Group()
        self.spritePlayer.add(self.player)
        self.spriteEnemies = pygame.sprite.Group()
        self.spriteEnemies.add(self.enemies)

        #player death screen
        ################## Testing ########################## Testing ################# vvvvvv
        imageFile = str(Path.cwd() / "graphics" / "death_temp.png")     #placeholder
        self.death_test_image = pygame.image.load(imageFile).convert_alpha()
        self.death_test_rect = self.death_test_image.get_rect()
        self.death_test_rect.x = int(self.screenWidth / 2 - self.death_test_rect.width / 2)
        self.death_test_rect.y = int(self.screenHeight / 2 - self.death_test_rect.height / 2)
        ################## Testing ########################## Testing ################# ^^^^^^


    #redering/drawing, update frames functions
    def render(self):#level, player, enemies):
        #Render level
        self.drawLevel()#self.level)
        
        #Update and render player
        self.spritePlayer.update(self.level)
        self.spritePlayer.draw(self.screen)

        #Update and render enemies
        self.spriteEnemies.update(self.level)
        self.spriteEnemies.draw(self.screen)

        for enemy in self.spriteEnemies:
            col = pygame.sprite.collide_rect(self.player, enemy)
            if col:
                self.player.state = const.STATE_DEAD
                if self.soundOn:
                    self.player.deathSound.play()

        text1 = str(int(self.clock.get_fps()))
        fps = self.font.render(text1, True, pygame.Color('white'))
        self.screen.blit(fps, (25, 25))


    def checkCollision(self, x1, y1, w1, h1, x2, y2, w2, h2, buffer):
        w1 -= buffer
        h1 -= buffer
        w2 -= buffer
        h2 -= buffer
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

    
    def drawLevel(self):#level):
        for row in range(const.MAP_HEIGHT):
            for column in range(const.MAP_WIDTH):
                self.drawTile(self.level.backgroundImage, column, row)
                try:
                    if isinstance(self.level.layout[row][column], Wall.Wall) and not self.level.layout[row][column].breakable:
                        self.drawTile(self.level.wallImage, column, row)
                    if isinstance(self.level.layout[row][column], Wall.Wall) and self.level.layout[row][column].breakable:
                        self.drawTile(self.level.breakableImage, column, row)
                    if self.level.layout[row][column] == const.TILE_DOOR_OPENED:
                        self.drawTile(self.level.doorOpenedImage, column, row)
                    if self.level.layout[row][column] == const.TILE_DOOR_CLOSED:
                        self.drawTile(self.level.doorClosedImage, column, row)
                except:
                    print("Index out of range error")


    def drawTile(self, image, x, y):
        xres = const.SCREEN_OFFSET_X_LEFT + x * const.TILE_SIZE
        yres = const.SCREEN_OFFSET_Y_TOP + y * const.TILE_SIZE
        self.screen.blit(image, (xres, yres))


    def updateScreen(self):
        pygame.display.update()
        self.screen.fill(colors.Black)
        self.clock.tick(const.FRAMERATE)


    def update(self):
        if self.musicOn:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        self.getUserInput()
        if self.gameState == const.GAME_STATE_RUNNING:
            self.render()#currentLevel, player, enemies)

            if self.player.state == const.STATE_DEAD:
                self.screenImage.blit(self.screen, (0,0), ((0,0), self.screenSize))    #take a snapshot of the screen
                self.gameState = const.GAME_STATE_PLAYER_DEAD
                self.start_ticks = pygame.time.get_ticks() #starter tick

            #display death screen when player dies
        elif self.gameState == const.GAME_STATE_PLAYER_DEAD:
            self.screen.blit(self.screenImage, (0,0))
            self.screen.blit(self.death_test_image, self.death_test_rect)
            seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
            if seconds > const.PLAYER_DEATH_SCREEN_TIMER:
                self.spritePlayer = None
                self.spriteEnemies = None 
                self.level, self.player, self.enemies = Level.startNewLevel(self.levelNum)
                self.spritePlayer = pygame.sprite.Group()
                self.spritePlayer.add(self.player)
                self.spriteEnemies = pygame.sprite.Group()
                self.spriteEnemies.add(self.enemies)
                self.gameState = const.GAME_STATE_RUNNING
        
        self.updateScreen()
        if self.gameState == const.GAME_STATE_QUITTING:
            self.quitGame()


    def getUserInput(self):
        self.getEvents()
        if self.gameState == const.GAME_STATE_RUNNING:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.player.move(const.UP, self.level)
            if key[pygame.K_DOWN]:
                self.player.move(const.DOWN, self.level)
            if key[pygame.K_LEFT]:
                self.player.move(const.LEFT, self.level)
            if key[pygame.K_RIGHT]:
                self.player.move(const.RIGHT, self.level)


    def getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameState = const.GAME_STATE_QUITTING
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameState = const.GAME_STATE_QUITTING
                if event.key == pygame.K_z:     #testing code for door
                    self.level.showDoor()
                if event.key == pygame.K_x:
                    self.level.openDoor()
                if event.key == pygame.K_m:
                    if self.musicOn: 
                        self.musicOn = False
                    else:
                        self.musicOn = True
                if event.key == pygame.K_s:
                    if self.soundOn: 
                        self.soundOn = False
                    else:
                        self.soundOn = True

    
    def quitGame(self):
        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit()
        self.gameRunning = False