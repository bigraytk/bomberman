
#How to transition from the high scores to the main menu and back?
import InputBox
from pathlib import Path
import constants as const
from LinkedList import *



class HighScore(object):

    def __init__(self, screen, screenWidth, screenHeight):
        '''Constructor'''
        self.screen = screen
        

        self.filePath = str(Path.cwd() / "HighScores" / "Scores.pickle")

        graphicsDir = Path.cwd() / "graphics"


        #unpickle the file into the tree
        self.scoreList = loadList(self.filePath)

        #sets up the display / buttons
        self.screen.fill(const.GREY)
        #TODO

        
    def newScore(self,value):
        '''checks to see if the passed value is a high score. If it is, will update the scoreTree and ask 
        for user input for the name.'''
        #check data structure to see where the new score goes
        smallestScore = self.scoreTree.smallestScore()
        if value > smallestScore:


            #have user input initials to go with the score
            fontSize = 32
            inputBox = InputBox.InputBox(self.screen, 320, 240, 58, 32, fontSize, const.GREY, const.GREEN)
            newName = InputBox.run()

            #add the newName and the score to the data structure
            

    def display(self):
        '''Displays the high scores and manages the buttons to return to the main menu'''
        pass

    
    

if __name__ == "__main__":
    filePath = str(Path.cwd() / "HighScores" / "Scores.pickle")
    test = loadList(filePath)
    print(test)




    
    



    