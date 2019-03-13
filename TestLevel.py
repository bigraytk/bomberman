#import constants as const
#import Wall
#import Character
#import Bomb
from pathlib import Path
import pygame
import constants as const
import unittest
#import sys

import Level

pygame.init()

screenSize = (1, 1)
screen = pygame.display.set_mode(screenSize)

#TODO finish


class TestLevel(unittest.TestCase):


    def test__init__(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)

        levelNum = 7
        level2, player2, enemies2, boss2 = Level.startNewLevel(levelNum)

        self.assertIsInstance(level.backgroundImage, pygame.SurfaceType)
        self.assertIsInstance(level.breakableImage, pygame.SurfaceType)
        self.assertIsInstance(level.doorClosedImage, pygame.SurfaceType)
        self.assertIsInstance(level.doorOpenedImage, pygame.SurfaceType)
        self.assertIsInstance(level.wallImage, pygame.SurfaceType)
        self.assertEqual(level.door, const.TILE_DOOR_HIDDEN)
        self.assertGreater(level.numEnemies, 0)
        self.assertIsInstance(level.enemyStartPosit, list)
        for i in range(len(level.enemyStartPosit)):
            self.assertIsInstance(level.enemyStartPosit[i], tuple)
        self.assertIsInstance(level.playerStartPosit, tuple)
        self.assertFalse(level.bossLevel)
        self.assertIsInstance(level.enemyFile, Path)

        self.assertIsInstance(level2.bossStartPosit, tuple)
        self.assertTrue(level2.bossLevel)

        
        flag = False
        try:
            level, player, enemies, boss = Level.startNewLevel('1')
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

        flag = False
        try:
            level.backgroundImage = 'a'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.breakableImage = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.doorClosedImage = 'b'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.doorOpenedImage = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.wallImage = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.door = True
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.numEnemies = -1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.enemyStartPosit = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            level.playerStartPosit = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level.bossLevel = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)




#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)