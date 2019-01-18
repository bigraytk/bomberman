

class Bomb(object):
    
    '''
    This is the Bomb class for the game

    '''

    def __init__(self,size,x,y):
        self.timer = 4
        self.blastSize = size
        self.xpos = x
        self.ypos = y
        countdow():
        

    def countdown(self):
        #need to countdown starting at self.time to 0
        # once at 0, call explode

    def explode(self):
        #explode centered at xpos and ypos, range of explosion equals self.blastSize
        #need to call animation for explosion, and initiate destroy checks on all
        #objects in range
    
    def kicked(self,direction):
        #change either xpos or ypos based on direction, stop when hit another object
        

