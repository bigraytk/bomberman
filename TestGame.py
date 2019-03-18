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

#pygame.init()

#screenSize = (1, 1)
#screen = pygame.display.set_mode(screenSize)

class TestLevel(unittest.TestCase):

    def testGame__init__(self):
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
        self.assertIsInstance(game.statusBar, StatusBar.StatusBar)
        self.assertIsInstance(game.deathScreen, pygame.SurfaceType)
        self.assertIsInstance(game.smallScreenRect, pygame.Rect)
        self.assertIsInstance(game.gameOverImage, pygame.SurfaceType)
        self.assertIsInstance(game.playerWinsImage, pygame.SurfaceType)
        self.assertIsInstance(game.borderImage, pygame.SurfaceType)


        flag = False
        try:
            game.musicFile = "level1.csv"
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.explodeSound = "music1.mp3"
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.deathSound = "music1.mp3"
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.bossDieSound = "music1.mp3"
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.start_ticks = "a"
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.font = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.gameRunning = 0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.gameOver = 0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.playerWins = 0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.exitingToMenu = 0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.musicOn = 0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.soundOn = 0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.gameState = 10
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.gameState = 'a'
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
            game.screenImage = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.theMainMenu = HighScore.HighScore(game.screen, 800, 600)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.theMainMenu = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.highScores = MainMenu.MainMenu(game.screen, 800, 600)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.highScores = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.levelNum = -1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.levelNum = 'a'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.level = None
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
            game.numLevels = -1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.numLevels = 'a'
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
            game.spriteBombs = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.spriteBombBlasts = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.spriteBossBombBlasts = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.spritePowerups = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.statusBar = game.highScores
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.deathScreen = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.smallScreenRect = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            game.gameOverImage = None
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

        flag = False
        try:
            game.borderImage = None
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def testRender(self):
        game = Game.Game()
        game.render()

        testXY = None
        for y in range(game.level.levelHeight):
            for x in range(game.level.levelWidth):
                if isinstance(game.level.layout[y][x], Wall.Wall) and game.level.layout[y][x].door:
                    game.level.destroyWalls(x+1, y, 3)
                    testXY = (y, x)

        self.assertEqual(game.level.layout[testXY[0]][testXY[1]], const.TILE_DOOR_CLOSED)
        game.spriteEnemies.empty()
        self.assertEqual(game.level.layout[testXY[0]][testXY[1]], const.TILE_DOOR_CLOSED)
        game.render()
        self.assertEqual(game.level.layout[testXY[0]][testXY[1]], const.TILE_DOOR_OPENED)

    def testDrawLevel(self):
        game = Game.Game()
        game.drawLevel()

        game.level.layout.pop()

        flag = False
        try:
            game.drawLevel()
        except IndexError as ie:
            flag = True
        finally:
            self.assertTrue(flag)

    def testUpdateBoss(self):
        game = Game.Game()

        game.levelNum = 7
        game.resetLevel()
        self.assertIsNotNone(game.boss)
        self.assertTrue(game.boss.readyDropBomb)
        self.assertEqual(len(game.spriteBombs), 0)

        game.updateBoss()
        self.assertFalse(game.boss.readyDropBomb)
        self.assertEqual(len(game.spriteBombs), 1)

    def testStateGameRunning(self):
        game = Game.Game()
        game.soundOn = False

        self.assertEqual(game.gameState, const.GAME_STATE_MENU)
        game.killPlayer()
        self.assertEqual(game.gameState, const.GAME_STATE_MENU)
        game.gameState = game.stateGameRunning()
        self.assertEqual(game.gameState, const.GAME_STATE_PLAYER_DEAD)
        
        game.player.state = const.STATE_PLAYER_WINS
        game.gameState = game.stateGameRunning()
        self.assertEqual(game.gameState, const.GAME_STATE_PLAYER_WINS)

    def testStateQuitting(self):
        game = Game.Game()

        self.assertEqual(game.gameState, const.GAME_STATE_MENU)
        game.gameState = game.stateQuitting()
        self.assertEqual(game.gameState, const.GAME_STATE_QUITTING)

    def testResetLevel(self):
        game = Game.Game()

        self.assertEqual(len(game.spriteBombs), 0)
        self.assertIsNone(game.boss)
        game.spriteBombs.add(game.player.dropBomb(game.level))
        self.assertEqual(len(game.spriteBombs), 1)
        game.levelNum = 7
        self.assertIsNone(game.boss)

        game.resetLevel()

        self.assertIsNotNone(game.boss)
        self.assertEqual(len(game.spriteBombs), 0)
        game.spriteBombs.add(game.player.dropBomb(game.level))
        game.spriteBombs.add(game.boss.dropBomb(game.level))
        self.assertEqual(len(game.spriteBombs), 2)

        game.resetLevel()

        self.assertEqual(len(game.spriteBombs), 0)

    def testKillPlayer(self):
        game = Game.Game()
        game.soundOn = False

        self.assertEqual(game.player.lives, 3)

        game.killPlayer()

        self.assertEqual(game.player.lives, 2)

        game.killPlayer()
        game.killPlayer()

        self.assertEqual(game.player.lives, 0)
        self.assertFalse(game.gameOver)

        game.killPlayer()

        self.assertTrue(game.gameOver)

    def testCheckPlayerProgress(self):
        game = Game.Game()
        game.soundOn = False

        game.player.state = const.STATE_DEAD
        self.assertEqual(game.gameState, const.GAME_STATE_MENU)
        game.gameState = game.checkPlayerProgress()
        self.assertEqual(game.gameState, const.GAME_STATE_PLAYER_DEAD)
        game.player.state = const.STATE_PLAYER_WINS
        game.gameState = game.checkPlayerProgress()
        self.assertEqual(game.gameState, const.GAME_STATE_PLAYER_WINS)
        game.resetLevel()

        testXY = None
        for y in range(game.level.levelHeight):
            for x in range(game.level.levelWidth):
                if isinstance(game.level.layout[y][x], Wall.Wall) and game.level.layout[y][x].door:
                    game.level.destroyWalls(x+1, y, 3)
                    testXY = (y, x)
        game.level.openDoor()

        self.assertEqual(game.level.layout[testXY[0]][testXY[1]], const.TILE_DOOR_OPENED)

        game.player.y, game.player.x = testXY
        self.assertEqual(game.levelNum, 1)
        self.assertEqual(game.player.score, 0)
        game.gameState = game.checkPlayerProgress()
        self.assertEqual(game.levelNum, 2)
        self.assertGreater(game.player.score, 0)

    def testPowerUp(self):
        game = Game.Game()
        p = Powerup.Powerup(const.POWERUP_BOOT,1,1)
        self.assertEqual(p.pickUp(game.player),const.POWERUP_BOOT)


    '''
    drawStatusBar, drawText, drawTile, statePlayerDead, statePlayerWin, getUserInut, getEvents, quitGame, and debugMode
        either require user input or do not perform any actions that can be unit tested.
    stateMainMenu and stateHighScores can't be unit tested because they will load their respective menus, requiring user input.
    update can't be unit tested because it will cause the game to fully run and require user input.

    Below are the other classes tested by this test suite
    - Wall
    - Characters (Boss, Player, and Enemy)
    - Door
    - Bomb
    - StatusBar
    - PowerUp
    '''

#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)