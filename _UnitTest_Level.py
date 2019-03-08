#import constants as const
#import Wall
#import Character
#import Bomb
#from pathlib import Path
import pygame
#import sys

import Level

pygame.init()

screenSize = (800, 600)
screen = pygame.display.set_mode(screenSize)


levelNum = 1
level, player, enemies, boss = Level.startNewLevel(levelNum)



print(player)