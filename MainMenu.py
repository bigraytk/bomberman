import constants as const
import colors
from pathlib import Path
import pygame

class MainMenu(object):

    def __init__(self, screen, screenWidth, screenHeight):
        '''Constructor'''
        self.screen = screen
        
        newGameButtonX = screenWidth / 2
        newGameButtonY = screenHeight / 4

        highScoreButtonX = screenWidth / 2
        highScoreButtonY = screenHeight / 3

        '''Will display the main menu.'''
        self.screen.fill(const.GREY)

        graphicsDir = Path.cwd() / "graphics"

        NewGameGraph = str(graphicsDir.joinpath("NewGameButton.png"))
        self.btnNewGame = pygame.image.load(NewGameGraph)

        NewGameGraphRed = str(graphicsDir.joinpath("NewGameButton_Red.png"))
        self.btnNewGameRed = pygame.image.load(NewGameGraphRed)
        self.ngRect = self.btnNewGameRed.get_rect(center =(newGameButtonX, newGameButtonY))
        
        highScoreGraph = str(graphicsDir.joinpath("HighScores.png"))
        self.btnHighScore = pygame.image.load(highScoreGraph)
        self.hsRect = self.btnHighScore.get_rect(center =(highScoreButtonX, highScoreButtonY))
        
        highScoreGraphRed = str(graphicsDir.joinpath("HighScores_Red.png"))
        self.btnHighScoreRed = pygame.image.load(highScoreGraphRed)

        self.hoveringNG = False
        self.hoveringHS = False

    #main menu loop
    def showMenu(self):
        
        gameState = const.GAME_STATE_MENU
        while gameState == const.GAME_STATE_MENU:
            
            self.screen.fill(const.GREY)
            if self.hoveringNG == False:
                self.screen.blit(self.btnNewGame, self.ngRect)
            else:
                self.screen.blit(self.btnNewGameRed, self.ngRect)

            if self.hoveringHS == False:
                self.screen.blit(self.btnHighScore, self.hsRect)
            else:
                self.screen.blit(self.btnHighScoreRed, self.hsRect)


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
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if self.ngRect.collidepoint(mousex, mousey):      #clicked on new game: start level 1
                        gameState = const.GAME_STATE_RUNNING
                    elif self.hsRect.collidepoint(mousex, mousey):    #clicked on high score: show high score screen
                        #TODO
                        #show the high score screen
                        pass

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState = const.GAME_STATE_QUITTING

            pygame.display.update()
        return gameState
        