import constants as const
import Level
import Wall
import Bomb
import random
import math
from pathlib import Path
import pygame


class Character(pygame.sprite.Sprite):

    '''
    This class encompasess all characters (Player and Enemy)
    PlayerCharacter and Emeny are subclasses
    '''

    def __init__(self, x, y, facing, speed, kind):
        '''Constructor'''
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.xres = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE #init this by running self.x through the grid_to_res conversion function
        self.yres = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE #same but for y
        self.speed = speed
        self.facing = facing
        self.kind = kind
        self.activeBombs = 0
        self.bombCount = 0
        self.bombRange = 0
        self.state = const.STATE_IDLE
        
        
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def xres(self):
        return self.__xres

    @property
    def yres(self):
        return self.__yres

    @property
    def speed(self):
        return self.__speed

    @property
    def facing(self):
        return self.__facing
    
    @property
    def kind(self):
        return self.__kind

    @property
    def activeBombs(self):
        return self.__activeBombs

    @property
    def bombCount(self):
        return self.__bombCount

    @property
    def bombRange(self):
        return self.__bombRange

    @property
    def state(self):
        return self.__state

    @x.setter
    def x(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__x = val

    @y.setter
    def y(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__y = val

    @xres.setter
    def xres(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__xres = val

    @yres.setter
    def yres(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__yres = val

    @speed.setter
    def speed(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__speed = val

    @facing.setter
    def facing(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__facing = val
    
    @kind.setter
    def kind(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__kind = val

    @activeBombs.setter
    def activeBombs(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__activeBombs = val

    @bombCount.setter
    def bombCount(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__bombCount = val

    @bombRange.setter
    def bombRange(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__bombRange = val

    @state.setter
    def state(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__state = val
         
    def move(self, direction, level):
        '''
        Controls movement of a character. Takes a direcetion as input, if character
        is able to move in that direction, will update the character's position and 
        facing. Else, will just update facing.
        -direction, specifies the direction the character should move
        -level, contains the object that allows for validation of colisions during character movement 
        ''' 
        layout = level.layout
        self.facing = direction
        pathBlocked = False
        

        if direction == const.UP:
            if self.y > 0 and not isinstance(layout[self.y - 1][self.x], Wall.Wall) and not isinstance(layout[self.y - 1][self.x], Bomb.Bomb) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_DOWN):
                self.y -= 1
                self.state = const.STATE_MOVING_UP
            else:
                pathBlocked = True
        elif direction == const.DOWN:
            if self.y < const.MAP_HEIGHT - 1 and not isinstance(layout[self.y + 1][self.x], Wall.Wall) and not isinstance(layout[self.y + 1][self.x], Bomb.Bomb) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_UP):
                self.y += 1
                self.state = const.STATE_MOVING_DOWN
            else:
                pathBlocked = True
        elif direction == const.LEFT:
            if self.x > 0 and not isinstance(layout[self.y][self.x - 1], Wall.Wall) and not isinstance(layout[self.y][self.x - 1], Bomb.Bomb) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_RIGHT):
                self.x -= 1
                self.state = const.STATE_MOVING_LEFT
            else:
                pathBlocked = True
        elif direction == const.RIGHT:
            if self.x < const.MAP_WIDTH - 1 and not isinstance(layout[self.y][self.x + 1], Wall.Wall) and not isinstance(layout[self.y][self.x + 1], Bomb.Bomb) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_LEFT):
                self.x += 1
                self.state = const.STATE_MOVING_RIGHT
            else:
                pathBlocked = True

        if self.kind == const.PC and not pathBlocked:
            self.changeDirection(direction)
        return pathBlocked
        
        
    def update(self, level, player):
        '''
        Updates character position when a character is moving towards a grid position
        -level
        '''
        if self.kind == const.ENEMY:
            if self.state == const.STATE_IDLE:
                if self.logic == const.RANDOM:
                    self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
                    self.move(self.direction, level)
                elif self.logic == const.BASIC:
                    pathBlocked = self.move(self.direction, level)
                    if pathBlocked or random.randint(0, 50) > 45:   #enemy walks until path blocked, or randomly decides to turn
                        self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
                        self.move(self.direction, level)
                elif self.logic == const.ADVANCED and player != None:
                    if abs(self.x - player.x) < const.ADVANCED_ENEMY_RANGE and abs(self.y - player.y) < const.ADVANCED_ENEMY_RANGE:
                        self.pursuePlayer = True
                        self.speed = const.SPEED_HIGH
                    if self.pursuePlayer:
                        self.advancedMovement(level, player)
                    else:
                        pathBlocked = self.move(self.direction, level)
                        if pathBlocked or random.randint(0, 50) > 45:   #enemy walks until path blocked, or randomly decides to turn
                            self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
                            self.move(self.direction, level)
            elif self.state == const.STATE_DYING:
                self.fade_out -= 8
                self.image.set_alpha(self.fade_out)
                if self.fade_out < 0:
                    self.kill()
        elif self.kind == const.BOSS:
            if self.state == const.STATE_IDLE:

                pathBlocked = self.move(self.direction, level)
                if pathBlocked or self.x > const.MAP_WIDTH - 5:
                    if self.direction == const.LEFT:
                        self.direction = const.RIGHT
                    else:
                        self.direction = const.LEFT

            if self.health <= 0:
                self.state = const.STATE_DYING
            if self.state == const.STATE_DYING:
                self.fade_out -= 4
                self.image.set_alpha(self.fade_out)
                if self.fade_out < 0:
                    self.kill()
                    player.state = const.STATE_PLAYER_WINS
            

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
            #self.changeDirection(self.facing)
            self.hitbox.x = self.rect.x + const.HIT_BOX_OFFSET_X - 2
            self.hitbox.y = self.rect.y + 4
            #self.rect.x += 0#8
            self.rect.y -= 8
        else:
            self.hitbox.x = self.rect.x + const.HIT_BOX_OFFSET_X / 2
            self.hitbox.y = self.rect.y + const.HIT_BOX_OFFSET_Y / 2


    def advancedMovement(self, level, player):
        ''' This method contains logic for advanced movement for enemy sprites idenfied as advanced
        -Level, contains a matrix to identify location of stationary objects
        -player, contains the current player object
        '''
        pathsBlocked = 0
        if self.x > player.x:
            self.direction = const.LEFT
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        elif self.x < player.x:
            self.direction = const.RIGHT
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        elif self.y > player.y:
            self.direction = const.UP
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        elif self.y < player.y:
            self.direction = const.DOWN
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        if pathsBlocked > 0 or self.direction == None:
            self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
            self.move(self.direction, level)


    def dropBomb(self, level):
        '''Creates an instance of the bomb class at the PC's position
        -level, contains matrix to identify location of stationary objects
        '''
        xDiff = abs(self.xres - (const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE))
        yDiff = abs(self.yres - (const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE))
        if self.kind == const.BOSS:
            isBoss = True
            offsetX = 1
            offsetY = 2
        else:
            isBoss = False
            offsetX = 0
            offsetY = 0
        if xDiff < 10 and yDiff < 10 and self.activeBombs < self.bombCount and level.layout[self.y][self.x] == None:
            newBomb = Bomb.Bomb(self.x + offsetX, self.y + offsetY, self.bombRange, isBoss)
            self.changeActiveBombCount(1)
            if isBoss:
                self.readyDropBomb = False
                self.startTicksBomb = pygame.time.get_ticks()
            return newBomb
        else:
            return None


    def changeActiveBombCount(self, change):
        '''This method is how to change the value of self.activeBombs
        will be called by dropBomb method of the PlayerCharacter, and
        the explode method of the Bomb
        -change, used to increment or decrement number of active bombs
        '''
        self.activeBombs = self.activeBombs + change
        if self.activeBombs < 0:
            self.activeBombs = 0
        if self.activeBombs > self.bombCount:
            self.activeBombs = self.bombCount


class PlayerCharacter(Character):
    '''
    This object is for the player's character. Only one
    should be instantiated.
    '''
    
    def __init__(self, level, x, y):
        '''Constructor'''
        facing = const.DOWN
        super().__init__(x, y, facing, const.PLAYER_SPEED, const.PC)
        self.bombCount = const.PLAYER_DEFAULT_NUM_BOMBS
        self.bombRange = 1
        self.boot = False
        self.lives = const.LIVES
        self.score = 0
        
       
        imageFile = str(Path.cwd() / "graphics" / "Left.png")
        self.left = pygame.image.load(imageFile).convert_alpha()

        imageFile = str(Path.cwd() / "graphics" / "Right.png")
        self.right = pygame.image.load(imageFile).convert_alpha()

        imageFile = str(Path.cwd() / "graphics" / "Front.png")
        self.front = pygame.image.load(imageFile).convert_alpha()

        imageFile = str(Path.cwd() / "graphics" / "Back.png")
        self.back = pygame.image.load(imageFile).convert_alpha()
    

        self.image = self.front


        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-const.HIT_BOX_OFFSET_X, -const.HIT_BOX_OFFSET_Y)

    def increaseScore(self,score):
        ''' This method increases/decreases the player's score dependent on the action taken by the player
        -score, value to be added to player's score
        '''
        self.score += score
        if self.score < 0:
            self.score = 0

    def move(self, direction, level):
        ''' This method implements movement unique to a player.  To be specific, whether or not a bomb should be kicked.
        -direction, based on the direction key the user selects
        -level, used to validate stationary objects on map
        '''
        layout = level.layout
        self.facing = direction
        pathBlocked = False

        #check for bomb to kick
        if self.boot:
            bomb = None
            if direction == const.UP and isinstance(layout[self.y - 1][self.x], Bomb.Bomb):
                bomb = layout[self.y - 1][self.x]
            if direction == const.DOWN and isinstance(layout[self.y + 1][self.x], Bomb.Bomb): 
                bomb = layout[self.y + 1][self.x]
            if direction == const.LEFT and isinstance(layout[self.y][self.x - 1], Bomb.Bomb): 
                bomb = layout[self.y][self.x - 1]
            if direction == const.RIGHT and isinstance(layout[self.y][self.x + 1], Bomb.Bomb): 
                bomb = layout[self.y][self.x + 1]
            if bomb and not bomb.bossBomb:
                bomb.kick(direction, level)
                
        #calls parent class' move function
        super().move(direction, level)


    def getPowerup(self, powerup):
        '''This method is called when the PC occupies the same space as a 
        powerup. 
        -powerup, type of powerup to provide the player
        '''
        if powerup.powerupType == const.POWERUP_RANGE and self.bombRange < 5:
            self.bombRange += 1
        elif powerup.powerupType == const.POWERUP_COUNT and self.bombCount < 5:
            self.bombCount += 1
        elif powerup.powerupType == const.POWERUP_BOOT:
            self.boot = True

    
    def changeDirection(self,direction):
        '''This method cnanges the direction of the player image
        -direction, used to decide what image to select.
        '''
        if direction == const.RIGHT and self.image != self.right:
            self.image = self.right
        if direction == const.LEFT and self.image != self.left: 
            self.image = self.left
        if direction == const.UP and self.image != self.back: 
            self.image = self.back
        if direction == const.DOWN and self.image != self.front:
            self.image = self.front

        
    


class Enemy(Character):
    '''
    This is the object for enemies. Many of them will be 
    instantiated at once. Version  allows the
    constructor to choose one of several attribute values
    '''

    def __init__(self, level, x, y):#version):
        '''Constructor'''
        facing = const.DOWN
        version = const.BASIC       #placeholder, maybe load enemy types from a list based on level #
        super().__init__(x, y, facing, 0, const.ENEMY)
        self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
        version = random.choice([const.BASIC, const.RANDOM, const.ADVANCED])
        self.pursuePlayer = False

        self.image = pygame.image.load(level.enemyFile).convert()
        self.image.set_colorkey(const.TRAN_COL)
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-const.HIT_BOX_OFFSET_X, -const.HIT_BOX_OFFSET_Y)
        self.fade_out = const.FADE_START
        
        if version == const.RANDOM: #BASIC is some value that we have not mapped yet
            self.speed = const.SPEED_LOW
            self.logic = const.RANDOM
        elif version == const.BASIC: 
            self.speed = const.SPEED_MED
            self.logic = const.BASIC
        elif version == const.ADVANCED:
            self.speed = const.SPEED_LOW    #advanced enemies start slow but speed up when in pursuit
            self.logic = const.ADVANCED

    
    def destroy(self):
        #gets called if something destroys an enemy
        self.state = const.STATE_DYING


class Boss(Character):
    def __init__(self, level, x, y):#version):
        '''Constructor'''
        facing = const.DOWN
        super().__init__(x, y, facing, 0, const.BOSS)
        self.yres += 5 #TODO constant
        self.direction = random.choice([const.LEFT, const.RIGHT])
        self.speed = const.SPEED_HIGH
        self.readyDropBomb = True
        self.timerBomb = 1.5  #TODO constant
        self.bombCount = 3  #TODO constant
        self.bombRange = max(level.levelHeight, level.levelWidth)
        self.startTicksBomb = 0
        self.timerTakeDamage = 3 #TODO constant
        self.canTakeDamage = True
        self.startTicksTakeDamage = 0

        graphicsDir = Path.cwd() / "graphics"

        imageFile = str(graphicsDir.joinpath("boss.png"))
        self.imageNormal = pygame.image.load(imageFile).convert()
        self.imageNormal.set_colorkey(const.TRAN_COL)
        self.image = self.imageNormal
        imageFile = str(graphicsDir.joinpath("boss_mouth_open.png"))
        self.imageMouth = pygame.image.load(imageFile).convert()
        self.imageMouth.set_colorkey(const.TRAN_COL)
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-const.HIT_BOX_OFFSET_X, -const.HIT_BOX_OFFSET_Y)

        imageFile = str(graphicsDir.joinpath("boss_damaged_1.png"))
        self.imageDamaged_1 = pygame.image.load(imageFile).convert()
        self.imageDamaged_1.set_colorkey(const.TRAN_COL)

        imageFile = str(graphicsDir.joinpath("boss_damaged_1_mouth_open.png"))
        self.imageMouthDamaged_1 = pygame.image.load(imageFile).convert()
        self.imageMouthDamaged_1.set_colorkey(const.TRAN_COL)

        imageFile = str(graphicsDir.joinpath("boss_damaged_2.png"))
        self.imageDamaged_2 = pygame.image.load(imageFile).convert()
        self.imageDamaged_2.set_colorkey(const.TRAN_COL)

        imageFile = str(graphicsDir.joinpath("boss_damaged_2_mouth_open.png"))
        self.imageMouthDamaged_2 = pygame.image.load(imageFile).convert()
        self.imageMouthDamaged_2.set_colorkey(const.TRAN_COL)

        imageFile = str(graphicsDir.joinpath("boss_dead.png"))
        self.imageDead = pygame.image.load(imageFile).convert()
        self.imageDead.set_colorkey(const.TRAN_COL)

        self.fade_out = const.FADE_START
        self.health = const.BOSS_HEALTH


    def update(self, level, player):
        super().update(level, player)

        seconds = self.countdownTakeDamage()#calculate how many seconds
        if seconds > self.timerTakeDamage:
            self.canTakeDamage = True

        seconds = self.countdownDropBomb()#calculate how many seconds
        if seconds > self.timerBomb and self.health > 0:
            self.readyDropBomb = True

        if self.readyDropBomb:
            self.image = self.imageMouth
        else:
            self.image = self.imageNormal
    
    
    def countdownDropBomb(self):
        return (pygame.time.get_ticks() - self.startTicksBomb) / const.SECOND


    def countdownTakeDamage(self):
        return (pygame.time.get_ticks() - self.startTicksTakeDamage) / const.SECOND 


    def takeDamage(self):
        if self.canTakeDamage:
            self.health -= 1
            self.canTakeDamage = False
            self.startTicksTakeDamage = pygame.time.get_ticks()

            if self.health == const.BOSS_HEALTH - 1:
                self.imageNormal = self.imageDamaged_1
                self.imageMouth = self.imageMouthDamaged_1
            elif self.health == const.BOSS_HEALTH - 2:
                self.imageNormal = self.imageDamaged_2
                self.imageMouth = self.imageMouthDamaged_2
            elif self.health <= 0:
                self.imageNormal = self.imageDead
                self.imageMouth = self.imageDead

        if self.health > 0:
            return False
        else:
            return True
