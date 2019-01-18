
import Bomb

class Character(object):

    '''
    This class encompasess all characters (Player and Enemy)
    PlayerCharacter and Emeny are subclasses
    '''

    class PlayerCharacter(object):

        '''
        This object is for the player's character. Only one
        should be instantiated.
        '''
        
        def __init__(self):
            '''Constructor'''
            self.bombCount = 1
            self.bombRange = 1
            self.speed = 40 #placeholder
            self.activeBombs = 0
            self.boot = False

        def dropBomb():
            '''Creates an instance of the bomb class at the PC's position'''
            if self.activeBombs < self.bombCount:
                newBomb = Bomb.Bomb(self.bombRange,self.x,self.y)
                self.changeBombCount(1)

        def changeBombCount(change):
            '''This method is how to change the value of self.activeBombs
            will be called by dropBomb method of the PlayerCharacter, and
            the explode method of the Bomb
            '''
            self.activeBombs = self.activeBombs + change

        def getPowerup(powerup):
            '''This method is called when the PC occupies the same space as a 
            powerup. 
            '''
            if powerup == RANGE and self.bombRange < 5:
                self.bombRange += 1
            elif powerup == COUNT and self.bombCount < 5:
                self.bombCount += 1
            elif powerup == BOOT:
                self.boot = True


    class Enemy(object):

        '''
        This is the object for enemies. Many of them will be 
        instantiated at once. Version  allows the
        constructor to choose one of several attribute values
        '''

        def __init__(self,version):
            '''Constructor'''
            if version == BASIC: #BASIC is some value that we have not mapped yet
                self.speed = LOW
                self.logic = RANDOM
            elif version == MED: 
                self.speed = LOW
                self.logic = BASIC:
            elif version == ADVANCED:
                self.speed = HIGH
                self.logic = SMART
            

        def destroy():
            #gets called if something destroys an enemy
            #


    def __init__(self,x,y,facing,kind):
        '''Constructor'''

        self.x = x
        self.y = y
        self.xres = #init this by running self.x through the grid_to_res conversion function
        self.yres = #same but for y
        self.facing = facing
        if kind == PC:
            self.Player = self.PlayerCharacter()
        elif kind == ENEMY:
            self.Enemy = self.Enemy()
        else:
            raise RuntimeError(kind + ' is not a valid kind of character')


    def move(self,direction):
        '''
        Controls movement of a character. Takes a direcetion as input, if character
        is able to move in that direction, will update the character's position and 
        facing. Else, will just update facing.
        ''' 
        #checks if able to move in direction
        #if no, stays in same square, but update self.facing
        #if yes, move to correct square and update self.facing

