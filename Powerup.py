
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

        self.powerupType = powerupType
        self.x = x
        self.y = y
        self.resx = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        self.resy = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE

        if self.powerupType == const.POWERUP_RANGE:
            imageFile = str(Path.cwd() / "graphics" / "powerup_range.png")
        elif self.powerupType == const.POWERUP_COUNT:
            imageFile = str(Path.cwd() / "graphics" / "powerup_count.png")
        elif self.powerupType == const.POWERUP_BOOT:
            imageFile = str(Path.cwd() / "graphics" / "powerup_boot.png")
        else:
            raise RuntimeError(str(powerupType) + ' is not a valid kind of powerup')

        try:
            self.image = pygame.image.load(imageFile).convert()
            self.image.set_colorkey(const.TRAN_COL)
            self.rect = self.image.get_rect()
            self.rect.x = self.resx
            self.rect.y = self.resy
            self.fade = const.FADE_START
            self.fadeIncrease = False
            self.fadeSpeed = 6
            self.fadeMinimum = 120
        except:
            raise RuntimeError('Error: Unable to load graphics files')

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
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def fade(self):
        return self.__fade

    @property
    def fadeIncrease(self):
        return self.__fadeIncrease

    @property
    def fadeSpeed(self):
        return self.__fadeSpeed

    @property
    def fadeMinimum(self):
        return self.__fadeMinimum

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

    @image.setter
    def image(self,val):
        if val == None:
            raise RuntimeError('Invalid assignment')
        else:
            self.__image = val

    @rect.setter
    def rect(self,val):
        if val == None:
            raise RuntimeError('Invalid assignment')
        else:
            self.__rect = val

    @fade.setter
    def fade(self,val):
        if val < 0:
            raise RuntimeError('Invalid assignment')
        else:
            self.__fade = val

    @fadeIncrease.setter
    def fadeIncrease(self,val):
        if isinstance(val,bool):
            self.__fadeIncrease = val
        else:
            raise RuntimeError('Invalid assignment')
            

    @fadeSpeed.setter
    def fadeSpeed(self,val):
        if val < 0:
            raise RuntimeError('Invalid assignment')
        else:
            self.__fadeSpeed = val

    @fadeMinimum.setter
    def fadeMinimum(self,val):
        if val < 0:
            raise RuntimeError('Invalid assignment')
        else:
            self.__fadeMinimum = val

    def update(self):
        if self.fadeIncrease:
            self.fade += self.fadeSpeed
        else:
            self.fade -= self.fadeSpeed
        if self.fade > const.FADE_START:
            self.fade = const.FADE_START
            self.fadeIncrease = False
        if self.fade < self.fadeMinimum:
            self.fade = self.fadeMinimum
            self.fadeIncrease = True
            
        self.image.set_alpha(self.fade)

    def pickUp(self, player):
        '''This method is called when a PC occupies the same space as a powerup.
        This returns the value of the powerup'''
        return self.powerupType
    
    def destroy(self):
        '''This method is called when a powerup would be destroyed for any reason'''
        pass
