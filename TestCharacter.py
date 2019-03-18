import constants as const
import Wall
import Powerup
import Bomb
import Level
import Character
import HighScore
import MainMenu
import StatusBar
from pathlib import Path
import pygame
import unittest

import Game

'''

-Character (Ray)
-Bomb(Ray)
-Door(Ray)
-Wall(Ray)
-Powerup(Ray)
-Statusbar(Ray)
'''

class TestCharacter(unittest.TestCase):

    def testCharacter__init__(self):
        game = Game.Game()
        self.assertIn("/sounds/music1.mp3", game.musicFile,)
        self.assertIsInstance(game.explodeSound, pygame.mixer.SoundType)
        self.assertIsInstance(game.deathSound, pygame.mixer.SoundType)
        self.assertIsInstance(game.bossDieSound, pygame.mixer.SoundType)
        self.assertEqual(game.start_ticks, 0.0)
        self.assertIsInstance(game.font, pygame.font.FontType)
        self.assertIsInstance(game.gameRunning, bool)
        self.assertIsInstance(game.gameOver, bool)
        self.assertIsInstance(game.playerWins, bool)
        self.assertIsInstance(game.exitingToMenu, bool)
        self.assertIsInstance(game.musicOn, bool)
        self.assertIsInstance(game.soundOn, bool)
        self.assertIn(game.gameState, [const.GAME_STATE_MENU, const.GAME_STATE_RUNNING, const.GAME_STATE_PLAYER_DEAD,
                                        const.GAME_STATE_PLAYER_WINS, const.GAME_STATE_QUITTING, const.GAME_STATE_HIGHSCORES ])
        self.assertIsInstance(game.screenImage, pygame.SurfaceType)
        self.assertIsInstance(game.theMainMenu, MainMenu.MainMenu)
        self.assertIsInstance(game.highScores, HighScore.HighScore)
        self.assertEqual(game.levelNum, 1)
        self.assertIsInstance(game.level, Level.Level)
        self.assertIsInstance(game.player, Character.PlayerCharacter)
        self.assertIsInstance(game.enemies, list)

        for i in range(len(game.spriteEnemies)):
            self.assertIsInstance(game.enemies[i], Character.Enemy)
        self.assertEqual(game.boss, None)
        self.assertEqual(game.numLevels, 7)
        self.assertIn(game.player, game.spritePlayer)
        self.assertIn(game.enemies, game.spriteEnemies)
        for bomb in game.spriteBombs:
            self.assertIsInstance(bomb, Bomb.Bomb)
        for blast in game.spriteBombBlasts:
            self.assertIsInstance(blast, Bomb.Blast)
        for blast2 in game.spriteBossBombBlasts:
            self.assertIsInstance(blast2, Bomb.Blast)
        for powerup in game.spritePowerups:
            self.assertIsInstance(powerup, Powerup.Powerup)

        flag = False
        try:
            game.playerWins = 0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.screenImage = "enemy1.png"
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            game.player = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.player = game.boss
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.enemies = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.boss = game.player
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.spritePlayer = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
    
        flag = False
        try:
            game.spriteEnemies = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.playerWinsImage = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def testIncreaseScore(self):
        game = Game.Game()
        game.player.increaseScore(10)

        self.assertEqual(game.player.score ,10)

    def testMove(self):
        game = Game.Game()
        game.drawLevel()

        game.player.move(const.DOWN,game.level)
        self.assertTrue(game.player.facing,const.DOWN)

        

    def testGetPowerUp(self):
        game = Game.Game()

        p = Powerup.Powerup(const.POWERUP_RANGE,1,1)
        self.assertTrue(game.player.bombRange,0)
        game.player.getPowerup(p)
        self.assertTrue(game.player.bombRange,1)

        p = Powerup.Powerup(const.POWERUP_COUNT,1,1)
        self.assertTrue(game.player.bombCount,0)
        game.player.getPowerup(p)
        self.assertTrue(game.player.bombCount,1)

        p = Powerup.Powerup(const.POWERUP_BOOT,1,1)
        self.assertFalse(game.player.boot,False)
        game.player.getPowerup(p)
        self.assertTrue(game.player.boot,True)

    def testChangeDirection(self):
        game = Game.Game()
        
        game.player.changeDirection(const.UP)
        self.assertTrue(game.player.facing,const.UP)

        game.player.changeDirection(const.DOWN)
        self.assertTrue(game.player.facing,const.DOWN)

        game.player.changeDirection(const.RIGHT)
        self.assertTrue(game.player.facing,const.RIGHT)

        game.player.changeDirection(const.LEFT)
        self.assertTrue(game.player.facing,const.LEFT)


    def testDropBomb(self):
        game = Game.Game()
        bomb = game.player.dropBomb(game.level)
        self.assertIsInstance(bomb,Bomb.Bomb)

    def testChangeActiveBombCount(self):
        game = Game.Game()

        self.assertFalse(game.player.activeBombs, 0)
        game.player.changeActiveBombCount(1)
        self.assertTrue(game.player.activeBombs, 1)
        
        bomb = game.player.dropBomb(game.level)
        self.assertTrue(game.player.activeBombs, 2)


    
        

    '''
    update and advanceMovement
        either require user input or do not perform any actions that can be unit tested.
    '''

#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)