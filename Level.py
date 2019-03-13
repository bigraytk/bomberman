# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 13:17:57 2019

@author: 
"""
import constants as const
import Wall
import Character
import Bomb
from pathlib import Path
import pygame
import sys


def openImage(imageFile, convertAlpha = False):
    
    '''
    Verifies an image file is valid

    - imageFile, file location of image to be loaded, in pathlib format
    - convertAlpha, if true, use convert_alpha() instead of convert(), for png files with transparency
    '''

    if imageFile and not imageFile.is_file():
        raise RuntimeError(str(imageFile) + ' is not a valid image file.')

    try:
        if convertAlpha:
            image = pygame.image.load(str(imageFile)).convert_alpha()
        else:
            image = pygame.image.load(str(imageFile)).convert()
        return image
    except IOError:
        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit()
        raise RuntimeError('Error: File ' + str(imageFile) + " does not exist!")


def checkNumeric(value):
    if not isinstance(value, int) and not isinstance(value, float):
        raise RuntimeError('Error: ' + str(value) + ' is not a number')
    return value


def checkPositive(value):
    if isinstance(value, int) and not value > 0:
        raise RuntimeError('Error: '  + str(value) + ' is not a positive number')
    return value



class Level(object):

    '''
    This class holds all required information for a level, to include layout, level
     size parameters, character starting positions, the state of the level door,
     and images for walls, background, and the door
    '''
    
    def __init__(self, levelNum):
        checkNumeric(levelNum)
        checkPositive(levelNum)

        self.layout = []
        self.door = const.TILE_DOOR_HIDDEN
        self.numEnemies = 0
        self.enemyStartPosit = []

        # Set the current working directory, read and write:
        dataDir = Path.cwd() / "data"

        #Open csv level file to create level layout      
        levelFile = dataDir.joinpath("level" + str(levelNum) + ".csv")
        self.layout = self.levelParser(levelFile)
    
    
    @property
    def backgroundImage(self):
        ''' Accessor. '''
        return self.__backgroundImage

    @backgroundImage.setter
    def backgroundImage(self, backgroundImage):
        '''Sets the background tile image. Allows only a pygame surface'''
        if not isinstance(backgroundImage, pygame.SurfaceType):
            raise RuntimeError(str(backgroundImage) + ' is not a valid pygame image.')
        self.__backgroundImage = backgroundImage


    @property
    def wallImage(self):
        ''' Accessor. '''
        return self.__wallImage

    @wallImage.setter
    def wallImage(self, wallImage):
        '''Sets the wall tile image. Allows only a pygame surface'''
        if not isinstance(wallImage, pygame.SurfaceType):
            raise RuntimeError(str(wallImage) + ' is not a valid pygame image.')
        self.__wallImage = wallImage


    @property
    def breakableImage(self):
        ''' Accessor. '''
        return self.__breakableImage

    @breakableImage.setter
    def breakableImage(self, breakableImage):
        '''Sets the breakable wall tile image. Allows only a pygame surface'''
        if not isinstance(breakableImage, pygame.SurfaceType):
            raise RuntimeError(str(breakableImage) + ' is not a valid pygame image.')
        self.__breakableImage = breakableImage


    @property
    def doorOpenedImage(self):
        ''' Accessor. '''
        return self.__doorOpenedImage

    @doorOpenedImage.setter
    def doorOpenedImage(self, doorOpenedImage):
        '''Sets the open door image. Allows only a pygame surface'''
        if not isinstance(doorOpenedImage, pygame.SurfaceType):
            raise RuntimeError(str(doorOpenedImage) + ' is not a valid pygame image.')
        self.__doorOpenedImage = doorOpenedImage


    @property
    def doorClosedImage(self):
        ''' Accessor. '''
        return self.__doorClosedImage

    @doorClosedImage.setter
    def doorClosedImage(self, doorClosedImage):
        '''Sets the closed door image. Allows only a pygame surface'''
        if not isinstance(doorClosedImage, pygame.SurfaceType):
            raise RuntimeError(str(doorClosedImage) + ' is not a valid pygame image.')
        self.__doorClosedImage = doorClosedImage


    @property
    def layout(self):
        ''' Accessor. '''
        return self.__layout

    @layout.setter
    def layout(self, layout):
        ''' Prevents level layout from being assigned None '''
        if layout == None:
            raise RuntimeError('Level layout matrix cannot be None')
        self.__layout = layout


    @property
    def levelWidth(self):
        ''' Accessor. '''
        return self.__levelWidth

    #no levelWidth.setter


    @property
    def levelHeight(self):
        ''' Accessor. '''
        return self.__levelHeight

    #no levelHeight.setter
    

    @property
    def door(self):
        ''' Accessor. '''
        return self.__door

    @door.setter
    def door(self, door):
        '''Sets the value of door, used for showing, opening and closing the door '''
        if door != const.TILE_DOOR_CLOSED and door != const.TILE_DOOR_OPENED and door != const.TILE_DOOR_HIDDEN:
            raise RuntimeError(str(door) + ' is not a valid valid value for door.')
        self.__door = door


    @property
    def playerStartPosit(self):
        ''' Accessor. '''
        return self.__playerStartPosit

    @playerStartPosit.setter
    def playerStartPosit(self, playerStartPosit):
        '''Sets the player starting position '''
        if  not isinstance(playerStartPosit, tuple) or len(playerStartPosit) != 2:
            raise RuntimeError(str(playerStartPosit) + ' is not a valid valid value for player starting position. Must be a tuple containing x and y.')
        elif playerStartPosit[0] < 0 or playerStartPosit[1] < 0:
            raise RuntimeError(str(playerStartPosit) + ' is not a valid valid value for player starting position. Both x and y must be greater than 0.')
        self.__playerStartPosit = playerStartPosit


    @property
    def numEnemies(self):
        ''' Accessor. '''
        return self.__numEnemies

    @numEnemies.setter
    def numEnemies(self, numEnemies):
        '''Sets the number of enemies in a level'''
        if numEnemies and numEnemies < 0:
            raise RuntimeError(str(numEnemies) + ' is not a valid value for number of enemies.  Must be 0 or greater.')
        self.__numEnemies = numEnemies


    @property
    def enemyStartPosit(self):
        ''' Accessor. '''
        return self.__enemyStartPosit

    @enemyStartPosit.setter
    def enemyStartPosit(self, enemyStartPosit):
        ''' Prevents enemy start position list from being assigned None '''
        if enemyStartPosit == None:
            raise RuntimeError('Enemy start position list cannot be None')
        self.__enemyStartPosit = enemyStartPosit


    @property
    def bossLevel(self):
        ''' Accessor. '''
        return self.__bossLevel

    @bossLevel.setter
    def bossLevel(self, bossLevel):
        '''Sets the value of bossLevel, used for determining whether the level is a boss level.  Type is boolean '''
        if bossLevel and not isinstance(bossLevel, bool):
            raise RuntimeError(str(bossLevel) + ' is not a valid valid value for bossLevel.')
        self.__bossLevel = bossLevel


    @property
    def bossStartPosit(self):
        ''' Accessor. '''
        return self.__bossStartPosit

    @bossStartPosit.setter
    def bossStartPosit(self, bossStartPosit):
        '''Sets the player starting position '''
        if bossStartPosit and (not isinstance(bossStartPosit, tuple) or len(bossStartPosit) != 2):
            raise RuntimeError(str(bossStartPosit) + ' is not a valid valid value for boss starting position. Must be a tuple containing x and y.')
        elif bossStartPosit and (bossStartPosit[0] < 0 or bossStartPosit[1] < 0):
            raise RuntimeError(str(bossStartPosit) + ' is not a valid valid value for boss starting position. Both x and y must be greater than 0.')
        self.__bossStartPosit = bossStartPosit


    def levelParser(self, levelFile):

        '''
        Loads a level file, sets appropriate images for level, and returns the layout
        
        - levelFile, file location of level to be loaded, in pathlib format
        '''

        layout = []
        graphicsDir = Path.cwd() / "graphics"
        if levelFile and not levelFile.is_file():
            raise RuntimeError(str(levelFile) + ' is not a valid file.')
        try:
            with levelFile.open() as f:
                levelParams = f.readline().split(",")
                self.__levelWidth = int(levelParams[const.LEVEL_WIDTH])
                self.__levelHeight = int(levelParams[const.LEVEL_HEIGHT])
                self.bossLevel = False
                backgroundNum = int(levelParams[const.LEVEL_BG_GFX])
                wallNum = int(levelParams[const.LEVEL_WALL_GFX])
                breakableNum = int(levelParams[const.LEVEL_BREAK_GFX])
                enemyNum = int(levelParams[const.LEVEL_ENEMY_GFX])
            
                for i in range(self.levelHeight):
                    line = f.readline().split(",")
                    line[-1] = line[-1][0]     #remove "\n" from the last element of each line imported from the csv file
                    layout.append(line)
                for y in range(self.levelHeight):
                    for x in range(self.levelWidth):
                        if layout[y][x] == '':
                            layout[y][x] = None
                        elif layout[y][x] == const.TILE_WALL:
                            layout[y][x] = Wall.Wall(False, 0, x, y)
                        elif layout[y][x] == const.TILE_BREAKABLE:
                            layout[y][x] = Wall.Wall(True, 0, x, y)
                        elif layout[y][x] == const.TILE_DOOR_HIDDEN:
                            layout[y][x] = Wall.Wall(True, 0, x, y, True)
                        elif layout[y][x] == const.TILE_PLAYER_START:
                            layout[y][x] = None
                            self.playerStartPosit = (x, y)
                        elif layout[y][x] == const.TILE_ENEMY_SPAWN:
                            layout[y][x] = None
                            self.numEnemies += 1
                            self.enemyStartPosit.append((x, y))
                        elif layout[y][x] == const.TILE_BOSS_SPAWN:
                            layout[y][x] = None
                            self.bossStartPosit = (x, y)
                            self.bossLevel = True
            f.close()
        except IOError:
            pygame.mixer.music.stop()
            pygame.display.quit()
            pygame.quit()
            raise RuntimeError('Error: File ' + str(levelFile) + " does not exist!")

        backgroundFile = graphicsDir.joinpath("back" + str(backgroundNum) + ".png")
        self.backgroundImage = openImage(backgroundFile)
         
        wallFile = graphicsDir.joinpath("wall" + str(wallNum) + ".png")
        self.wallImage = openImage(wallFile)
         
        breakableFile = graphicsDir.joinpath("break" + str(breakableNum) + ".png")
        self.breakableImage = openImage(breakableFile)

        doorOpenedFile = graphicsDir.joinpath("door_opened.png")
        self.doorOpenedImage = openImage(doorOpenedFile, True)
         
        doorClosedFile = graphicsDir.joinpath("door_closed.png")
        self.doorClosedImage = openImage(doorClosedFile, True)

        self.enemyFile = graphicsDir.joinpath("enemy" + str(enemyNum) + ".png")

        
        return layout


    def showDoor(self):

        '''
        Shows a door where a breakable wall was previously shown, used when the wall hiding the door breaks
        '''

        for y in range(self.levelHeight):
            for x in range(self.levelWidth):
                if isinstance(self.layout[y][x], Wall.Wall) and self.layout[y][x].door:
                    self.layout[y][x] = const.TILE_DOOR_CLOSED
        door = const.TILE_DOOR_CLOSED
        
    
    def openDoor(self):

        '''
        Opens the door of the level
        '''

        for y in range(self.levelHeight):
            for x in range(self.levelWidth):
                if self.layout[y][x] == const.TILE_DOOR_CLOSED:
                    self.layout[y][x] = const.TILE_DOOR_OPENED
        
    
    def destroyWalls(self, x, y, level, blastRange):

        '''Used when a bomb explodes to put blast graphics in all four directions
            returns powerups and blasts so they can be drawn onscreen by the caller 
        - x, x location where blast starts
        - y, y location where blast starts
        - level, used to check level layout so that blasts don't go past walls
        - blastRange, used to limit how far the blasts extend in each direction
        '''

        walls = []
        powerups = []
        hitWallUp = False
        hitWallDown = False
        hitWallLeft = False
        hitWallRight = False

        blasts = []
        blasts.append(Bomb.Blast(x, y, const.CENTER_FLAME, True))
        for i in range(1, blastRange + 1):
            if y - i > 0 and not hitWallUp:
                if isinstance(level.layout[y - i][x], Wall.Wall):
                    walls.append(level.layout[y - i][x])
                    hitWallUp = True
                    if level.layout[y - i][x].breakable:
                        blasts.append(Bomb.Blast(x, y - i, const.UP_FLAME, True))
                if not hitWallUp:
                    if i < blastRange:
                        blasts.append(Bomb.Blast(x, y - i, const.UP_FLAME, False))
                    else:
                        blasts.append(Bomb.Blast(x, y - i, const.UP_FLAME, True))
            
            if y + i < level.levelHeight and not hitWallDown:
                if isinstance(level.layout[y + i][x], Wall.Wall):
                    walls.append(level.layout[y + i][x])
                    hitWallDown = True
                    if level.layout[y + i][x].breakable:
                        blasts.append(Bomb.Blast(x, y + i, const.DOWN_FLAME, True))
                if not hitWallDown:
                    if i < blastRange:
                        blasts.append(Bomb.Blast(x, y + i, const.DOWN_FLAME, False))
                    else:
                        blasts.append(Bomb.Blast(x, y + i, const.DOWN_FLAME, True))
            
            if x - i > 0 and not hitWallLeft:
                if isinstance(level.layout[y][x - i], Wall.Wall):
                    walls.append(level.layout[y][x - i])
                    hitWallLeft = True
                    if level.layout[y][x - i].breakable:
                        blasts.append(Bomb.Blast(x - i, y, const.LEFT_FLAME, True))
                if not hitWallLeft:
                    if i < blastRange:
                        blasts.append(Bomb.Blast(x - i, y, const.LEFT_FLAME, False))
                    else:
                        blasts.append(Bomb.Blast(x - i, y, const.LEFT_FLAME, True))
            
            if x + i < level.levelWidth and not hitWallRight:
                if isinstance(level.layout[y][x + i], Wall.Wall):
                    walls.append(level.layout[y][x + i])
                    hitWallRight = True
                    if level.layout[y][x + i].breakable:
                        blasts.append(Bomb.Blast(x + i, y, const.RIGHT_FLAME, True))
                if not hitWallRight:
                    if i < blastRange:
                        blasts.append(Bomb.Blast(x + i, y, const.RIGHT_FLAME, False))
                    else:
                        blasts.append(Bomb.Blast(x + i, y, const.RIGHT_FLAME, True))
        for theWall in walls:
            result = theWall.destroy(level)
            if result:
                powerups.append(result)
        return powerups, blasts



def startNewLevel(num):

    '''
    Loads level file based on number passed, returns level, player and enemies
    returns the new level, player, enemy list, and boss (None if no boss in level)
    - num, level number which is passed to the level initialization method
    '''
    
    level = Level(num)
    x, y = level.playerStartPosit
    player = Character.PlayerCharacter(level, x, y)
    enemies = []
    if level.bossLevel:
        x, y = level.bossStartPosit
        boss = Character.Boss(level, x, y)
    else:
        boss = None

    for i in range(level.numEnemies):
        x, y = level.enemyStartPosit[i]
        enemies.append(Character.Enemy(level, x, y))

    return (level, player, enemies, boss)