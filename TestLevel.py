import constants as const
import Wall
import Powerup
import Bomb
from pathlib import Path
import pygame
import unittest

import Level

pygame.init()

screenSize = (1, 1)
screen = pygame.display.set_mode(screenSize)


class TestLevel(unittest.TestCase):

    def testLevel__init__(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)

        levelNum = 7
        level2, player2, enemies2, boss2 = Level.startNewLevel(levelNum)

        self.assertIsInstance(level.backgroundImage, pygame.SurfaceType)
        self.assertIsInstance(level.breakableImage, pygame.SurfaceType)
        self.assertIsInstance(level.doorClosedImage, pygame.SurfaceType)
        self.assertIsInstance(level.doorOpenedImage, pygame.SurfaceType)
        self.assertIsInstance(level.wallImage, pygame.SurfaceType)
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


    def testLevelParser(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)

        dataDir = Path.cwd() / "data"      
        levelFile = dataDir.joinpath("level" + str(levelNum) + ".csv")

        test = level.levelParser(levelFile)

        self.assertEqual(type(test), type(level.layout))
        self.assertEqual(len(test), len(level.layout))
        self.assertEqual(len(test[0]), len(level.layout[0]))
        self.assertEqual(type(test[0][0]), type(level.layout[0][0]))
        
        test[0][0] = "B"
        cell = "B"
        self.assertEqual(test[0][0], cell)


        flag = False
        try:
            test = level.levelParser(None)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.levelParser(0)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)


    def testShowDoor(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)
        
        testXY = None
        for y in range(level.levelHeight):
            for x in range(level.levelWidth):
                if isinstance(level.layout[y][x], Wall.Wall) and level.layout[y][x].door:
                    testXY = (y, x)

        testDoor = level.layout[testXY[0]][testXY[1]]
        self.assertTrue(testDoor.door)
        self.assertIsInstance(testDoor, Wall.Wall)

        level.showDoor()
        testDoor = level.layout[testXY[0]][testXY[1]]
        self.assertEqual(testDoor, const.TILE_DOOR_CLOSED)


    def testOpenDoor(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)
        
        testXY = None
        for y in range(level.levelHeight):
            for x in range(level.levelWidth):
                if isinstance(level.layout[y][x], Wall.Wall) and level.layout[y][x].door:
                    testXY = (y, x)

        testDoor = level.layout[testXY[0]][testXY[1]]
        self.assertTrue(testDoor.door)
        self.assertIsInstance(testDoor, Wall.Wall)

        level.showDoor()
        testDoor = level.layout[testXY[0]][testXY[1]]
        self.assertEqual(testDoor, const.TILE_DOOR_CLOSED)

        level.openDoor()
        testDoor = level.layout[testXY[0]][testXY[1]]
        self.assertEqual(testDoor, const.TILE_DOOR_OPENED)


    def testDestroyWalls(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)

        breakableWallCount = 0
        for y in range(level.levelHeight):
            for x in range(level.levelWidth):
                if isinstance(level.layout[y][x], Wall.Wall) and level.layout[y][x].breakable:
                    breakableWallCount += 1

        self.assertGreater(breakableWallCount, 0)

        powerups = []
        blasts = []
        breakableWallCount = 0
        for y in range(level.levelHeight):
            for x in range(level.levelWidth):
                newPowerups, newBlasts = level.destroyWalls(x, y , 5)
                powerups.extend(newPowerups)
                blasts.extend(newBlasts)
                if isinstance(level.layout[y][x], Wall.Wall) and level.layout[y][x].breakable:
                    breakableWallCount += 1

        self.assertEqual(breakableWallCount, 0)
        self.assertGreater(len(powerups), 0)
        self.assertGreater(len(blasts), 0)
        self.assertIsInstance(powerups[0], Powerup.Powerup)
        self.assertIsInstance(powerups[-1], Powerup.Powerup)
        self.assertIsInstance(blasts[0], Bomb.Blast)
        self.assertIsInstance(blasts[-1], Bomb.Blast)


        flag = False
        try:
            test = level.destroyWalls(-1, 1 , 5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls(1, -1 , 5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls(1, 1 , -5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls('a', 1 , 5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls(1, 'b' , 5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls(1, 1 , 'c')
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls(None, 1 , 5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls(1, None , 5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test = level.destroyWalls(1, 1 , None)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)


    def testStartNewLevel(self):
        levelNum = 1
        level, player, enemies, boss = Level.startNewLevel(levelNum)
        level2, player, enemies, boss = Level.startNewLevel(levelNum)

        self.assertEqual(level.playerStartPosit, level2.playerStartPosit)
        self.assertEqual(level.bossLevel, level2.bossLevel)
        self.assertEqual(level.enemyFile, level2.enemyFile)
        self.assertEqual(level.numEnemies, level2.numEnemies)

        levelNum = 7
        level2, player, enemies, boss = Level.startNewLevel(levelNum)
        
        self.assertNotEqual(level.playerStartPosit, level2.playerStartPosit)
        self.assertNotEqual(level.bossLevel, level2.bossLevel)
        self.assertNotEqual(level.enemyFile, level2.enemyFile)
        self.assertNotEqual(level.numEnemies, level2.numEnemies)


        flag = False
        try:
            level, player, enemies, boss = Level.startNewLevel(-1)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            level, player, enemies, boss = Level.startNewLevel('a')
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)



#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)