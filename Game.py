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


def checkNumeric(value):
    if not isinstance(value, int) and not isinstance(value, float):
        raise RuntimeError('Error: ' + str(value) + ' is not a number')
    return value


def checkPositive(value):
    if isinstance(value, int) and not value > 0:
        raise RuntimeError('Error: '  + str(value) + ' is not a positive number')
    return value


class Game(object):

    '''
    This is the game object.  It manages the various states of the game while running.
    '''
    def __init__(self):

        #Game states, tells the game what code to run depending on the current state
        self.__states = {const.GAME_STATE_MENU : self.stateMainMenu,
          const.GAME_STATE_RUNNING           : self.stateGameRunning,
          const.GAME_STATE_PLAYER_DEAD       : self.statePlayerDead,
          const.GAME_STATE_PLAYER_WINS       : self.statePlayerWins,
          const.GAME_STATE_QUITTING          : self.stateQuitting,
          const.GAME_STATE_HIGHSCORES        : self.stateHighScores}

        #Initialize pygame
        pygame.init()

        #Setup music and sound
        self.musicFile = str(Path.cwd() / "sounds" / "music1.mp3")
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(self.musicFile)

        self.explodeSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "bomb.wav"))
        self.deathSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "yell.wav"))
        self.bossDieSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "boss_no.wav"))

        #Setup misc pygame settings such as clock for timers and font for text
        self.__clock = pygame.time.Clock()
        self.start_ticks = 0.0
        self.font = pygame.font.Font(None, const.FONT_SIZE)

        #Setup game progression booleans
        self.gameRunning = True
        self.gameOver = False
        self.playerWins = False
        self.exitingToMenu = False
        self.musicOn = True
        self.soundOn = True

        #Makes game start in main menu
        self.gameState = const.GAME_STATE_MENU

        #Setup screen parameters and the pygame window
        self.__screenWidth = const.MAP_WIDTH * const.TILE_SIZE + const.SCREEN_OFFSET_X_LEFT + const.SCREEN_OFFSET_X_RIGHT
        self.__screenHeight = const.MAP_HEIGHT * const.TILE_SIZE + const.SCREEN_OFFSET_Y_TOP + const.SCREEN_OFFSET_Y_BOTTOM
        self.__screenSize = self.__screenWidth, self.__screenHeight
        self.__screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("BomberDude")
        self.screenImage = pygame.Surface(self.screenSize)    #used to store the screen to an image, useful for semi-transparent screens 

        #Setup the MainMenu and High scores Screen
        self.theMainMenu = MainMenu.MainMenu(self.screen, self.__screenWidth, self.__screenHeight)
        self.highScores = HighScore.HighScore(self.screen, self.__screenWidth, self.__screenHeight)

        #Load starting level
        self.levelNum = 1
        self.level, self.player, self.enemies, self.boss = Level.startNewLevel(self.levelNum)

        #Retreive total number of levels stored in data directory, requires levels to be numbered sequentially
        self.numLevels = 0
        dataDir = Path.cwd() / "data"
        for f in dataDir.glob("level*.csv"):
            self.numLevels += 1

        #Create sprite groups for all game sprite objects
        self.spritePlayer = pygame.sprite.Group()
        self.spritePlayer.add(self.player)
        self.spriteEnemies = pygame.sprite.Group()
        self.spriteEnemies.add(self.enemies)
        self.spriteBombs = pygame.sprite.Group()
        self.spriteBombBlasts = pygame.sprite.Group()
        self.spriteBossBombBlasts = pygame.sprite.Group()
        self.spritePowerups = pygame.sprite.Group()

        #Create status bar for displaying player information at top of screen
        self.statusBar = StatusBar.StatusBar(0, 0)
        self.statusBar.addIcon("Down.png", 0, True)
        self.statusBar.addIcon("powerup_boot.png", 2, False, const.ICON_SCALE + 5)  #This is offset because the graphic is a little smaller than the icons
        self.statusBar.addIcon("powerup_range.png", 3, False)
        self.statusBar.addIcon("powerup_count.png", 4, False)

        #Player death screen
        imageFile = str(Path.cwd() / "graphics" / "death_screen.png")
        self.deathScreen = pygame.image.load(imageFile).convert_alpha()
        self.smallScreenRect = self.deathScreen.get_rect()
        self.smallScreenRect.x = int(self.__screenWidth / 2 - self.smallScreenRect.width / 2)
        self.smallScreenRect.y = int(self.__screenHeight / 2 - self.smallScreenRect.height / 2)

        #Game over screen image
        imageFile = str(Path.cwd() / "graphics" / "game_over_screen.png")    
        self.gameOverImage = pygame.image.load(imageFile).convert_alpha()

        #Player win screen image
        imageFile = str(Path.cwd() / "graphics" / "you_win_screen.png")
        self.playerWinsImage = pygame.image.load(imageFile).convert_alpha()

        #Screen border image
        imageFile = str(Path.cwd() / "graphics" / "border.png")
        self.borderImage = pygame.image.load(imageFile).convert()

        #Debug mode allows cheats, only for developer use
        self.__debugMode = True


    @property
    def musicFile(self):
        ''' Accessor. '''
        return self.__musicFile

    @musicFile.setter
    def musicFile(self, musicFile):
        '''Sets the file for the current music'''
        if not isinstance(musicFile, str) or (".mp3" not in(musicFile)):
            raise RuntimeError(str(musicFile) + ' is not a properly formatted filename.')
        self.__musicFile = musicFile


    @property
    def explodeSound(self):
        ''' Accessor. '''
        return self.__explodeSound

    @explodeSound.setter
    def explodeSound(self, explodeSound):
        '''Sets the sound for bomb explosions'''
        if not isinstance(explodeSound, pygame.mixer.SoundType):
            raise RuntimeError(str(explodeSound) + ' is not a sound file.')
        self.__explodeSound = explodeSound


    @property
    def deathSound(self):
        ''' Accessor. '''
        return self.__deathSound

    @deathSound.setter
    def deathSound(self, deathSound):
        '''Sets the sound for player death'''
        if not isinstance(deathSound, pygame.mixer.SoundType):
            raise RuntimeError(str(deathSound) + ' is not a sound file.')
        self.__deathSound = deathSound


    @property
    def bossDieSound(self):
        ''' Accessor. '''
        return self.__bossDieSound

    @bossDieSound.setter
    def bossDieSound(self, bossDieSound):
        '''Sets the sound for boss death'''
        if not isinstance(bossDieSound, pygame.mixer.SoundType):
            raise RuntimeError(str(bossDieSound) + ' is not a sound file.')
        self.__bossDieSound = bossDieSound


    @property
    def start_ticks(self):
        ''' Accessor. '''
        return self.__start_ticks

    @start_ticks.setter
    def start_ticks(self, start_ticks):
        '''Sets the ticks counter starting point for timers'''
        if not isinstance(start_ticks, int) and not isinstance(start_ticks, float):
            raise RuntimeError(str(start_ticks) + ' is not valid value for start_ticks.  Must be a number.')
        self.__start_ticks = start_ticks


    @property
    def font(self):
        ''' Accessor. '''
        return self.__font

    @font.setter
    def font(self, font):
        '''Sets the ticks counter starting point for timers'''
        if not isinstance(font, pygame.font.FontType):
            raise RuntimeError(str(font) + ' is not valid font.')
        self.__font = font


    @property
    def gameRunning(self):
        ''' Accessor. '''
        return self.__gameRunning

    @gameRunning.setter
    def gameRunning(self, gameRunning):
        '''Sets the boolean for gameRunning'''
        if not isinstance(gameRunning, bool):
            raise RuntimeError(str(gameRunning) + ' is not a boolean.')
        self.__gameRunning = gameRunning


    @property
    def gameOver(self):
        ''' Accessor. '''
        return self.__gameOver

    @gameOver.setter
    def gameOver(self, gameOver):
        '''Sets the boolean for gameOver'''
        if not isinstance(gameOver, bool):
            raise RuntimeError(str(gameOver) + ' is not a boolean.')
        self.__gameOver = gameOver


    @property
    def playerWins(self):
        ''' Accessor. '''
        return self.__playerWins

    @playerWins.setter
    def playerWins(self, playerWins):
        '''Sets the boolean for playerWins'''
        if not isinstance(playerWins, bool):
            raise RuntimeError(str(playerWins) + ' is not a boolean.')
        self.__playerWins = playerWins


    @property
    def exitingToMenu(self):
        ''' Accessor. '''
        return self.__exitingToMenu

    @exitingToMenu.setter
    def exitingToMenu(self, exitingToMenu):
        '''Sets the boolean for exitingToMenu'''
        if not isinstance(exitingToMenu, bool):
            raise RuntimeError(str(exitingToMenu) + ' is not a boolean.')
        self.__exitingToMenu = exitingToMenu


    @property
    def musicOn(self):
        ''' Accessor. '''
        return self.__musicOn

    @musicOn.setter
    def musicOn(self, musicOn):
        '''Sets the boolean for musicOn'''
        if not isinstance(musicOn, bool):
            raise RuntimeError(str(musicOn) + ' is not a boolean.')
        self.__musicOn = musicOn


    @property
    def soundOn(self):
        ''' Accessor. '''
        return self.__soundOn

    @soundOn.setter
    def soundOn(self, soundOn):
        '''Sets the boolean for soundOn'''
        if not isinstance(soundOn, bool):
            raise RuntimeError(str(soundOn) + ' is not a boolean.')
        self.__soundOn = soundOn


    @property
    def gameState(self):
        ''' Accessor. '''
        return self.__gameState

    @gameState.setter
    def gameState(self, gameState):
        '''Sets the boolean for soundOn'''
        if gameState not in ([const.GAME_STATE_HIGHSCORES, const.GAME_STATE_MENU, const.GAME_STATE_PLAYER_DEAD,
        const.GAME_STATE_PLAYER_WINS, const.GAME_STATE_QUITTING, const.GAME_STATE_RUNNING]):
            raise RuntimeError(str(gameState) + ' is not a valid value for gameState.')
        self.__gameState = gameState


    @property
    def screenSize(self):
        ''' Accessor. '''
        return self.__screenSize

    #no screenSize.setter



    @property
    def screen(self):
        ''' Accessor. '''
        return self.__screen

    #no screen.setter


    @property
    def screenImage(self):
        ''' Accessor. '''
        return self.__screenImage

    @screenImage.setter
    def screenImage(self, screenImage):
        '''Sets the screen image, used for capturing the screen. Allows only a pygame surface'''
        if not isinstance(screenImage, pygame.SurfaceType):
            raise RuntimeError(str(screenImage) + ' is not a valid pygame image.')
        self.__screenImage = screenImage


    @property
    def theMainMenu(self):
        ''' Accessor. '''
        return self.__theMainMenu

    @theMainMenu.setter
    def theMainMenu(self, theMainMenu):
        '''Sets the main menu object'''
        if not isinstance(theMainMenu, MainMenu.MainMenu):
            raise RuntimeError(str(theMainMenu) + ' is not a valid MainMenu object type.')
        self.__theMainMenu = theMainMenu

    
    @property
    def highScores(self):
        ''' Accessor. '''
        return self.__highScores

    @highScores.setter
    def highScores(self, highScores):
        '''Sets the high score menu object'''
        if not isinstance(highScores, HighScore.HighScore):
            raise RuntimeError(str(highScores) + ' is not a valid HighScore object type.')
        self.__highScores = highScores


    @property
    def levelNum(self):
        ''' Accessor. '''
        return self.__levelNum

    @levelNum.setter
    def levelNum(self, levelNum):
        '''Sets the current level number'''
        checkNumeric(levelNum)
        checkPositive(levelNum)
        self.__levelNum = levelNum


    @property
    def level(self):
        ''' Accessor. '''
        return self.__level

    @level.setter
    def level(self, level):
        '''Sets the level object'''
        if not isinstance(level, Level.Level):
            raise RuntimeError(str(level) + ' is not a valid Level object type.')
        self.__level = level


    @property
    def player(self):
        ''' Accessor. '''
        return self.__player

    @player.setter
    def player(self, player):
        '''Sets the player object'''
        if not isinstance(player, Character.PlayerCharacter):
            raise RuntimeError(str(player) + ' is not a valid PlayerCharacter object type.')
        self.__player = player


    @property
    def enemies(self):
        ''' Accessor. '''
        return self.__enemies

    @enemies.setter
    def enemies(self, enemies):
        '''Sets the list of enemies objects'''
        if not isinstance(enemies, list):
            raise RuntimeError(str(enemies) + ' is not a valid Python list.')
        else:
            for i in range(len(enemies)):
                if not isinstance(enemies[i], Character.Enemy):
                    raise RuntimeError(str(enemies[i]) + ' is not a valid Enemy object type.')
        self.__enemies = enemies


    @property
    def boss(self):
        ''' Accessor. '''
        return self.__boss

    @boss.setter
    def boss(self, boss):
        '''Sets the boss object'''
        if boss and not isinstance(boss, Character.Boss):
            raise RuntimeError(str(boss) + ' is not a valid Boss object type.')
        self.__boss = boss


    @property
    def numLevels(self):
        ''' Accessor. '''
        return self.__numLevels

    @numLevels.setter
    def numLevels(self, numLevels):
        '''Sets the total number of levels in the game'''
        checkNumeric(numLevels)
        if numLevels != 0:
            checkPositive(numLevels)
        self.__numLevels = numLevels


    @property
    def spritePlayer(self):
        ''' Accessor. '''
        return self.__spritePlayer

    @spritePlayer.setter
    def spritePlayer(self, spritePlayer):
        '''Sets the sprite group for the player sprite'''
        if not isinstance(spritePlayer, pygame.sprite.Group):
            raise RuntimeError(str(spritePlayer) + ' is not a valid pygame sprite group.')
        self.__spritePlayer = spritePlayer


    @property
    def spriteEnemies(self):
        ''' Accessor. '''
        return self.__spriteEnemies

    @spriteEnemies.setter
    def spriteEnemies(self, spriteEnemies):
        '''Sets the sprite group for the enemy sprites'''
        if not isinstance(spriteEnemies, pygame.sprite.Group):
            raise RuntimeError(str(spriteEnemies) + ' is not a valid pygame sprite group.')
        self.__spriteEnemies = spriteEnemies


    @property
    def spriteBombs(self):
        ''' Accessor. '''
        return self.__spriteBombs

    @spriteBombs.setter
    def spriteBombs(self, spriteBombs):
        '''Sets the sprite group for the bomb sprites'''
        if not isinstance(spriteBombs, pygame.sprite.Group):
            raise RuntimeError(str(spriteBombs) + ' is not a valid pygame sprite group.')
        self.__spriteBombs = spriteBombs


    @property
    def spriteBombBlasts(self):
        ''' Accessor. '''
        return self.__spriteBombBlasts

    @spriteBombBlasts.setter
    def spriteBombBlasts(self, spriteBombBlasts):
        '''Sets the sprite group for the bomb blasts sprites'''
        if not isinstance(spriteBombBlasts, pygame.sprite.Group):
            raise RuntimeError(str(spriteBombBlasts) + ' is not a valid pygame sprite group.')
        self.__spriteBombBlasts = spriteBombBlasts


    @property
    def spriteBossBombBlasts(self):
        ''' Accessor. '''
        return self.__spriteBossBombBlasts

    @spriteBossBombBlasts.setter
    def spriteBossBombBlasts(self, spriteBossBombBlasts):
        '''Sets the sprite group for the boss bomb blasts sprites'''
        if not isinstance(spriteBossBombBlasts, pygame.sprite.Group):
            raise RuntimeError(str(spriteBossBombBlasts) + ' is not a valid pygame sprite group.')
        self.__spriteBossBombBlasts = spriteBossBombBlasts


    @property
    def spritePowerups(self):
        ''' Accessor. '''
        return self.__spritePowerups

    @spritePowerups.setter
    def spritePowerups(self, spritePowerups):
        '''Sets the sprite group for the powerups sprites'''
        if not isinstance(spritePowerups, pygame.sprite.Group):
            raise RuntimeError(str(spritePowerups) + ' is not a valid pygame sprite group.')
        self.__spritePowerups = spritePowerups


    @property
    def statusBar(self):
        ''' Accessor. '''
        return self.__statusBar

    @statusBar.setter
    def statusBar(self, statusBar):
        '''Sets the status bar object'''
        if statusBar and not isinstance(statusBar, StatusBar.StatusBar):
            raise RuntimeError(str(statusBar) + ' is not a valid StatusBar object type.')
        self.__statusBar = statusBar


    @property
    def deathScreen(self):
        ''' Accessor. '''
        return self.__deathScreen

    @deathScreen.setter
    def deathScreen(self, deathScreen):
        '''Sets the death screen image. Allows only a pygame surface'''
        if not isinstance(deathScreen, pygame.SurfaceType):
            raise RuntimeError(str(deathScreen) + ' is not a valid pygame image.')
        self.__deathScreen = deathScreen


    @property
    def smallScreenRect(self):
        ''' Accessor. '''
        return self.__smallScreenRect

    @smallScreenRect.setter
    def smallScreenRect(self, smallScreenRect):
        '''Sets the death screen rectangle, used for holding x and y coords of death/gameover/win screens. Allows only a pygame Rect'''
        if not isinstance(smallScreenRect, pygame.Rect):
            raise RuntimeError(str(smallScreenRect) + ' is not a valid pygame Rect.')
        self.__smallScreenRect = smallScreenRect


    @property
    def gameOverImage(self):
        ''' Accessor. '''
        return self.__gameOverImage

    @gameOverImage.setter
    def gameOverImage(self, gameOverImage):
        '''Sets the game over screen image. Allows only a pygame surface'''
        if not isinstance(gameOverImage, pygame.SurfaceType):
            raise RuntimeError(str(gameOverImage) + ' is not a valid pygame image.')
        self.__gameOverImage = gameOverImage


    @property
    def playerWinsImage(self):
        ''' Accessor. '''
        return self.__playerWinsImage

    @playerWinsImage.setter
    def playerWinsImage(self, playerWinsImage):
        '''Sets the player wins screen image. Allows only a pygame surface'''
        if not isinstance(playerWinsImage, pygame.SurfaceType):
            raise RuntimeError(str(playerWinsImage) + ' is not a valid pygame image.')
        self.__playerWinsImage = playerWinsImage


    @property
    def borderImage(self):
        ''' Accessor. '''
        return self.__borderImage

    @borderImage.setter
    def borderImage(self, borderImage):
        '''Sets the screen border image. Allows only a pygame surface'''
        if not isinstance(borderImage, pygame.SurfaceType):
            raise RuntimeError(str(borderImage) + ' is not a valid pygame image.')
        self.__borderImage = borderImage



    def render(self):

        '''
        Handles drawing and updating all spritegroups, to include movement and interaction 
         between spritegroups.  Handles death of enemies and players, bomb explosions, wall
         destruction, and powerup pickups since all are spritegroup-based interation.
        ''' 

        #Render level
        self.screen.blit(self.borderImage, (0, 0))
        self.drawStatusBar()
        self.drawLevel()
        
        #Update and render enemies
        self.spriteEnemies.update(self.level, self.player)
        self.spriteEnemies.draw(self.screen)

        #Update and render bombs, blasts, and powerups
        self.spriteBombs.update(self.level)
        self.spriteBombs.draw(self.screen)

        self.spriteBombBlasts.update()
        self.spriteBombBlasts.draw(self.screen)

        self.spriteBossBombBlasts.update()
        self.spriteBossBombBlasts.draw(self.screen)

        self.spritePowerups.update()
        self.spritePowerups.draw(self.screen)

        #Update and render player
        self.spritePlayer.update(self.level, self.player)
        self.spritePlayer.draw(self.screen)

        #Check collisions between enemies and players (kill player) / bomb blasts (kill enemy)
        for enemy in self.spriteEnemies:
            if enemy.rect.colliderect(self.player.hitbox) and enemy.state != const.STATE_DYING:
                if pygame.sprite.spritecollide(enemy, self.spritePlayer, False, pygame.sprite.collide_mask):
                    self.killPlayer()
            if pygame.sprite.spritecollide(enemy, self.spriteBombBlasts, False, pygame.sprite.collide_mask):
                if enemy.kind == const.BOSS:
                    if enemy.takeDamage():
                      self.player.increaseScore(const.ENEMY_DIED)
                      if self.soundOn:
                          self.bossDieSound.play()
                else:
                    enemy.destroy()
                    self.player.increaseScore(const.ENEMY_DIED)

        #Check if any enemies left, open door if all enemies gone
        if not self.spriteEnemies:
            self.level.openDoor()

        #Kill player if hit by bomb blast
        for blast in self.spriteBombBlasts:
            if blast.rect.colliderect(self.player.hitbox) and blast.fade_out > const.FADE_START / 2:
                self.killPlayer()

        for blast in self.spriteBossBombBlasts:
            if blast.rect.colliderect(self.player.hitbox) and blast.fade_out > const.FADE_START / 2:
                self.killPlayer()

        #Handle bomb collision with enemies or other bombs when kicked, and handle bomb explosions
        for bomb in self.spriteBombs:
            for enemy in self.spriteEnemies:
                if bomb.state == const.STATE_MOVING_UP and bomb.y == enemy.y +1 and bomb.x == enemy.x:
                    bomb.collision = True
                if bomb.state == const.STATE_MOVING_DOWN and bomb.y == enemy.y - 1 and bomb.x == enemy.x:
                    bomb.collision = True
                if bomb.state == const.STATE_MOVING_LEFT and bomb.y == enemy.y and bomb.x == enemy.x + 1:
                    bomb.collision = True
                if bomb.state == const.STATE_MOVING_RIGHT and bomb.y == enemy.y and bomb.x == enemy.x - 1:
                    bomb.collision = True
            if pygame.sprite.spritecollideany(bomb, self.spriteBombBlasts, collided = None) or pygame.sprite.spritecollideany(bomb, self.spriteBossBombBlasts, collided = None):
                bomb.expiditeExplosion()
            if bomb.exploded:
                if self.soundOn:
                    self.explodeSound.play()
                if not bomb.bossBomb:
                    powerups, blasts = self.level.destroyWalls(bomb.x, bomb.y, bomb.range)
                    self.spritePowerups.add(powerups)
                    self.spriteBombBlasts.add(blasts)
                    self.level, self.player = bomb.explode(self.level, self.player)
                else:
                    powerups, blasts = self.level.destroyWalls(bomb.x, bomb.y, bomb.range)
                    self.spriteBossBombBlasts.add(blasts)
                    self.level, self.boss = bomb.explode(self.level, self.boss)
                bomb.kill()

        #Handle player collision with powerup (player collects up powerup on collision)
        for powerup in self.spritePowerups:
            if powerup.rect.colliderect(self.player.hitbox):
                self.player.getPowerup(powerup)
                self.player.increaseScore(const.PICK_UP_POWER_UP)
                powerup.kill()


    def drawStatusBar(self):

        '''
        Draws the status bar on screen.  The status bar shows player information such as
         lives, powerups held, and score.
        ''' 

        self.statusBar.getIconSpriteGroup().draw(self.screen)

        textY = const.ICON_Y + const.ICON_TEXT_Y_OFFSET
        textXOffset = const.ICON_SCALE
        
        #Text for Player Lives Count, active bombs, boot powerup, bomb range, bomb count, and score
        self.drawText('x'+str(self.player.lives), self.statusBar.getIconX(0) + textXOffset, textY, const.YELLOW)
        self.drawText('x' + str(int(self.player.boot)), self.statusBar.getIconX(2) + textXOffset, textY, const.YELLOW)
        self.drawText('x'+ str(self.player.bombRange), self.statusBar.getIconX(3) + textXOffset, textY, const.YELLOW)
        self.drawText('x'+ str(self.player.bombCount), self.statusBar.getIconX(4) + textXOffset, textY, const.YELLOW)
        self.drawText('Score: '+str(self.player.score), const.SCORE_X, textY, const.YELLOW)


    def drawText(self, text, x, y, color):

        '''
        Draws text to the screen
        -text, contains the text to display on screen
        -x, x location where to draw text
        -y, y location where to draw text
        -color, color to use when drawing text
        ''' 
        
        textSurface = self.font.render(text, True, color)
        self.screen.blit(textSurface, (x, y))

    
    def drawLevel(self):

        '''
        Draws all of the tiles onscreen from the current level, to include background, walls,
         breakable walls, and the door
        ''' 

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
                except RuntimeError:
                    print("Index out of range error in level.layout")


    def drawTile(self, image, x, y):

        '''
        Converts the x and y value of each tile based on its location in
         the map grid into x and y coordinates on screen.
        -image, contains the image for the tile being drawn on screen
        -x, the x value based on the tile's index location in the map
        -y, the y value based on the tile's index location in the map
        ''' 

        xres = const.SCREEN_OFFSET_X_LEFT + x * const.TILE_SIZE
        yres = const.SCREEN_OFFSET_Y_TOP + y * const.TILE_SIZE
        self.screen.blit(image, (xres, yres))


    def updateBoss(self):
        
        '''
        Tells the boss to drop and kick a bomb down the screen when ready.
        ''' 

        if self.boss.readyDropBomb:
            newBomb = self.boss.dropBomb(self.level)
            if newBomb:
                self.level.layout[newBomb.y][newBomb.x] = newBomb
                self.spriteBombs.add(newBomb)
                newBomb.kick(const.DOWN, self.level)
    

    def update(self):

        '''
        Updates the state of the game, handles state transitions, 
         and updates the screen.
        ''' 

        #Keeps the music playing if it is turned on.
        if self.musicOn:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        if self.level.bossLevel:
            self.updateBoss()

        #Get user input from the player
        self.getUserInput()

        #Handles switching game states by calling gamestate fucntions from a dictionary
        self.gameState = self.__states[self.gameState]()

        #Update the screen
        pygame.display.update()
        self.screen.fill(colors.Black)
        self.__clock.tick(const.FRAMERATE)

        #Make sure game finishes cycles before quitting
        if self.exitingToMenu:
            self.exitingToMenu = False
            self.gameState = const.GAME_STATE_MENU
        if self.gameState == const.GAME_STATE_QUITTING:
            self.quitGame()


    def stateGameRunning(self):

        '''
        Game state for when the game is being played.
        ''' 

        self.render()
        newState = self.checkPlayerProgress()

        return newState


    def statePlayerDead(self):

        '''
        Game state for when the player dies.  Shows the death screen for a
         period of time, and the resets the level.
        ''' 

        self.screen.blit(self.screenImage, (0,0))
        if not self.gameOver:
            self.screen.blit(self.deathScreen, self.smallScreenRect)
        else:
            self.screen.blit(self.gameOverImage, self.smallScreenRect)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
        newState = self.gameState
        if seconds > const.PLAYER_DEATH_SCREEN_TIMER:
            newState = self.resetLevel()

        return newState


    def statePlayerWins(self):

        '''
        Game state for when the player wins the game.  Displays the win screen
         for a period of time, and then goes to the high schore.
        ''' 

        self.screen.blit(self.screenImage, (0,0))
        self.screen.blit(self.playerWinsImage, self.smallScreenRect)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
        newState = self.gameState
        if seconds > const.PLAYER_DEATH_SCREEN_TIMER:
            newState = const.GAME_STATE_HIGHSCORES
            self.highScores.newScore(self.player.score)

        return newState


    def stateMainMenu(self):

        '''
        Game state for when the user is at the main menu.
        ''' 

        if self.musicOn and self.musicFile != str(Path.cwd() / "sounds" / "musicMainMenu.mp3"):
            self.musicFile = str(Path.cwd() / "sounds" / "musicMainMenu.mp3")
            pygame.mixer.music.load(self.musicFile)
            pygame.mixer.music.play()

        newState = self.theMainMenu.showMenu(self.musicOn)
        if newState == const.GAME_STATE_RUNNING:
            self.levelNum = 1
            newState = self.resetLevel()

        return newState


    def stateHighScores(self):

        '''
        Game state for when the user is in the high score screen.
        ''' 

        newState = self.highScores.display()
        return newState


    def stateQuitting(self):

        '''
        Game state for when user chooses to quit the game.
        ''' 

        return const.GAME_STATE_QUITTING


    def resetLevel(self):

        '''
        Handles resetting a level, to include wiping out all spritegroups and
         loading a level.
        ''' 

        #Destroy all sprites in each spritegroup
        for enemy in self.spriteEnemies:
            enemy.kill()
        for bomb in self.spriteBombs:
            bomb.kill()
        for blast in self.spriteBombBlasts:
            blast.kill()
        for blast in self.spriteBossBombBlasts:
            blast.kill()
        for powerup in self.spritePowerups:
            powerup.kill()

        #Clear out each sprite group
        self.spritePlayer.empty()
        self.spriteEnemies.empty()
        self.spriteBombs.empty()
        self.spriteBombBlasts.empty()
        self.spriteBossBombBlasts.empty()
        
        #Since the player is initialized in the level class, backup the parameters that we want to keep by copying player to temp variable
        tempPlayer = self.player
        self.level, self.player, self.enemies, self.boss = Level.startNewLevel(self.levelNum)
        if self.gameOver:
            self.gameOver = False
            self.highScores.newScore(tempPlayer.score)
            newState = const.GAME_STATE_HIGHSCORES
        else:
            self.player.lives = tempPlayer.lives
            self.player.increaseScore(tempPlayer.score)

            #player keeps powerups when going to next level, but not if player dies or exits to main menu
            if self.gameState == const.GAME_STATE_MENU:
                self.player.lives = const.LIVES
                self.player.score = 0
            elif tempPlayer.state != const.STATE_DEAD:
                self.player.bombCount = tempPlayer.bombCount
                self.player.bombRange = tempPlayer.bombRange
                self.player.boot = tempPlayer.boot
            self.spritePlayer.add(self.player)
            self.player.state = const.STATE_IDLE
            self.spriteEnemies.add(self.enemies)
            
            #Determine which music plays depending on if the current level is a boss level.
            if self.boss:
                self.spriteEnemies.add(self.boss)
                if self.musicOn and self.musicFile != str(Path.cwd() / "sounds" / "musicBoss.mp3"):
                    self.musicFile = str(Path.cwd() / "sounds" / "musicBoss.mp3")
                    pygame.mixer.music.load(self.musicFile)
            else:
                if self.musicOn and self.musicFile != str(Path.cwd() / "sounds" / "music1.mp3"):
                    self.musicFile = str(Path.cwd() / "sounds" / "music1.mp3")
                    pygame.mixer.music.load(self.musicFile)
            newState = const.GAME_STATE_RUNNING
        
        #Destroy temporary player variable since no longer needed
        tempPlayer.kill()

        return newState


    def killPlayer(self):

        '''
        When player is killed, adjust score accordingly, decrement and determine
         if game is over.
        ''' 

        self.player.increaseScore(const.PLAYER_DIED)
        self.player.state = const.STATE_DEAD
        if self.player.lives == 0:
            self.gameOver = True
        else:
            self.player.lives -= 1

        #Play death sound  
        if self.soundOn:
            self.deathSound.play()

    
    def checkPlayerProgress(self):

        '''
        Handles if player has completed a level, has died, or has won the game.
        ''' 

        #If player has reached the door and it is opened, adjust score accordingly and go to next level
        if self.level.layout[self.player.y][self.player.x] == const.TILE_DOOR_OPENED and self.player.state == const.STATE_IDLE:
            self.player.increaseScore(const.LEVEL_CHANGE)

            if self.levelNum < self.numLevels:
                self.levelNum += 1
                self.gameState = self.resetLevel()

        newState = self.gameState

        #If player died, display death screen briefly
        if self.player.state == const.STATE_DEAD:
            self.screenImage.blit(self.screen, (0,0), ((0,0), self.screenSize))    #take a snapshot of the screen
            newState = const.GAME_STATE_PLAYER_DEAD
            self.start_ticks = pygame.time.get_ticks() #starter tick

        #If player won game, display the winning screen briefly
        if self.player.state == const.STATE_PLAYER_WINS:
            self.screenImage.blit(self.screen, (0,0), ((0,0), self.screenSize))    #take a snapshot of the screen
            newState = const.GAME_STATE_PLAYER_WINS
            self.start_ticks = pygame.time.get_ticks() #starter tick

        return newState


    #User keyboard input, game controls
    def getUserInput(self):

        '''
        Get user input, for game controls / keyboard button presses
        ''' 

        #Get non-gameplay inputs
        self.getEvents()

        #Controls for movement and dropping bombs
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


    def getEvents(self):

        '''
        Event-driven input.  Handles things such as pressing escape to quit
         the game, 'f' to switch to fullscreen, and 'm'/'s' to toggle music
         and sound.
        ''' 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitingToMenu = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exitingToMenu = True
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
                
                #If debug mode is on, call the debug mode inputs for 'cheats'
                if self.__debugMode:
                    self.debug_mode(event)
    

    def quitGame(self):

        '''
        Handles gracefully quitting the game.  Turns off music and display before quitting.
        ''' 

        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit()
        self.gameRunning = False


    def debug_mode(self, event):

        '''
        Debug mode is for the developer only, not for the user.  It is used
         to enter 'cheats' for testing gameplay mechanics.
        ''' 

        if event.key == pygame.K_z:     #kills player
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
                powerups, blasts = self.level.destroyWalls(self.player.x, self.player.y, self.player.bombRange)
                self.spritePowerups.add(powerups)
        elif event.key == pygame.K_q:
            self.player.bombCount = const.POWERUP_MAX
            self.player.bombRange = const.POWERUP_MAX
            self.player.boot = True
        elif event.key == pygame.K_b:
            newBomb = self.boss.dropBomb(self.level)
            if newBomb:
                self.level.layout[newBomb.y][newBomb.x] = newBomb
                self.spriteBombs.add(newBomb)
                self.level.layout[newBomb.y][newBomb.x].kick(const.DOWN, self.level)
