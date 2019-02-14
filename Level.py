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


class Level(object):
    
    def __init__(self, levelNum):
        #set class variable
        self.backgroundImage = None
        self.wallImage = None
        self.breakableImage = None
        self.doorOpenedImage = None
        self.doorClosedImage = None
        self.levelFile = None
        self.layout = []
        self.levelWidth = None
        self.levelHeight = None
        self.door = const.TILE_DOOR_HIDDEN
        self.playerStartPosit = None
        self.numEnemies = 0
        self.enemyStartPosit = []

        # Set the current working directory, read and write:
        dataDir = Path.cwd() / "data"

        #Open csv level file to create level layout      
        levelFile = dataDir.joinpath("level" + str(levelNum) + ".csv")
        self.layout = self.levelParser(levelFile)
    
    def levelParser(self, levelFile):
        layout = []
        graphicsDir = Path.cwd() / "graphics"
        with levelFile.open() as f: 
            levelParams = f.readline().split(",")
            self.levelWidth = int(levelParams[const.LEVEL_WIDTH])
            self.levelHeight = int(levelParams[const.LEVEL_HEIGHT])
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
                         
        backgroundFile = str(graphicsDir.joinpath("back" + str(backgroundNum) + ".png"))
        self.backgroundImage = pygame.image.load(backgroundFile).convert()
         
        wallFile = str(graphicsDir.joinpath("wall" + str(wallNum) + ".png"))
        self.wallImage = pygame.image.load(wallFile).convert()
         
        breakableFile = str(graphicsDir.joinpath("break" + str(breakableNum) + ".png"))
        self.breakableImage = pygame.image.load(breakableFile).convert()

        doorOpenedFile = str(graphicsDir.joinpath("door_opened.png"))
        self.doorOpenedImage = pygame.image.load(doorOpenedFile).convert_alpha()
         
        doorClosedFile = str(graphicsDir.joinpath("door_closed.png"))
        self.doorClosedImage = pygame.image.load(doorClosedFile).convert_alpha()

        enemyFile = str(graphicsDir.joinpath("enemy" + str(enemyNum) + ".png"))
        self.enemyImage = pygame.image.load(enemyFile).convert_alpha()
        
        return layout


    def showDoor(self):
        for y in range(self.levelHeight):
            for x in range(self.levelWidth):
                if isinstance(self.layout[y][x], Wall.Wall) and self.layout[y][x].door:
                    self.layout[y][x] = const.TILE_DOOR_CLOSED
        door = const.TILE_DOOR_CLOSED
        
        
    def openDoor(self):
        for y in range(self.levelHeight):
            for x in range(self.levelWidth):
                if self.layout[y][x] == const.TILE_DOOR_CLOSED:
                    self.layout[y][x] = const.TILE_DOOR_OPENED
        door = const.TILE_DOOR_CLOSED
        
        
    def destroyWalls(self, x, y, level, blastRange):     #TODO make it so that "range" is utilized so walls in all four directions at that range are destroyed
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


#class tileSprite(pygame.sprite.DirtySprite):
#    '''
#    Usage: TileSprite(image, x, y).  Use map grid coordinates, not actual on screen x,y values
#    '''
#    def __init__(self, image, x, y):
#        # call DirtySprite initializer
#        pygame.sprite.DirtySprite.__init__(self)
#        self.image = image
#        self.rect = self.image.get_rect()
#        self.rect.x = const.SCREEN_OFFSET_X_LEFT + x * const.TILE_SIZE
#        self.rect.y = const.SCREEN_OFFSET_Y_TOP + y * const.TILE_SIZE
#        self.dirty = 2      #Tile is redrawn every frame.  Could use 1 to redraw once until flag is reset, useful for optimization


#Loads level file based on number passed, returns level, player and enemies
def startNewLevel(num):
    level = Level(num)
    x, y = level.playerStartPosit
    player = Character.PlayerCharacter(level, x, y)
    enemies = []
    for i in range(level.numEnemies):
        x, y = level.enemyStartPosit[i]
        enemies.append(Character.Enemy(level, x, y))
    
    return (level, player, enemies)