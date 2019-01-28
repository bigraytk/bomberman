"""
Created on Fri Jan 11 08:09:12 2019

@author: 
"""
import sys
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
        self.gameState = const.GAME_STATE_MENU
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

        #retreive total number of levels stored in data directory
        self.numLevels = 0
        dataDir = Path.cwd() / "data"
        for f in dataDir.glob('level*.csv'):
            self.numLevels += 1

        #Create sprite groups
        self.spritePlayer = pygame.sprite.Group()
        self.spritePlayer.add(self.player)
        self.spriteEnemies = pygame.sprite.Group()
        self.spriteEnemies.add(self.enemies)
        self.spriteBombs = pygame.sprite.Group()

        #self.testsprite  = Level.tileSprite(self.level.backgroundImage, 1, 1)

        #self.tile_group = pygame.sprite.LayeredDirty()  #dirty sprites can be used for optimized tilemaps, but I didn't see much improvement
        #for y in range(self.level.levelHeight):
        #    for x in range(self.level.levelWidth):
        #        if isinstance(self.level.layout[y][x], Wall.Wall) and not self.level.layout[y][x].breakable:
        #            tile  = Level.tileSprite(self.level.wallImage, x, y)
        #        else:
        #            tile  = Level.tileSprite(self.level.backgroundImage, x, y)
        #        self.tile_group.add(tile)
        


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
        #for tile in self.tile_group:               ### could be used to optimize drawing tiles, but requires a lot of changes to do so
        #    if pygame.sprite.spritecollideany(tile, self.enemies):     ### also, tested the optimization and it's not any faster
        #        tile.dirty = True
        #self.tile_group.draw(self.screen)
        self.drawLevel()#self.level)
        
        #Update and render enemies
        self.spriteEnemies.update(self.level, self.player)
        self.spriteEnemies.draw(self.screen)
        self.spriteBombs.draw(self.screen)

        #for enemy in self.spriteEnemies:
        #    if enemy.logic == const.ADVANCED:
        #        if enemy.pursuePlayer:
        #            pygame.draw.rect(self.screen, (255, 0, 0), enemy.hitbox, 2)  #Draws player's collision box, for testing purposes
        #        else:
        #            pygame.draw.rect(self.screen, (255, 255, 0), enemy.hitbox, 2)  #Draws player's collision box, for testing purposes

        #Update and render player
        self.spritePlayer.update(self.level)
        self.spritePlayer.draw(self.screen)
        #pygame.draw.rect(self.screen, (255, 255, 0), self.player.hitbox, 2)  #Draws player's collision box, for testing purposes

        for enemy in self.spriteEnemies:
            if enemy.logic == const.ADVANCED:
                pass
            if enemy.rect.colliderect(self.player.hitbox):
                self.player.state = const.STATE_DEAD
                self.updateScore()
                if self.soundOn:
                    self.player.deathSound.play()

        text1 = str(int(self.clock.get_fps()))
        fps = self.font.render(text1, True, pygame.Color('white'))
        self.screen.blit(fps, (25, 25))


    def checkCollision(self, sprite, spriteGroup):
        return pygame.sprite.spritecollide(sprite, spriteGroup, False)

    
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

        #Check current game state
        if self.gameState == const.GAME_STATE_RUNNING:
            self.render()
            self.checkPlayerProgress()

            if self.player.state == const.STATE_DEAD:
                self.screenImage.blit(self.screen, (0,0), ((0,0), self.screenSize))    #take a snapshot of the screen
                self.gameState = const.GAME_STATE_PLAYER_DEAD
                self.start_ticks = pygame.time.get_ticks() #starter tick

        #display death screen when player dies, then reset level
        elif self.gameState == const.GAME_STATE_PLAYER_DEAD:
            self.screen.blit(self.screenImage, (0,0))
            self.screen.blit(self.death_test_image, self.death_test_rect)
            seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
            if seconds > const.PLAYER_DEATH_SCREEN_TIMER:
                self.resetLevel()

        elif self.gameState == const.GAME_STATE_MENU:
            self.mainMenu()
        self.updateScreen()
        if self.gameState == const.GAME_STATE_QUITTING:
            self.quitGame()


    def resetLevel(self):
        for enemy in self.spriteEnemies:
            enemy.kill()
        for bomb in self.spriteBombs:
            bomb.kill()
        self.spritePlayer.empty()
        self.spriteEnemies.empty()
        self.level, self.player, self.enemies = Level.startNewLevel(self.levelNum)
        #self.spritePlayer = pygame.sprite.Group()
        self.spritePlayer.add(self.player)
        #self.spriteEnemies = pygame.sprite.Group()
        self.spriteEnemies.add(self.enemies)
        self.gameState = const.GAME_STATE_RUNNING


    def checkPlayerProgress(self):
        if self.level.layout[self.player.y][self.player.x] == const.TILE_DOOR_OPENED and self.player.state == const.STATE_IDLE:
            if self.levelNum < self.numLevels:
                self.levelNum += 1
                self.resetLevel()
            else:
                #TODO player wins game?
                pass


    #User keyboard input, game controls
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
            if key[pygame.K_SPACE]:
                newBomb = self.player.dropBomb()
                if newBomb:
                    self.spriteBombs.add(newBomb)


    #Event-driven input
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameState = const.GAME_STATE_QUITTING
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.gameState != const.GAME_STATE_MENU:
                        self.gameState = const.GAME_STATE_MENU
                    else:
                        self.gameState = const.GAME_STATE_QUITTING
                elif event.key == pygame.K_f:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode(self.screenSize)
                    else:
                        pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
                elif event.key == pygame.K_m:
                    if self.musicOn: 
                        self.musicOn = False
                    else:
                        self.musicOn = True
                elif event.key == pygame.K_s:
                    if self.soundOn: 
                        self.soundOn = False
                    else:
                        self.soundOn = True
                self.debug_mode(event)          #Testing purposeses  #TODO  remove


    def mainMenu(self):

        newGameLocLeft = 500
        newGameLocTop = 200
        highScoreLocLeft = 500
        highScoreLocTop = 300
        '''Will display the main menu.'''
        self.screen.fill(const.GREY)

        graphicsDir = Path.cwd() / "graphics"
        print(graphicsDir)
        NewGameGraph = str(graphicsDir.joinpath("NewGameButton.png"))
        newGameButt = pygame.image.load(NewGameGraph)
        NewGameGraphRed = str(graphicsDir.joinpath("NewGameButton_Red.png"))
        newGameButtRed = pygame.image.load(NewGameGraphRed)
        ngRect = pygame.Rect(newGameLocLeft,newGameLocTop,200,50)
        highScoreGraph = str(graphicsDir.joinpath("HighScores.png"))
        highScoreButt = pygame.image.load(highScoreGraph)
        highScoreGraphRed = str(graphicsDir.joinpath("HighScores_Red.png"))
        highScoreButtRed = pygame.image.load(highScoreGraphRed)
        hsRect = pygame.Rect(highScoreLocLeft,highScoreLocTop,200,50)
        mousex = 0
        mousey = 0
        hoveringNG = False
        hoveringHS = False

        #main menu loop
        #print('game state' , self.gameState)
        while self.gameState == const.GAME_STATE_MENU:
            mouseClicked = False
            
            if hoveringNG == False:
                self.screen.blit(newGameButt,(newGameLocLeft,newGameLocTop))
            if hoveringHS == False:
                self.screen.blit(highScoreButt,(highScoreLocLeft,highScoreLocTop))
            #pygame.draw.rect(DISPLAYSURF,RED,ngRect)
            #hoveringNG = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    mousex,mousey = event.pos
                    if ngRect.collidepoint(mousex,mousey):
                        hoveringNG = True
                        self.screen.blit(newGameButtRed,(newGameLocLeft,newGameLocTop))
                    elif not ngRect.collidepoint(mousex,mousey):
                        hoveringNG = False
                    if hsRect.collidepoint(mousex,mousey):
                        hoveringHS = True
                        print('test')
                        self.screen.blit(highScoreButtRed,(highScoreLocLeft,highScoreLocTop))
                    elif not hsRect.collidepoint(mousex,mousey):
                        hoveringHS = False
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex,mousey = event.pos
                    print(mousex,mousey)
                    if ngRect.collidepoint(mousex,mousey):
                        #TODO
                        #change game state and start the 1st level
                        self.gameState = const.GAME_STATE_RUNNING
                    elif hsRect.collidepoint(mousex,mousey):
                        #TODO
                        #show the high score screen
                        pass
                        
                    
                    
            pygame.display.update()
        


    def updateScore(self):
        #TODO
        pass
    

    def quitGame(self):
        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit()
        self.gameRunning = False


    #TODO  remove before release
    def debug_mode(self, event):
        if event.key == pygame.K_z:     #testing code for door
            self.level.showDoor()
        elif event.key == pygame.K_x:
            self.level.openDoor()
        elif event.key == pygame.K_k:   #kill all enemies on screen
            for enemy in self.spriteEnemies:
                enemy.kill()
        elif event.key == pygame.K_COMMA:
            if self.levelNum > 1:
                self.levelNum -= 1
                self.resetLevel()
        elif event.key == pygame.K_PERIOD:
            if self.levelNum < self.numLevels:
                self.levelNum += 1
                self.resetLevel()
        