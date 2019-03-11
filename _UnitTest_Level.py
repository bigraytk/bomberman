#import constants as const
#import Wall
#import Character
#import Bomb
#from pathlib import Path
import pygame
import unittest
#import sys

import Level

pygame.init()

screenSize = (800, 600)
screen = pygame.display.set_mode(screenSize)

#TODO finish


class TestLevel(unittest.TestCase):


    def test__init__(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)

        #self.assertEqual(c.radius, r)
        #self.assertEqual(c.location, p)
        
        flag = False
        try:
            level, player, enemies, boss = Level.startNewLevel('1')
            #c = Circle.Circle(Point.Point('P', r))
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)


        flag = False
        try:
            level, player, enemies, boss = Level.startNewLevel(-1)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)


#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)