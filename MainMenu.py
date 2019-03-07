import constants as const
import colors
from pathlib import Path
import pygame

class MainMenu(object):

    def __init__(self, screen, screenWidth, screenHeight):
        '''Constructor'''
        self.__screen__ = screen
        
        newGameButtonX = screenWidth / 2
        newGameButtonY = const.TILE_SIZE * 8

        highScoreButtonX = screenWidth / 2
        highScoreButtonY = const.TILE_SIZE * 9

        quitButtonX = screenWidth / 2
        quitButtonY = const.TILE_SIZE * 10

        graphicsDir = Path.cwd() / "graphics"

        try:

            imageFile = str(graphicsDir.joinpath("main_menu.png"))
            self.__background__ = pygame.image.load(imageFile)
            

            NewGameGraph = str(graphicsDir.joinpath("NewGameButton.png"))
            self.__btnNewGame__ = pygame.image.load(NewGameGraph)

            NewGameGraphRed = str(graphicsDir.joinpath("NewGameButton_hover.png"))
            self.__btnNewGameHover__ = pygame.image.load(NewGameGraphRed)
            self.__ngRect__ = self.__btnNewGameHover__.get_rect(center =(newGameButtonX, newGameButtonY))
            
            highScoreGraph = str(graphicsDir.joinpath("HighScores.png"))
            self.__btnHighScore__ = pygame.image.load(highScoreGraph)
            self.__hsRect__ = self.__btnHighScore__.get_rect(center =(highScoreButtonX, highScoreButtonY))
            
            highScoreGraphRed = str(graphicsDir.joinpath("HighScores_hover.png"))
            self.__btnHighScoreHover__ = pygame.image.load(highScoreGraphRed)

            imageFile = str(graphicsDir.joinpath("button_quit.png"))
            self.__btnQuit__ = pygame.image.load(imageFile)
            self.__quitRectt__ = self.__btnQuit__.get_rect(center =(quitButtonX, quitButtonY))
            
            imageFile = str(graphicsDir.joinpath("button_quit_hover.png"))
            self.__btnQuitHover__ = pygame.image.load(imageFile)
        except:
            raise RuntimeError('Error: Unable to load graphis file')

        self.hoveringNG = False
        self.hoveringHS = False
        self.hoveringQT = False

    #main menu loop
    def showMenu(self):
        
        gameState = const.GAME_STATE_MENU
        while gameState == const.GAME_STATE_MENU:
            
            self.__screen__.blit(self.__background__, (0,0))
            if self.hoveringNG == False:
                self.__screen__.blit(self.__btnNewGame__, self.__ngRect__)
            else:
                self.__screen__.blit(self.__btnNewGameHover__, self.__ngRect__)

            if self.hoveringHS == False:
                self.__screen__.blit(self.__btnHighScore__, self.__hsRect__)
            else:
                self.__screen__.blit(self.__btnHighScoreHover__, self.__hsRect__)

            if self.hoveringQT == False:
                self.__screen__.blit(self.__btnQuit__, self.__quitRectt__)
            else:
                self.__screen__.blit(self.__btnQuitHover__, self.__quitRectt__)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = const.GAME_STATE_QUITTING

                elif event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                    if self.__ngRect__.collidepoint(mousex, mousey):
                        self.hoveringNG = True
                    elif not self.__ngRect__.collidepoint(mousex, mousey):
                        self.hoveringNG = False
                    if self.__hsRect__.collidepoint(mousex, mousey):
                        self.hoveringHS = True
                    elif not self.__hsRect__.collidepoint(mousex, mousey):
                        self.hoveringHS = False
                    if self.__quitRectt__.collidepoint(mousex, mousey):
                        self.hoveringQT = True
                    elif not self.__quitRectt__.collidepoint(mousex, mousey):
                        self.hoveringQT = False
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if self.__ngRect__.collidepoint(mousex, mousey):      #clicked on new game: start level 1
                        gameState = const.GAME_STATE_RUNNING
                    elif self.__hsRect__.collidepoint(mousex, mousey):    #clicked on high score: show high score screen
                        gameState = const.GAME_STATE_HIGHSCORES
                        
                    elif self.__quitRectt__.collidepoint(mousex, mousey):
                        gameState = const.GAME_STATE_QUITTING

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState = const.GAME_STATE_QUITTING

            pygame.display.update()
        return gameState
        