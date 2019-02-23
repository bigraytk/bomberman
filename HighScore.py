
#How to transition from the high scores to the main menu and back?
import InputBox
from pathlib import Path
import constants as const
import LinkedList as LL
import pygame



class HighScore(object):

    def __init__(self, screen, screenWidth, screenHeight):
        '''Constructor'''
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.font = pygame.font.Font(None, 48)
        self.yOffset = 48
        
        

        self.scoreFile = str(Path.cwd() / "HighScores" / "Scores.pickle")

        graphicsDir = Path.cwd() / "graphics"

        imageFile = str(graphicsDir.joinpath("high_scores.png"))
        self.background = pygame.image.load(imageFile)

        mainMenuButtonX = screenWidth / 2
        mainMenuButtonY = const.TILE_SIZE * 11

        mainMenuGraph = str(graphicsDir.joinpath("MainMenuButton.png"))
        self.btnMainMenu = pygame.image.load(mainMenuGraph)

        mainMenuGraphRed = str(graphicsDir.joinpath("MainMenuButton_hover.png"))
        self.btnMainMenuHover = pygame.image.load(mainMenuGraphRed)
        self.mmRect = self.btnMainMenuHover.get_rect(center =(mainMenuButtonX, mainMenuButtonY))

        self.hoveringMM = False

        #unpickle the file into the tree
        self.scoreList = LL.loadList(self.scoreFile)

        
    def newScore(self, value):
        '''checks to see if the passed value is a high score. If it is, will update the scoreList and ask 
        for user input for the name.'''
        #check data structure to see where the new score goes
        
        if self.scoreList.numberOfNodes >= 10:
            if value > self.scoreList.tail.score:
                self.scoreList.deleteTail()
                #have user input initials to go with the score
                fontSize = 64
                inputBox = InputBox.InputBox(self.screen, self.screenWidth//2 - fontSize, self.screenHeight//3, fontSize * 2, fontSize, fontSize, const.GREY, const.GREEN)
                newName = inputBox.run()

                #add the newName and the score to the data structure
                self.scoreList.insertInOrder(value, newName)
                LL.saveList(self.scoreList, self.scoreFile)
        else:
            #have user input initials to go with the score
            fontSize = 64
            inputBox = InputBox.InputBox(self.screen, self.screenWidth//2 - fontSize, self.screenHeight//3, fontSize * 2, fontSize, fontSize, const.GREY, const.GREEN)
            newName = inputBox.run()

            #add the newName and the score to the data structure
            self.scoreList.insertInOrder(value,newName)
            LL.saveList(self.scoreList, self.scoreFile)


    def drawText(self, text, x, y, color):
        textSurface = self.font.render(text, True, color)
        self.screen.blit(textSurface, (x, y))     


    def display(self):
        '''Displays the high scores and manages the buttons to return to the main menu'''
        gamestate = const.GAME_STATE_HIGHSCORES
        scoreArray = self.scoreList.readData()
        while gamestate == const.GAME_STATE_HIGHSCORES:
            self.screen.blit(self.background, (0,0))

            xPos = self.screenWidth // 2 - 110
            yPos = 120
            for element in scoreArray:
                #scoreLine = "{0:>4}{1:>12}".format(element[1], (element[0]))
                #self.drawText(scoreLine, xPos, yPos, const.YELLOW)
                self.drawText(str(element[1]), xPos, yPos, const.YELLOW)
                self.drawText(str(element[0]), xPos + 128, yPos, const.YELLOW)
                yPos = yPos + self.yOffset

            if self.hoveringMM == False:
                self.screen.blit(self.btnMainMenu, self.mmRect)
            else:
                self.screen.blit(self.btnMainMenuHover, self.mmRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gamestate = const.GAME_STATE_QUITTING

                elif event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                    if self.mmRect.collidepoint(mousex, mousey):
                        self.hoveringMM = True
                    elif not self.mmRect.collidepoint(mousex, mousey):
                        self.hoveringMM = False


                elif event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if self.mmRect.collidepoint(mousex, mousey):      #clicked on new game: start level 1
                        gamestate = const.GAME_STATE_MENU


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = const.GAME_STATE_QUITTING

            pygame.display.update()

        return gamestate

    
    

if __name__ == "__main__":
    filePath = str(Path.cwd() / "HighScores" / "Scores.pickle")
    test = loadList(filePath)
    print(test)




    
    



    