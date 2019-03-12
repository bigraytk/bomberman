import constants as const
import colors
from pathlib import Path
import pygame

class MainMenu(object):

    def __init__(self, screen, screenWidth, screenHeight):
        '''Constructor'''

        #check that screenWidth and height are ints
        if not isinstance(screenWidth,int) or not isinstance(screenHeight,int):
            raise RuntimeError('Error: screenWidth and screenHeight must be ints')

        if not isinstance(screen,pygame.Surface):
            raise RuntimeError('Error: screen must be an instance of pygame.Surface')

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
            raise RuntimeError('Error: Unable to load graphics files')

        self.__hoveringNG__ = False
        self.__hoveringHS__ = False
        self.__hoveringQT__ = False

    
    def showMenu(self, musicOn):
        '''Method that contians the loop that displays the main menu and handles game state transitions to other elements of the game'''

    
        if not isinstance(musicOn,bool):
            raise RuntimeError('Error: musicOn must be a boolean')

        
        gameState = const.GAME_STATE_MENU
        while gameState == const.GAME_STATE_MENU:
            if musicOn:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()
            
            self.__screen__.blit(self.__background__, (0,0))
            if self.__hoveringNG__ == False:
                self.__screen__.blit(self.__btnNewGame__, self.__ngRect__)
            else:
                self.__screen__.blit(self.__btnNewGameHover__, self.__ngRect__)

            if self.__hoveringHS__ == False:
                self.__screen__.blit(self.__btnHighScore__, self.__hsRect__)
            else:
                self.__screen__.blit(self.__btnHighScoreHover__, self.__hsRect__)

            if self.__hoveringQT__ == False:
                self.__screen__.blit(self.__btnQuit__, self.__quitRectt__)
            else:
                self.__screen__.blit(self.__btnQuitHover__, self.__quitRectt__)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = const.GAME_STATE_QUITTING

                elif event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                    if self.__ngRect__.collidepoint(mousex, mousey):
                        self.__hoveringNG__ = True
                    elif not self.__ngRect__.collidepoint(mousex, mousey):
                        self.__hoveringNG__ = False
                    if self.__hsRect__.collidepoint(mousex, mousey):
                        self.__hoveringHS__ = True
                    elif not self.__hsRect__.collidepoint(mousex, mousey):
                        self.__hoveringHS__ = False
                    if self.__quitRectt__.collidepoint(mousex, mousey):
                        self.__hoveringQT__ = True
                    elif not self.__quitRectt__.collidepoint(mousex, mousey):
                        self.__hoveringQT__ = False
                
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
        