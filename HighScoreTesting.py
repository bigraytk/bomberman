from pathlib import Path


def makeBlankScores():
    blankArray = []
    for i in range(10):
        blankArray.append('---0')
    #print(blankArray)
    return blankArray

def tokenizer(text):
    '''Takes the text of the HighScore file and converts it to an array.'''
    scoreList = []
    textList = []
    nameTarget = ''
    scoreTarget = ''
    textLength = len(text)
    #turn the string into a list
    for i in range(textLength):
        textList.append(text[i])

    item = textList.pop(0)
    #print('1: ' , item)
    #iterate through list until all elements have been popped off
    while(item != False):
        nameTarget = item
        for i in range(2):            
            nameTarget = nameTarget + textList.pop(0)
        item = textList.pop(0)
        #print('2: ' ,item)
        scoreTarget = ''
        try:
            isnum = int(item)
            isnum = True
        except:
            isnum = False
        while (isnum == True and item != False):
            #print('top of number while loop')
            scoreTarget = scoreTarget + item
            try:
                item = textList.pop(0)
                try:
                    isnum = int(item)
                    isnum = True
                except:
                    isnum = False
            except:
                item = False
            #print('3: ' , item)
        
        scoreList.append((nameTarget,int(scoreTarget)))

    return scoreList


def writeScores(scoreList,filepath):
    '''writes the scoreList to the file given in filepath'''
    scoreFile = open(filePath,'w')
    scoreString = ''
    for element in scoreList:
        scoreString = scoreString + str(element[0]) + str(element[1])

    print(scoreString)

    for letter in scoreString:
        scoreFile.write(letter)
    
    scoreFile.close()


def newScore(scoreList,newEntry):
    '''Compares newEntry to scoreList, and insterts it into the correct spot, or ignores it.
    Returns the updated (or not) scoreList'''
    newNum = newEntry[1]
    for i in range(10):
        if newNum > scoreList[i][1]:
            print(newNum , ' is greater than ' ,scoreList[i][1])
            scoreList.insert(i,newEntry)
            scoreList.pop()
            print(scoreList)
            return scoreList
    return scoreList

    




    

    
    


filePath = str(Path.cwd() / "HighScores" / "Scores.txt")
'''
scoreFile = open(filePath,'w')
blankList = makeBlankScores()
for element in blankList:
    scoreFile.write(element)

scoreFile.close()
'''
scoreFile = open(filePath,'r')
scoreString = scoreFile.read()
print(scoreString)

ans = tokenizer(scoreString)
entry = ('JLW',100)

updatedList = newScore(ans,entry)
scoreFile.close()


writeScores(ans,filePath)















