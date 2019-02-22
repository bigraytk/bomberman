import constants as const
import colors
from pathlib import Path
import pygame

class MainMenu(object):

    def __init__(self, screen, screenWidth, screenHeight):
        '''Constructor'''
        self.screen = screen
        
        newGameButtonX = screenWidth / 2
        newGameButtonY = const.TILE_SIZE * 8

        highScoreButtonX = screenWidth / 2
        highScoreButtonY = const.TILE_SIZE * 9

        quitButtonX = screenWidth / 2
        quitButtonY = const.TILE_SIZE * 10

        graphicsDir = Path.cwd() / "graphics"

        imageFile = str(graphicsDir.joinpath("main_menu.png"))
        self.background = pygame.image.load(imageFile)

        NewGameGraph = str(graphicsDir.joinpath("NewGameButton.png"))
        self.btnNewGame = pygame.image.load(NewGameGraph)

        NewGameGraphRed = str(graphicsDir.joinpath("NewGameButton_hover.png"))
        self.btnNewGameHover = pygame.image.load(NewGameGraphRed)
        self.ngRect = self.btnNewGameHover.get_rect(center =(newGameButtonX, newGameButtonY))
        
        highScoreGraph = str(graphicsDir.joinpath("HighScores.png"))
        self.btnHighScore = pygame.image.load(highScoreGraph)
        self.hsRect = self.btnHighScore.get_rect(center =(highScoreButtonX, highScoreButtonY))
        
        highScoreGraphRed = str(graphicsDir.joinpath("HighScores_hover.png"))
        self.btnHighScoreHover = pygame.image.load(highScoreGraphRed)

        imageFile = str(graphicsDir.joinpath("button_quit.png"))
        self.btnQuit = pygame.image.load(imageFile)
        self.quitRect = self.btnQuit.get_rect(center =(quitButtonX, quitButtonY))
        
        imageFile = str(graphicsDir.joinpath("button_quit_hover.png"))
        self.btnQuitHover = pygame.image.load(imageFile)

        self.hoveringNG = False
        self.hoveringHS = False
        self.hoveringQT = False

    #main menu loop
    def showMenu(self):
        
        gameState = const.GAME_STATE_MENU
        while gameState == const.GAME_STATE_MENU:
            
            #self.screen.fill(const.GREY)
            self.screen.blit(self.background, (0,0))
            if self.hoveringNG == False:
                self.screen.blit(self.btnNewGame, self.ngRect)
            else:
                self.screen.blit(self.btnNewGameHover, self.ngRect)

            if self.hoveringHS == False:
                self.screen.blit(self.btnHighScore, self.hsRect)
            else:
                self.screen.blit(self.btnHighScoreHover, self.hsRect)

            if self.hoveringQT == False:
                self.screen.blit(self.btnQuit, self.quitRect)
            else:
                self.screen.blit(self.btnQuitHover, self.quitRect)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = const.GAME_STATE_QUITTING

                elif event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                    if self.ngRect.collidepoint(mousex, mousey):
                        self.hoveringNG = True
                    elif not self.ngRect.collidepoint(mousex, mousey):
                        self.hoveringNG = False
                    if self.hsRect.collidepoint(mousex, mousey):
                        self.hoveringHS = True
                    elif not self.hsRect.collidepoint(mousex, mousey):
                        self.hoveringHS = False
                    if self.quitRect.collidepoint(mousex, mousey):
                        self.hoveringQT = True
                    elif not self.quitRect.collidepoint(mousex, mousey):
                        self.hoveringQT = False
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if self.ngRect.collidepoint(mousex, mousey):      #clicked on new game: start level 1
                        gameState = const.GAME_STATE_RUNNING
                    elif self.hsRect.collidepoint(mousex, mousey):    #clicked on high score: show high score screen
                        gameState = const.GAME_STATE_HIGHSCORES
                        
                    elif self.quitRect.collidepoint(mousex, mousey):
                        gameState = const.GAME_STATE_QUITTING

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState = const.GAME_STATE_QUITTING

            pygame.display.update()
        return gameState
        