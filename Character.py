
import Bomb
import level
import Wall
import constants

class Character(object):

    '''
    This class encompasess all characters (Player and Enemy)
    PlayerCharacter and Emeny are subclasses
    '''

    def __init__(self,x,y,facing,kind):
        '''Constructor'''

        self.x = x
        self.y = y
        self.xres = x#init this by running self.x through the grid_to_res conversion function
        self.yres = y#same but for y
        self.facing = facing
        constants.TILE_WALL
        if kind == constants.PC:
            self.Player = self.PlayerCharacter()
        elif kind == constants.ENEMY:
            self.Enemy = self.Enemy()
        else:
            raise RuntimeError(kind + ' is not a valid kind of character')


    def move(self,direction,layout):
        '''
        Controls movement of a character. Takes a direcetion as input, if character
        is able to move in that direction, will update the character's position and 
        facing. Else, will just update facing.
        ''' 
        if constants.UP == direction:
            if (self.y - constants.GRID_MOVE_SCALE) >= 0 and (not isinstance(layout[self.x][self.y - constants.GRID_MOVE_SCALE], Wall)):
                self.y -= constants.GRID_MOVE_SCALE

        elif constants.DOWN == direction:
            if (self.y + constants.GRID_MOVE_SCALE) <= constants.MAP_HEIGHT and (not isinstance(layout[self.x][self.y + constants.GRID_MOVE_SCALE], Wall)):
                self.y += constants.GRID_MOVE_SCALE
        
        elif constants.LEFT == direction:
            if (self.x - constants.GRID_MOVE_SCALE) >= 0 and (not isinstance(layout[self.x - constants.GRID_MOVE_SCALE][self.y], Wall)):
                self.x -= constants.GRID_MOVE_SCALE

        elif constants.RIGHT == direction:
            if (self.x + constants.GRID_MOVE_SCALE) <= constants.MAP_HEIGHT and (not isinstance(layout[self.x + constants.GRID_MOVE_SCALE][self.y], Wall)):
                self.x += constants.GRID_MOVE_SCALE

        #checks if able to move in direction
        #if no, stays in same square, but update self.facing
        #if yes, move to correct square and update self.facing


    class PlayerCharacter(Character):
        
        '''
        This object is for the player's character. Only one
        should be instantiated.
        '''
        
        def __init__(self):
            '''Constructor'''
            Character.__init__(self)
            self.bombCount = 1
            self.bombRange = 1
            self.speed = 40 #placeholder
            self.activeBombs = 0
            self.boot = False

        def dropBomb(self):
            '''Creates an instance of the bomb class at the PC's position'''
            if self.activeBombs < self.bombCount:
                newBomb = Bomb.Bomb(self.bombRange,self.x,self.y)
                self.changeBombCount(1)

        def changeBombCount(self,change):
            '''This method is how to change the value of self.activeBombs
            will be called by dropBomb method of the PlayerCharacter, and
            the explode method of the Bomb
            '''
            self.activeBombs = self.activeBombs + change

        def getPowerup(self,powerup):
            '''This method is called when the PC occupies the same space as a 
            powerup. 
            '''
            if powerup == constants.RANGE and self.bombRange < 5:
                self.bombRange += 1
            elif powerup == constants.COUNT and self.bombCount < 5:
                self.bombCount += 1
            elif powerup == constants.BOOT:
                self.boot = True


    class Enemy(Character):

        '''
        This is the object for enemies. Many of them will be 
        instantiated at once. Version  allows the
        constructor to choose one of several attribute values
        '''

        def __init__(self,version):
            '''Constructor'''
            Character.__init__(self)
            if version == constants.BASIC: #BASIC is some value that we have not mapped yet
                self.speed = constants.LOW
                self.logic = constants.RANDOM
            elif version == constants.MED: 
                self.speed = constants.LOW
                self.logic = constants.BASIC
            elif version == constants.ADVANCED:
                self.speed = constants.HIGH
                self.logic = constants.SMART
            

        def destroy(self):
            #gets called if something destroys an enemy
            pass