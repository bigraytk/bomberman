"""
Created on Fri Jan 11 08:09:12 2019

@author: 
"""
#import sys
import constants as const
import colors
import Level
import Wall
import Character
import Bomb
import Powerup
import MainMenu
import StatusBar
import HighScore
import random
from pathlib import Path
import pygame


class Game(object):

    '''
    This is the game object
    '''
    def __init__(self):
        self.states = {const.GAME_STATE_MENU : self.stateMainMenu,
          const.GAME_STATE_RUNNING           : self.stateGameRunning,
          const.GAME_STATE_PLAYER_DEAD       : self.statePlayerDead,
          const.GAME_STATE_QUITTING          : self.stateQuitting,
          const.GAME_STATE_HIGHSCORES        : self.stateHighScores}

        #initialize pygame
        pygame.init()

        #setup music and sound
        musicFile = str(Path.cwd() / "sounds" / "music1.mp3")
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(musicFile)

        self.explodeSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "bomb.wav"))
        self.deathSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "yell.wav"))


        #setup misc pygame settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.start_ticks = 0

        #setup game state variables
        self.gameRunning = True
        self.gameOver = False
        self.exitingToMenu = False
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

        #sets up the MainMenu and High scores Screen
        self.theMainMenu = MainMenu.MainMenu(self.screen, self.screenWidth, self.screenHeight)
        self.highScores = HighScore.HighScore(self.screen, self.screenWidth, self.screenHeight)

        #load starting level
        self.levelNum = 1
        self.level, self.player, self.enemies, self.boss = Level.startNewLevel(self.levelNum)

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
        #self.spriteDeadEnemies = pygame.sprite.Group()
        self.spriteBombs = pygame.sprite.Group()
        self.spriteBombBlasts = pygame.sprite.Group()
        self.spritePowerups = pygame.sprite.Group()

        
        self.statusBar = StatusBar.StatusBar(0, 0)
        self.statusBar.addIcon("front.png", 0, True)
        #self.statusBar.addIcon("bomb.png", 1)
        self.statusBar.addIcon("powerup_boot.png", 2, False, const.ICON_SCALE + 5)
        self.statusBar.addIcon("powerup_range.png", 3, False)
        self.statusBar.addIcon("powerup_count.png", 4, False)


        #player death screen
        ################## Testing ########################## Testing ################# vvvvvv
        imageFile = str(Path.cwd() / "graphics" / "death_screen.png")     #placeholder
        self.death_test_image = pygame.image.load(imageFile).convert_alpha()
        self.death_test_rect = self.death_test_image.get_rect()
        self.death_test_rect.x = int(self.screenWidth / 2 - self.death_test_rect.width / 2)
        self.death_test_rect.y = int(self.screenHeight / 2 - self.death_test_rect.height / 2)

        imageFile = str(Path.cwd() / "graphics" / "game_over_screen.png")     #placeholder
        self.gameOverImage = pygame.image.load(imageFile).convert_alpha()
        ################## Testing ########################## Testing ################# ^^^^^^
        imageFile = str(Path.cwd() / "graphics" / "border.png")
        self.borderImage = pygame.image.load(imageFile).convert()


    #redering/drawing, update frames functions
    def render(self):#level, player, enemies):
        #Render level

        self.screen.blit(self.borderImage, (0, 0))
        self.drawStatusBar()
        #self.test.draw(self.screen)
        self.drawLevel()
        
        #Update and render enemies
        self.spriteEnemies.update(self.level, self.player)
        self.spriteEnemies.draw(self.screen)

        self.spriteBombs.update(self.level)
        self.spriteBombs.draw(self.screen)

        self.spriteBombBlasts.update()
        self.spriteBombBlasts.draw(self.screen)

        self.spritePowerups.update()   #TODO uncomment when finished
        self.spritePowerups.draw(self.screen)

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
            if enemy.rect.colliderect(self.player.hitbox) and enemy.state != const.STATE_DYING:
                self.killPlayer()
            if pygame.sprite.spritecollideany(enemy, self.spriteBombBlasts, collided = None):
                if enemy.kind == const.BOSS:
                    if enemy.takeDamage():
                      self.player.increaseScore(const.ENEMY_DIED)  
                else:
                    enemy.destroy()
                    self.player.increaseScore(const.ENEMY_DIED)
        if not self.spriteEnemies:  #check if no more enemies left
            self.level.openDoor()

        for blast in self.spriteBombBlasts:
            if blast.rect.colliderect(self.player.hitbox) and blast.fade_out > const.FADE_START / 2:
                self.killPlayer()

        for bomb in self.spriteBombs:
            if pygame.sprite.spritecollideany(bomb, self.spriteBombBlasts, collided = None):
                bomb.expiditeExplosion()
            if bomb.exploded:
                if self.soundOn:
                    self.explodeSound.play()
                powerups, blasts = self.level.destroyWalls(bomb.x, bomb.y, self.level, self.player.bombRange)
                self.spritePowerups.add(powerups)
                self.spriteBombBlasts.add(blasts)
                self.level, self.player = bomb.explode(self.level, self.player)
                bomb.kill()

        for powerup in self.spritePowerups:
            if powerup.rect.colliderect(self.player.hitbox):
                self.player.getPowerup(powerup)
                self.player.increaseScore(const.PICK_UP_POWER_UP)
                powerup.kill()

        #Frame Per Section update
        currentFPS = int(self.clock.get_fps())
        if currentFPS >= 50:
            fpsColor = const.GREEN
        elif currentFPS >= 40:
            fpsColor = const.YELLOW
        else:
            fpsColor = const.RED
        text1 = str(currentFPS)
        fps = self.font.render(text1, True, fpsColor)
        self.screen.blit(fps, (self.screenWidth - 25, 5))


    def drawStatusBar(self):
        self.statusBar.getIconSpriteGroup().draw(self.screen)

        textY = const.ICON_Y + 12
        textXOffset = const.ICON_SCALE
        
        #Text for Player Lives Count, active bombs, boot powerup, bomb range, bomb count, and score
        self.drawText('x'+str(self.player.lives), self.statusBar.getIconX(0) + textXOffset, textY, const.YELLOW)
        #self.drawText('x'+ str(self.player.activeBombs), self.statusBar.getIconX(1) + textXOffset, textY, const.YELLOW)
        self.drawText('x' + str(int(self.player.boot)), self.statusBar.getIconX(2) + textXOffset, textY, const.YELLOW)
        self.drawText('x'+ str(self.player.bombRange), self.statusBar.getIconX(3) + textXOffset, textY, const.YELLOW)
        self.drawText('x'+ str(self.player.bombCount), self.statusBar.getIconX(4) + textXOffset, textY, const.YELLOW)
        self.drawText('Score: '+str(self.player.score), const.SCORE_X, textY, const.YELLOW)


    def drawText(self, text, x, y, color):
        textSurface = self.font.render(text, True, color)
        self.screen.blit(textSurface, (x, y))


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

        #stateFunction = self.states[self.gameState]
        #self.gameState = stateFunction()
        self.gameState = self.states[self.gameState]()
        self.updateScreen()

        #must make sure game finishes cycles before quitting
        if self.gameState == const.GAME_STATE_QUITTING:
            self.quitGame()


    def stateGameRunning(self):
            self.render()
            self.checkPlayerProgress()
            newState = self.gameState
            if self.player.state == const.STATE_DEAD:
                self.screenImage.blit(self.screen, (0,0), ((0,0), self.screenSize))    #take a snapshot of the screen
                newState = const.GAME_STATE_PLAYER_DEAD
                self.start_ticks = pygame.time.get_ticks() #starter tick

            return newState


    def statePlayerDead(self):
        #display death screen when player dies, then reset level
        self.screen.blit(self.screenImage, (0,0))
        if not self.gameOver:#self.player.lives > 0:
            self.screen.blit(self.death_test_image, self.death_test_rect)
        else:
            self.screen.blit(self.gameOverImage, self.death_test_rect)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
        newState = self.gameState
        if seconds > const.PLAYER_DEATH_SCREEN_TIMER:
            newState = self.resetLevel()

        return newState


    def stateMainMenu(self):
        newState = self.theMainMenu.showMenu()
        if newState == const.GAME_STATE_RUNNING:
            self.levelNum = 1
            newState = self.resetLevel()

        return newState


    def stateHighScores(self):
        newState = self.highScores.display()
        return newState


    def stateQuitting(self):
        return const.GAME_STATE_QUITTING




    def resetLevel(self):
        for enemy in self.spriteEnemies:
            enemy.kill()
        for bomb in self.spriteBombs:
            bomb.kill()
        for blast in self.spriteBombBlasts:
            blast.kill()
        for powerup in self.spritePowerups:
            powerup.kill()

        self.spritePlayer.empty()
        self.spriteEnemies.empty()
        self.spriteBombs.empty()
        self.spriteBombBlasts.empty()
        
        tempPlayer = self.player
        self.level, self.player, self.enemies, self.boss = Level.startNewLevel(self.levelNum)
        if self.exitingToMenu:
            self.exitingToMenu = False
            newState = const.GAME_STATE_MENU
        elif self.gameOver:
            self.gameOver = False
            print(self.player.score)
            self.updateScore(tempPlayer.score)
            newState = const.GAME_STATE_HIGHSCORES
        else:
            self.player.lives = tempPlayer.lives
            self.player.increaseScore(tempPlayer.score)
            if tempPlayer.state == const.STATE_DEAD:        #player keeps powerups when going to next level, but not if player dies
                #self.player.increaseScore(const.PLAYER_DIED)
                pass
            elif self.gameState == const.GAME_STATE_MENU:
                self.player.lives = const.LIVES
                self.player.score = 0
            else:
                self.player.bombCount = tempPlayer.bombCount
                self.player.bombRange = tempPlayer.bombRange
                self.player.boot = tempPlayer.boot
            self.spritePlayer.add(self.player)
            self.player.state = const.STATE_IDLE
            self.spriteEnemies.add(self.enemies)
            if self.boss:
                self.spriteEnemies.add(self.boss)
                musicFile = str(Path.cwd() / "sounds" / "musicBoss.mp3")
                pygame.mixer.music.load(musicFile)
            else:
                musicFile = str(Path.cwd() / "sounds" / "music1.mp3")
                pygame.mixer.music.load(musicFile)
            newState = const.GAME_STATE_RUNNING
        tempPlayer.kill()
        return newState


    def killPlayer(self):
        self.player.increaseScore(const.PLAYER_DIED)
        self.player.state = const.STATE_DEAD
        if self.player.lives == 0:
            self.gameOver = True
        else:
            self.player.lives -= 1
            
        if self.soundOn:
            self.deathSound.play()

    
    def checkPlayerProgress(self):
        if self.level.layout[self.player.y][self.player.x] == const.TILE_DOOR_OPENED and self.player.state == const.STATE_IDLE:
            self.player.increaseScore(const.LEVEL_CHANGE)

            if self.levelNum < self.numLevels:
                self.levelNum += 1
                self.gameState = self.resetLevel()

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
                newBomb = self.player.dropBomb(self.level)
                if newBomb:
                    self.level.layout[newBomb.y][newBomb.x] = newBomb
                    self.spriteBombs.add(newBomb)


    #Event-driven input
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitingToMenu = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameState = const.GAME_STATE_MENU
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


    def updateScore(self,score):
        self.highScores.newScore(score)
    

    def quitGame(self):
        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit()
        self.gameRunning = False


    #TODO  remove before release
    def debug_mode(self, event):
        if event.key == pygame.K_z:     #testing code for door
            self.killPlayer()
        elif event.key == pygame.K_x:   #reduce lives to 0 for quick testing of highscore
            self.player.lives = 0
        elif event.key == pygame.K_k:   #kill all enemies on screen
            for enemy in self.spriteEnemies:
                enemy.kill()
        elif event.key == pygame.K_COMMA:
            if self.levelNum > 1:
                self.levelNum -= 1
                self.gameState = self.resetLevel()
        elif event.key == pygame.K_PERIOD:
            if self.levelNum < self.numLevels:
                self.levelNum += 1
                self.gameState = self.resetLevel()
        elif event.key == pygame.K_LSHIFT:
            if self.player.state == const.STATE_IDLE:
                powerups, blasts = self.level.destroyWalls(self.player.x, self.player.y, self.level, self.player.bombRange)     #TODO powerups sprite group, add to
                self.spritePowerups.add(powerups)
        elif event.key == pygame.K_q:
            self.player.bombCount = 5
            self.player.bombRange = 3
