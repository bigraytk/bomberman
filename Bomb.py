
import constants as const
import Character
import Level
import pygame
from pathlib import Path

class Bomb(pygame.sprite.Sprite):
    
    '''
    This is the Bomb class for the game

    '''

    def __init__(self, x, y, range):
        super().__init__()
        self.timer = 4
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
        seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
        if seconds > self.timer:
            self.exploded = True

    def countdown(self):
        #need to countdown starting at self.time to 0
        # once at 0, call explode

        pass

    def explode(self, level, player):
        #explode centered at xpos and ypos, range of explosion equals self.blastSize
        #need to call animation for explosion, and initiate destroy checks on all
        #objects in range.
        #also needs to call the changeBombCount method from the PlayerCharacter class
        level.layout[self.y][self.x] = None
        player.changeActiveBombCount(-1)
        return level, player

    
    def kicked(self,direction):
        #change either xpos or ypos based on direction, stop when hit another object
        pass
    
class Blast (Bomb):

    def __init__(self, x, y, range, imageFile, direction):
        super().__init__(x,y,range)
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.direction = direction

        

