

class Door(object):

    '''
    This is the Door object
    '''

    def __init__(self,x,y):
        self.open = False
        self.x = x
        self.y = y
        checkIfOpen()

    def checkIfOpen(self):
        '''This method is called when the door is created, it must 
        be able too look at the list of active enemies, if it is 
        empty, then open the door.
        ''' 
        numEnemyLeft = #not sure how to do this yet
        if numEnemyLeft == 0:
            openDoor()

    def openDoor(self):
        '''This method is called either from the main game loop or
        from checkIfOpen.
        '''
        self.open = True
    
    def nextLevel(self):
        '''This method is called when the self.open = True and the PC
        attempts to move into the space of the door. This method then 
        starts the process to end the current level and load the next one
        '''