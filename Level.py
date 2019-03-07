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
    try:
        if convertAlpha:
            image = pygame.image.load(imageFile).convert_alpha()
        else:
            image = pygame.image.load(imageFile).convert()
        return image
    except IOError:
        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit()
        raise RuntimeError('Error: File ' + str(imageFile) + " does not exist!")


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
        self.bossLevel = None
        self.bossStartPosit = None

        # Set the current working directory, read and write:
        dataDir = Path.cwd() / "data"

        #Open csv level file to create level layout      
        levelFile = dataDir.joinpath("level" + str(levelNum) + ".csv")
        self.layout = self.levelParser(levelFile)
    
    def levelParser(self, levelFile):
        layout = []
        graphicsDir = Path.cwd() / "graphics"
        try:
            with levelFile.open() as f: 
                levelParams = f.readline().split(",")
                self.levelWidth = int(levelParams[const.LEVEL_WIDTH])
                self.levelHeight = int(levelParams[const.LEVEL_HEIGHT])
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

        backgroundFile = str(graphicsDir.joinpath("back" + str(backgroundNum) + ".png"))
        self.backgroundImage = openImage(backgroundFile)
         
        wallFile = str(graphicsDir.joinpath("wall" + str(wallNum) + ".png"))
        self.wallImage = openImage(wallFile)
         
        breakableFile = str(graphicsDir.joinpath("break" + str(breakableNum) + ".png"))
        self.breakableImage = openImage(breakableFile)

        doorOpenedFile = str(graphicsDir.joinpath("door_opened.png"))
        self.doorOpenedImage = openImage(doorOpenedFile, True)
         
        doorClosedFile = str(graphicsDir.joinpath("door_closed.png"))
        self.doorClosedImage = openImage(doorClosedFile, True)

        self.enemyFile = str(graphicsDir.joinpath("enemy" + str(enemyNum) + ".png"))

        
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


#Loads level file based on number passed, returns level, player and enemies
def startNewLevel(num):
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