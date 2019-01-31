
import constants as const
import Character
import Level
import pygame
import random
from pathlib import Path

class Bomb(pygame.sprite.Sprite):
    
    '''
    This is the Bomb class for the game

    '''

    def __init__(self, x, y, range):
        super().__init__()
        self.timer = const.BOMB_TIMER
        self.range = range  #range of blast
        self.x = x
        self.y = y
        self.xres = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        self.yres = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE

        imageFile = str(Path.cwd() / "graphics" / "bomb.png")
        self.image = pygame.image.load(imageFile).convert()
        self.image.set_colorkey(const.BLACK)
        self.blink = 255
        self.rect = self.image.get_rect()
        self.rect.x = self.xres
        self.rect.y = self.yres

        self.start_ticks = pygame.time.get_ticks() #starter tick
        self.exploded = False
        self.state = const.STATE_IDLE
        self.speed = const.SPEED_BOMB_KICKED
        

    def update(self, level):
        #self.rect.x = (const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE) + random.randint(-2, 2)   #make bomb shake
        #self.rect.y = (const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE) + random.randint(-2, 2)
        seconds = self.countdown()#calculate how many seconds
        if seconds > self.timer:
            self.exploded = True
        self.image.set_alpha(self.blink)
        if int(seconds * 10) % (const.BOMB_FLASH_SPEED * 2) < const.BOMB_FLASH_SPEED:
            self.blink = 100
        else:
            self.blink = 255

        # if bomb is moving because it was kicked
        if self.state != const.STATE_IDLE:
            xDest = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
            yDest = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE
            
            if self.state == const.STATE_MOVING_UP:
                if self.yres > yDest:
                    self.yres -= self.speed
                else:
                    self.yres = yDest
                    pathBlocked = self.move(const.UP, level)
                    if pathBlocked:
                        self.state = const.STATE_IDLE
                    
            if self.state == const.STATE_MOVING_DOWN:
                if self.yres < yDest:
                    self.yres += self.speed
                else:
                    self.yres = yDest
                    pathBlocked = self.move(const.DOWN, level)
                    if pathBlocked:
                        self.state = const.STATE_IDLE
                    
            if self.state == const.STATE_MOVING_LEFT:
                if self.xres > xDest:
                    self.xres -= self.speed
                else:
                    self.xres = xDest
                    pathBlocked = self.move(const.LEFT, level)
                    if pathBlocked:
                        self.state = const.STATE_IDLE
                    
            if self.state == const.STATE_MOVING_RIGHT:
                if self.xres < xDest:
                    self.xres += self.speed
                else:
                    self.xres = xDest
                    pathBlocked = self.move(const.RIGHT, level)
                    if pathBlocked:
                        self.state = const.STATE_IDLE
                    
            self.rect.x = self.xres
            self.rect.y = self.yres
 

    def countdown(self):
        return (pygame.time.get_ticks() - self.start_ticks) / const.SECOND 


    def explode(self, level, player):
        #explode centered at xpos and ypos, range of explosion equals self.blastSize
        #need to call animation for explosion, and initiate destroy checks on all
        #objects in range.
        #also needs to call the changeBombCount method from the PlayerCharacter class
        level.layout[self.y][self.x] = None
        player.changeActiveBombCount(-1)
        return level, player

    
    def expiditeExplosion(self):            #make bomb explode sooner, for chain reactions
        self.timer = self.countdown() + const.BOMB_EXPIDITE
    

    def kick(self, direction, level):
        #change either xpos or ypos based on direction, stop when hit another object
        self.move(direction, level)


    def move(self, direction, level):
        '''
        Moves bomb that has been kicked
        ''' 
        layout = level.layout
        pathBlocked = False
        

        if direction == const.UP:
            if self.y > 0 and layout[self.y - 1][self.x] == None:
                layout[self.y][self.x] = None
                self.y -= 1
                layout[self.y][self.x] = self
                self.state = const.STATE_MOVING_UP
            else:
                pathBlocked = True
        elif direction == const.DOWN:
            if self.y < const.MAP_HEIGHT - 1 and layout[self.y + 1][self.x] == None:
                layout[self.y][self.x] = None
                self.y += 1
                layout[self.y][self.x] = self
                self.state = const.STATE_MOVING_DOWN
            else:
                pathBlocked = True
        elif direction == const.LEFT:
            if self.x > 0 and layout[self.y][self.x - 1] == None:
                layout[self.y][self.x] = None
                self.x -= 1
                layout[self.y][self.x] = self
                self.state = const.STATE_MOVING_LEFT
            else:
                pathBlocked = True
        elif direction == const.RIGHT:
            if self.x < const.MAP_WIDTH - 1 and layout[self.y][self.x + 1] == None:
                layout[self.y][self.x] = None
                self.x += 1
                layout[self.y][self.x] = self
                self.state = const.STATE_MOVING_RIGHT
            else:
                pathBlocked = True

        return pathBlocked
    


class Blast (Bomb):

    def __init__(self, x, y, direction, tail, center = False):
        super().__init__(x,y,range)
        self.fade_out = 255
        if direction == const.CENTER_FLAME:
            imageFile = str(Path.cwd() / "graphics" / "flame_center.png")
        elif not tail:
            if direction == const.UP_FLAME or direction == const.DOWN_FLAME:
                imageFile = str(Path.cwd() / "graphics" / "flame_vert.png")
            if direction == const.LEFT_FLAME or direction == const.RIGHT_FLAME:
                imageFile = str(Path.cwd() / "graphics" / "flame_horiz.png")
        else:
            if direction == const.UP_FLAME:
                imageFile = str(Path.cwd() / "graphics" / "flame_up.png")
            elif direction == const.DOWN_FLAME:
                imageFile = str(Path.cwd() / "graphics" / "flame_down.png")
            elif direction == const.LEFT_FLAME:
                imageFile = str(Path.cwd() / "graphics" / "flame_left.png")
            elif direction == const.RIGHT_FLAME:
                imageFile = str(Path.cwd() / "graphics" / "flame_right.png")
        self.image = pygame.image.load(imageFile).convert()
        self.image.set_colorkey(const.BLACK)
        self.direction = direction
        self.timer = const.BLAST_TIMER


    def update(self):
        seconds = self.countdown() #calculate how many seconds
        if seconds > self.timer:
            self.kill()
        self.image.set_alpha(self.fade_out)
        self.fade_out -= 4


        

