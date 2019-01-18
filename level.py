# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 13:17:57 2019

@author: jkh02
"""
from constants import *
from pathlib import Path
import Wall
import pygame

class Level(object):
    __backgroundImage = None
    __wallImage = None
    __breakableImage = None
    __doorOpenedImage = None
    __doorClosedImage = None
    __levelFile = None
    layout = []
    levelWidth = None
    levelHeight = None
    door = TILE_DOOR_HIDDEN
    
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
             self.levelWidth = int(levelParams[LEVEL_WIDTH])
             self.levelHeight = int(levelParams[LEVEL_HEIGHT])
             backgroundNum = int(levelParams[LEVEL_BG_GFX])
             wallNum = int(levelParams[LEVEL_WALL_GFX])
             breakableNum = int(levelParams[LEVEL_BREAK_GFX])
        
             for i in range(self.levelHeight):
                 line = f.readline().split(",")
                 line[-1] = line[-1][0]     #remove "\n" from the last element of each line imported from the csv file
                 layout.append(line)
             for y in range(self.levelHeight):
                 for x in range(self.levelWidth):
                     if layout[y][x] == '':
                         layout[y][x] = None
                     elif layout[y][x] == TILE_WALL:
                         layout[y][x] = Wall.Wall(False, 0)
                     elif layout[y][x] == TILE_BREAKABLE:
                         layout[y][x] = Wall.Wall(True, 0)
                         
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


    def show_door(self):
        for y in range(self.levelHeight):
            for x in range(self.levelWidth):
                if self.layout[y][x] == TILE_DOOR_HIDDEN:
                    self.layout[y][x] = TILE_DOOR_CLOSED
        door = TILE_DOOR_CLOSED
        
        
    def open_door(self):
        for y in range(self.levelHeight):
            for x in range(self.levelWidth):
                if self.layout[y][x] == TILE_DOOR_CLOSED:
                    self.layout[y][x] = TILE_DOOR_OPENED
        door = TILE_DOOR_CLOSED
        
        
    def __init__(self, levelNum):
         # Set the current working directory, read and write:
         dataDir = Path.cwd() / "data"
         
         #Open csv level file to create level layout      
         levelFile = dataDir.joinpath("level" + str(levelNum) + ".csv")
         self.layout = self.levelParser(levelFile)


         
# Importing level data
#lev1 = Level(1, 1, 1, 1)



