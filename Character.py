
import pygame
from pathlib import Path
import random
import Bomb
import Level
import Wall
import constants

class Character(object):

    '''
    This class encompasess all characters (Player and Enemy)
    PlayerCharacter and Emeny are subclasses
    '''

    def __init__(self, x, y, facing, speed, kind):
        '''Constructor'''

        self.x = x
        self.y = y
        self.xres = constants.SCREEN_OFFSET_X_LEFT + self.x * constants.TILE_SIZE#init this by running self.x through the grid_to_res conversion function
        self.yres = constants.SCREEN_OFFSET_Y_TOP + self.y * constants.TILE_SIZE#same but for y
        self.speed = speed
        self.facing = facing
        self.kind = kind
        self.state = constants.STATE_IDLE
        constants.TILE_WALL
        #if kind == constants.PC:
            #self.Player = self.PlayerCharacter()
        #elif kind == constants.ENEMY:
            #self.Enemy = self.Enemy()
        #else:
            #raise RuntimeError(kind + ' is not a valid kind of character')
        
        
    def move(self, direction, level):
        '''
        Controls movement of a character. Takes a direcetion as input, if character
        is able to move in that direction, will update the character's position and 
        facing. Else, will just update facing.
        ''' 
        layout = level.layout
        if constants.UP == direction:
            if self.y > 0 and not isinstance(layout[self.y - 1][self.x], Wall.Wall) and self.state == constants.STATE_IDLE:
                self.y -= 1
                self.state = constants.STATE_MOVING_UP
        elif constants.DOWN == direction:
            if self.y < constants.MAP_HEIGHT - 1 and not isinstance(layout[self.y + 1][self.x], Wall.Wall) and self.state == constants.STATE_IDLE:
                self.y += 1
                self.state = constants.STATE_MOVING_DOWN
        elif constants.LEFT == direction:
            if self.x > 0 and not isinstance(layout[self.y][self.x - 1], Wall.Wall) and self.state == constants.STATE_IDLE:
                self.x -= 1
                self.state = constants.STATE_MOVING_LEFT
        elif constants.RIGHT == direction:
            if self.x < constants.MAP_WIDTH - 1 and not isinstance(layout[self.y][self.x + 1], Wall.Wall) and self.state == constants.STATE_IDLE:
                self.x += 1
                self.state = constants.STATE_MOVING_RIGHT

        #checks if able to move in direction
        #if no, stays in same square, but update self.facing
        #if yes, move to correct square and update self.facing
        
        
    def updatePosition(self, level):
        '''
        Updates character position when a character is moving towards a grid position
        '''
        if self.kind == constants.ENEMY and self.state == constants.STATE_IDLE:
            if self.logic == constants.RANDOM:
                direction = random.choice([constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT])
                self.move(direction, level)
        
        xDest = constants.SCREEN_OFFSET_X_LEFT + self.x * constants.TILE_SIZE
        yDest = constants.SCREEN_OFFSET_Y_TOP + self.y * constants.TILE_SIZE
        
        if self.state == constants.STATE_MOVING_UP:
            if self.yres > yDest:
                self.yres -= self.speed
            else:
                self.yres = yDest
                self.state = constants.STATE_IDLE
                
        if self.state == constants.STATE_MOVING_DOWN:
            if self.yres < yDest:
                self.yres += self.speed
            else:
                self.yres = yDest
                self.state = constants.STATE_IDLE
                
        if self.state == constants.STATE_MOVING_LEFT:
            if self.xres > xDest:
                self.xres -= self.speed
            else:
                self.xres = xDest
                self.state = constants.STATE_IDLE
                
        if self.state == constants.STATE_MOVING_RIGHT:
            if self.xres < xDest:
                self.xres += self.speed
            else:
                self.xres = xDest
                self.state = constants.STATE_IDLE
                
        self.rect.x = self.xres
        self.rect.y = self.yres




class PlayerCharacter(Character):
    
    '''
    This object is for the player's character. Only one
    should be instantiated.
    '''
    
    def __init__(self, level):
        '''Constructor'''
        x = level.playerStartPosit[0]
        y = level.playerStartPosit[1]
        facing = constants.DOWN
        Character.__init__(self, x, y, facing, constants.PLAYER_SPEED, constants.PC)
        self.bombCount = 1
        self.bombRange = 1
        #self.speed = 40 #placeholder
        self.activeBombs = 0
        self.boot = False
        
        imageFile = str(Path.cwd() / "graphics" / "player.png")
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()

    def dropBomb(self):
        '''Creates an instance of the bomb class at the PC's position'''
        if self.activeBombs < self.bombCount:
            newBomb = Bomb.Bomb(self.bombRange, self.x, self.y)
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

    def __init__(self, level, i):#version):
        '''Constructor'''
        x = level.enemyStartPosit[i][0]
        y = level.enemyStartPosit[i][1]
        facing = constants.DOWN
        version = constants.BASIC       #placeholder, maybe load enemy types from a list based on level #
        Character.__init__(self, x, y, facing, 0, constants.ENEMY)
        
        imageFile = str(Path.cwd() / "graphics" / "enemy1.png")     #placeholder
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()
        
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