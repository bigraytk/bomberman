import constants as const
import Level
import Wall
import Bomb
import random
from pathlib import Path
import pygame


class Character(object):

    '''
    This class encompasess all characters (Player and Enemy)
    PlayerCharacter and Emeny are subclasses
    '''

    def __init__(self, x, y, facing, speed, kind):
        '''Constructor'''

        self.x = x
        self.y = y
        self.xres = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE#init this by running self.x through the grid_to_res conversion function
        self.yres = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE#same but for y
        self.speed = speed
        self.facing = facing
        self.kind = kind
        self.state = const.STATE_IDLE
        const.TILE_WALL
        #if kind == const.PC:
            #self.Player = self.PlayerCharacter()
        #elif kind == const.ENEMY:
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
        self.facing = direction
        pathBlocked = False
        
        if const.UP == direction:
            if self.y > 0 and not isinstance(layout[self.y - 1][self.x], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_DOWN):
                self.y -= 1
                self.state = const.STATE_MOVING_UP
            else:
                pathBlocked = True
        elif const.DOWN == direction:
            if self.y < const.MAP_HEIGHT - 1 and not isinstance(layout[self.y + 1][self.x], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_UP):
                self.y += 1
                self.state = const.STATE_MOVING_DOWN
            else:
                pathBlocked = True
        elif const.LEFT == direction:
            if self.x > 0 and not isinstance(layout[self.y][self.x - 1], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_RIGHT):
                self.x -= 1
                self.state = const.STATE_MOVING_LEFT
            else:
                pathBlocked = True
        elif const.RIGHT == direction:
            if self.x < const.MAP_WIDTH - 1 and not isinstance(layout[self.y][self.x + 1], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_LEFT):
                self.x += 1
                self.state = const.STATE_MOVING_RIGHT
            else:
                pathBlocked = True

        return pathBlocked

        #checks if able to move in direction
        #if no, stays in same square, but update self.facing
        #if yes, move to correct square and update self.facing
        
        
    def updatePosition(self, level):
        '''
        Updates character position when a character is moving towards a grid position
        '''
        if self.kind == const.ENEMY and self.state == const.STATE_IDLE:

            if self.logic == const.BASIC:
                pathBlocked = self.move(self.direction, level)
                if pathBlocked or random.randint(0, 50) > 45:   #enemy walks until path blocked, or randomly decides to turn
                    self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
                
        
        xDest = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        yDest = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE
        
        if self.state == const.STATE_MOVING_UP:
            if self.yres > yDest:
                self.yres -= self.speed
            else:
                self.yres = yDest
                self.state = const.STATE_IDLE
                
        if self.state == const.STATE_MOVING_DOWN:
            if self.yres < yDest:
                self.yres += self.speed
            else:
                self.yres = yDest
                self.state = const.STATE_IDLE
                
        if self.state == const.STATE_MOVING_LEFT:
            if self.xres > xDest:
                self.xres -= self.speed
            else:
                self.xres = xDest
                self.state = const.STATE_IDLE
                
        if self.state == const.STATE_MOVING_RIGHT:
            if self.xres < xDest:
                self.xres += self.speed
            else:
                self.xres = xDest
                self.state = const.STATE_IDLE
                
        self.rect.x = self.xres
        self.rect.y = self.yres
        
        #temporary means to handle the image size difference (from tilesize) for the bman image
        if self.kind == const.PC:
            self.rect.x += 8
            self.rect.y -= 16



class PlayerCharacter(Character):
    
    '''
    This object is for the player's character. Only one
    should be instantiated.
    '''
    
    def __init__(self, level):
        '''Constructor'''
        x = level.playerStartPosit[0]
        y = level.playerStartPosit[1]
        facing = const.DOWN
        Character.__init__(self, x, y, facing, const.PLAYER_SPEED, const.PC)
        self.bombCount = 1
        self.bombRange = 1
        #self.speed = 40 #placeholder
        self.activeBombs = 0
        self.boot = False
        
        imageFile = str(Path.cwd() / "graphics" / "player_bman.png")
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()

        self.deathSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "yell.wav"))

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
        if powerup == const.RANGE and self.bombRange < 5:
            self.bombRange += 1
        elif powerup == const.COUNT and self.bombCount < 5:
            self.bombCount += 1
        elif powerup == const.BOOT:
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
        facing = const.DOWN
        version = const.BASIC       #placeholder, maybe load enemy types from a list based on level #
        Character.__init__(self, x, y, facing, 0, const.ENEMY)
        self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])

        imageFile = str(Path.cwd() / "graphics" / "enemy1.png")     #placeholder
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()
        
        if version == const.RANDOM: #BASIC is some value that we have not mapped yet
            self.speed = const.SPEED_LOW
            self.logic = const.RANDOM
        elif version == const.BASIC: 
            self.speed = const.SPEED_MED
            self.logic = const.BASIC
        elif version == const.ADVANCED:
            self.speed = const.SPEED_HIGH
            self.logic = const.SMART
        

    def destroy(self):
        #gets called if something destroys an enemy
        pass