
#How to transition from the high scores to the main menu and back?
import InputBox
from pathlib import Path
import constants as const
import LinkedList as LL
import pygame
import JsonEncoder



class HighScore(object):

    def __init__(self, screen, screenWidth, screenHeight):
        '''Constructor'''

        if not isinstance(screenWidth,int) or not isinstance(screenHeight,int):
            raise RuntimeError('Error: screenWidth and screenHeight must be ints')

        if not isinstance(screen,pygame.Surface):
            raise RuntimeError('Error: screen must be an instance of pygame.Surface')



        self.__screen__ = screen #how to check this
        self.__screenWidth__ = screenWidth
        self.__screenHeight__ = screenHeight
        self.__font__ = pygame.font.Font(None, 48)
        self.__yOffset__ = 48
        
        

        self.__scoreFile__ = str(Path.cwd() / "HighScores" / "Scores.json")

        graphicsDir = Path.cwd() / "graphics"

        imageFile = str(graphicsDir.joinpath("high_scores.png"))

        try:
            self.__background__ = pygame.image.load(imageFile)
        except:
            raise RuntimeError('Error: unable to open ' , imageFile)

        mainMenuButtonX = screenWidth / 2
        mainMenuButtonY = const.TILE_SIZE * 11

        mainMenuGraph = str(graphicsDir.joinpath("MainMenuButton.png"))
        self.__btnMainMenu__ = pygame.image.load(mainMenuGraph)

        mainMenuGraphRed = str(graphicsDir.joinpath("MainMenuButton_hover.png"))

        try:
            self.__btnMainMenuHover__ = pygame.image.load(mainMenuGraphRed)
        except:
            raise RuntimeError("Error: unable to open " , mainMenuGraphRed)
        self.__mmRect__ = self.__btnMainMenuHover__.get_rect(center =(mainMenuButtonX, mainMenuButtonY))

        self.__hoveringMM__ = False

        try:
            self.__scoreList__ = JsonEncoder.readData(self.__scoreFile__)
        except:
            raise RuntimeError('Error: unable to open or load ' , self.__scoreFile__)
       

        
    def newScore(self, value):
        '''checks to see if the passed value is a high score. If it is, will update the scoreList and ask 
        for user input for the name.'''
        #check data structure to see where the new score goes
        
        if self.__scoreList__.numberOfNodes >= 10:
            if value > self.__scoreList__.tail.score:
                self.__scoreList__.deleteTail()
                #have user input initials to go with the score
                fontSize = 64
                inputBox = InputBox.InputBox(self.__screen__, self.__screenWidth__//2 - fontSize, self.__screenHeight__//3, fontSize * 2, fontSize, fontSize, const.GREY, const.GREEN)
                newName = inputBox.run()

                #add the newName and the score to the data structure
                self.__scoreList__.insertInOrder(value, newName)
                JsonEncoder.loadData(self.__scoreList__, self.__scoreFile__)
        else:
            #have user input initials to go with the score
            fontSize = 64
            inputBox = InputBox.InputBox(self.__screen__, self.__screenWidth__//2 - fontSize, self.__screenHeight__//3, fontSize * 2, fontSize, fontSize, const.GREY, const.GREEN)
            newName = inputBox.run()

            #add the newName and the score to the data structure
            self.__scoreList__.insertInOrder(value,newName)
            JsonEncoder.loadData(self.__scoreList__, self.__scoreFile__)


    def drawText(self, text, x, y, color):
        textSurface = self.__font__.render(text, True, color)
        self.__screen__.blit(textSurface, (x, y))     


    def display(self):
        '''Displays the high scores and manages the buttons to return to the main menu'''
        gamestate = const.GAME_STATE_HIGHSCORES
        scoreArray = self.__scoreList__.readData()
        while gamestate == const.GAME_STATE_HIGHSCORES:
            self.__screen__.blit(self.__background__, (0,0))

            xPos = self.__screenWidth__ // 2 - 110
            yPos = 120
            for element in scoreArray:
                #scoreLine = "{0:>4}{1:>12}".format(element[1], (element[0]))
                #self.drawText(scoreLine, xPos, yPos, const.YELLOW)
                self.drawText(str(element[1]), xPos, yPos, const.YELLOW)
                self.drawText(str(element[0]), xPos + 128, yPos, const.YELLOW)
                yPos = yPos + self.__yOffset__

            if self.__hoveringMM__ == False:
                self.__screen__.blit(self.__btnMainMenu__, self.__mmRect__)
            else:
                self.__screen__.blit(self.__btnMainMenuHover__, self.__mmRect__)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gamestate = const.GAME_STATE_QUITTING

                elif event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                    if self.__mmRect__.collidepoint(mousex, mousey):
                        self.__hoveringMM__ = True
                    elif not self.__mmRect__.collidepoint(mousex, mousey):
                        self.__hoveringMM__ = False


                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if self.__mmRect__.collidepoint(mousex, mousey):      #clicked on new game: start level 1
                        gamestate = const.GAME_STATE_MENU


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = const.GAME_STATE_QUITTING

            pygame.display.update()

        return gamestate

    
    

if __name__ == "__main__":
    filePath = str(Path.cwd() / "HighScores" / "Scores.json")
    test = JsonEncoder.readData(filePath)
    print(test)
    




    
    



    