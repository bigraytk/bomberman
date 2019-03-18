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
    This class encompasess all characters (Player, Enemy and Boss)
    PlayerCharacter, Emeny and Boss are subclasses
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
        -level, used to verify level layout to prevent movement into walls
        -player, used to get player information for enemies who persue the player (advanced movement)
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
            self.hitbox.x = self.rect.x + const.HIT_BOX_OFFSET_X - 2
            self.hitbox.y = self.rect.y + 4
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
        self.imageIndex = 0
        self.imageFrame  = [None] * const.PLAYER_ANIM_FRAMES
        self.start_ticks = pygame.time.get_ticks() #starter tick

        try:
            self.left = []
            imageFile = str(Path.cwd() / "graphics" / "Left.png")
            image1 = pygame.image.load(imageFile).convert_alpha()
            imageFile = str(Path.cwd() / "graphics" / "Left2.png")
            image2 = pygame.image.load(imageFile).convert_alpha()
            self.left.extend([image1, image2, image1, image2])

            self.right = []
            imageFile = str(Path.cwd() / "graphics" / "Right.png")
            image1 = pygame.image.load(imageFile).convert_alpha()
            imageFile = str(Path.cwd() / "graphics" / "Right2.png")
            image2 = pygame.image.load(imageFile).convert_alpha()
            self.right.extend([image1, image2, image1, image2])

            self.up = []
            imageFile = str(Path.cwd() / "graphics" / "Up.png")
            image1 = pygame.image.load(imageFile).convert_alpha()
            imageFile = str(Path.cwd() / "graphics" / "Up2.png")
            image2 = pygame.image.load(imageFile).convert_alpha()
            imageFile = str(Path.cwd() / "graphics" / "Up3.png")
            image3 = pygame.image.load(imageFile).convert_alpha()
            self.up.extend([image1, image2, image1, image3])
            
            self.down = []
            imageFile = str(Path.cwd() / "graphics" / "Down.png")
            image1 = pygame.image.load(imageFile).convert_alpha()
            imageFile = str(Path.cwd() / "graphics" / "Down2.png")
            image2 = pygame.image.load(imageFile).convert_alpha()
            imageFile = str(Path.cwd() / "graphics" / "Down3.png")
            image3 = pygame.image.load(imageFile).convert_alpha()
            self.down.extend([image1, image2, image1, image3])
        except:
            raise RuntimeError('Error: Unable to load graphics files')
    
        self.changeDirection(facing)
        self.image = self.imageFrame[0]

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(-const.HIT_BOX_OFFSET_X, -const.HIT_BOX_OFFSET_Y)

    @property
    def score(self):
        return self.__score

    @property
    def lives(self):
        return self.__lives

    @property
    def down(self):
        return self.__down

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right
    
    @property
    def up(self):
        return self.__up
    
    @property
    def image(self):
        return self.__image

    @property
    def imageIndex(self):
        return self.__imageIndex
    
    @property
    def imageFrame(self):
        return self.__imageFrame

    @property
    def start_ticks(self):
        return self.__start_ticks

    @score.setter
    def score(self, val):
        if val < 0:
            val = 0
        self.__score = val
    
    @lives.setter
    def lives(self, val):
        if val < 0:
            raise RuntimeError('Lives cannot be less than 0')
        self.__lives = val
    
    @image.setter
    def image(self, val):
        if val == None:
            raise RuntimeError('Image Cannot Equal None')
        self.__image = val

    @down.setter
    def down(self, val):
        if val == None:
            raise RuntimeError('Image Cannot Equal None')
        self.__down = val

    @left.setter
    def left(self, val):
        if val == None:
            raise RuntimeError('Image Cannot Equal None')
        self.__left = val

    @right.setter
    def right(self, val):
        if val == None:
            raise RuntimeError('Image Cannot Equal None')
        self.__right = val

    @up.setter
    def up(self, val):
        if val == None:
            raise RuntimeError('Image Cannot Equal None')
        self.__up = val

    @imageIndex.setter
    def imageIndex(self, val):
        if val < 0:
            raise RuntimeError('Image index cannot be less than 0')
        self.__imageIndex = val
    
    @imageFrame.setter
    def imageFrame(self, val):
        if val == None:
            raise RuntimeError('ImageFrame Cannot Equal None')
        self.__imageFrame = val

    @start_ticks.setter
    def start_ticks(self, val):
        if val < 0:
            raise RuntimeError('Start Ticks cannot be less than 0')
        self.__start_ticks = val



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
        if powerup.powerupType == const.POWERUP_RANGE and self.bombRange < const.POWERUP_MAX:
            self.bombRange += 1
        elif powerup.powerupType == const.POWERUP_COUNT and self.bombCount < const.POWERUP_MAX:
            self.bombCount += 1
        elif powerup.powerupType == const.POWERUP_BOOT:
            self.boot = True

    
    def changeDirection(self,direction):
        '''This method cnanges the direction of the player image
        -direction, used to decide what image to select.
        '''
        if direction == const.RIGHT:
            for i in range(len(self.right)):
                self.imageFrame[i] = self.right[i]
        
        if direction == const.LEFT:
            for i in range(len(self.left)):
                self.imageFrame[i] = self.left[i]

        if direction == const.UP:
            for i in range(len(self.up)):
                self.imageFrame[i] = self.up[i]
        
        if direction == const.DOWN:
            for i in range(len(self.down)):
                self.imageFrame[i] = self.down[i]


    def update(self, level, player):
        '''Used to update player image frame, for animating walk cycle
        - level, required for parent update method
        - player, required for parent update method
        '''
        super().update(level, player)
        if self.state == const.STATE_IDLE:
            self.image = self.imageFrame[0]
        else:
            self.image = self.imageFrame[self.imageIndex]

        checkTimer = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND
        if  checkTimer > const.PLAYER_ANIM_SPEED or self.state == const.STATE_IDLE:
            self.start_ticks = pygame.time.get_ticks()
            self.imageIndex += 1

            if self.imageIndex >= const.PLAYER_ANIM_FRAMES:
                self.imageIndex = 0



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

        try:
            self.image = pygame.image.load(str(level.enemyFile)).convert()
        except:
           raise RuntimeError('Error: Unable to load graphics files')

        self.image.set_colorkey(const.TRAN_COL)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
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

    @property
    def direction(self):
        return self.__direction

    @property
    def pursuePlayer(self):
        return self.__pursuePlayer

    @property
    def speed(self):
        return self.__speed

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, val):
        if val < 0 :
            raise RuntimeError('Incorrect Speed')
        self.__version = val

    @speed.setter
    def speed(self, val):
        if val < 0 :
            raise RuntimeError('Incorrect Speed')
        self.__speed = val

    @direction.setter
    def direction(self, val):
        if val != const.UP and val != const.DOWN and val != const.RIGHT and val != const.UP and val != const.LEFT :
            raise RuntimeError('Incorrect Direction Val')
        self.__direction = val

    @pursuePlayer.setter
    def pursuePlayer(self, val):
        if val != False and val != True:
            raise RuntimeError('Not Boolean')
        self.__pursuePlayer = val

    def destroy(self):
        '''Used to manage the state of a dead enemy
        '''
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
        try:
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
        except:
            raise RuntimeError('Error: Unable to load graphics files')

        self.mask = pygame.mask.from_surface(self.image)
        
        self.fade_out = const.FADE_START
        self.health = const.BOSS_HEALTH

    @property
    def speed(self):
        return self.__speed

    @property
    def readyDropBomb(self):
        return self.__readyDropBomb

    @property
    def timerBomb(self):
        return self.__timerBomb
    
    @property
    def startTicksBomb(self):
        return self.__startTicksBomb
    
    @property
    def timerTakeDamage(self):
        return self.__timerTakeDamage

    @property
    def canTakeDamage(self):
        return self.__canTakeDamage
    
    @property
    def startTicksTakeDamage(self):
        return self.__startTicksTakeDamage

    @speed.setter
    def speed(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__speed = val

    @readyDropBomb.setter
    def readyDropBomb(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__readyDropBomb = val
        
    @timerBomb.setter
    def timerBomb(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__timerBomb = val

    @startTicksBomb.setter
    def startTicksBomb(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__startTicksBomb = val

    @timerTakeDamage.setter
    def timerTakeDamage(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__timerTakeDamage = val
    
    @canTakeDamage.setter
    def canTakeDamage(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__canTakeDamage = val

    @startTicksTakeDamage.setter
    def startTicksTakeDamage(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__startTicksTakeDamage = val

    def update(self, level, player):
        '''Used to manage timing for when the boss drops a bomb and how he takes damage.
        - level, required for parent update method
        - player, required for parent update method
        '''
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
        '''Used to manage when the boss drops a bomb
        '''
        return (pygame.time.get_ticks() - self.startTicksBomb) / const.SECOND


    def countdownTakeDamage(self):
        '''Used to manage timer for damage
        '''
        return (pygame.time.get_ticks() - self.startTicksTakeDamage) / const.SECOND 


    def takeDamage(self):
        '''Used to manage when a boss character takes damage
        '''
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
