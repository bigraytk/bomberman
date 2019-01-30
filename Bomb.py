
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
        self.resx = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        self.resy = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE

        imageFile = str(Path.cwd() / "graphics" / "bomb.png")
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.resx
        self.rect.y = self.resy

        self.start_ticks = pygame.time.get_ticks() #starter tick
        self.exploded = False
        

    def update(self):
        self.rect.x = (const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE) + random.randint(-2, 2)   #make bomb shake
        self.rect.y = (const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE) + random.randint(-2, 2)
        seconds = self.countdown()#calculate how many seconds
        if seconds > self.timer:
            self.exploded = True


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

        
    def kicked(self,direction):
        #change either xpos or ypos based on direction, stop when hit another object
        pass
    


class Blast (Bomb):

    def __init__(self, x, y, direction, tail, center = False):
        super().__init__(x,y,range)
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
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.direction = direction
        self.timer = const.BLAST_TIMER


    def update(self):
        seconds = self.countdown() #calculate how many seconds
        if seconds > self.timer:
            self.kill()
        


        

