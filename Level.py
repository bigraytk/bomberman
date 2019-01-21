# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 13:17:57 2019

@author: 
"""
import constants as const
import Wall
from pathlib import Path
import pygame

class Level(object):
    backgroundImage = None
    wallImage = None
    breakableImage = None
    doorOpenedImage = None
    doorClosedImage = None
    levelFile = None
    layout = []
    levelWidth = None
    levelHeight = None
    door = const.TILE_DOOR_HIDDEN
    playerStartPosit = None
    numEnemies = 0
    enemyStartPosit = []
    
    #@property
    #def backgroundFile(self):
    #    return self.__backgroundFile

    #@backgroundFile.setter
    #def backgroundFile(self, backgroundFile):
    #    self.__backgroundFile = backgroundFile
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
        
            for i in range(self.levelHeight):
                line = f.readline().split(",")
                line[-1] = line[-1][0]     #remove "\n" from the last element of each line imported from the csv file
                layout.append(line)
            for y in range(self.levelHeight):
                for x in range(self.levelWidth):
                    if layout[y][x] == '':
                        layout[y][x] = None
                    elif layout[y][x] == const.TILE_WALL:
                        layout[y][x] = Wall.Wall(False, 0)
                    elif layout[y][x] == const.TILE_BREAKABLE:
                        layout[y][x] = Wall.Wall(True, 0)
                    elif layout[y][x] == const.TILE_DOOR_HIDDEN:
                        layout[y][x] = Wall.Wall(True, 0, True)
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
        
        
    def __init__(self, levelNum):
        # Set the current working directory, read and write:
        self.numEnemies = 0
        dataDir = Path.cwd() / "data"
         
        #Open csv level file to create level layout      
        levelFile = dataDir.joinpath("level" + str(levelNum) + ".csv")
        self.layout = self.levelParser(levelFile)



