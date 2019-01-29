
import constants as const
import Character
import Level
import pygame
from pathlib import Path

class Powerup(pygame.sprite.Sprite):

    '''
    This is the object for all powerups
    '''

    def __init__(self, powerupType, x, y):
        super().__init__()
        if powerupType != const.POWERUP_RANGE and powerupType != const.POWERUP_COUNT and powerupType != const.POWERUP_BOOT:
            raise RuntimeError(str(powerupType) + ' is not a valid kind of powerup')

        self.powerupType = powerupType
        self.x = x
        self.y = y
        self.resx = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        self.resy = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE

        imageFile = str(Path.cwd() / "graphics" / "powerup_range.png")
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.resx
        self.rect.y = self.resy


    def update(self):
        pass

    def pickUp(self):
        '''This method is called when a PC occupies the same space as a powerup.
        This returns the value of the powerup'''
        return self.powerupType
    
    def destroy(self):
        '''This method is called when a powerup would be destroyed for any reason'''
        pass
