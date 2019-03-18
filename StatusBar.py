
import constants as const
import Character
import Level
import pygame
from pathlib import Path

class StatusBar(object):

    '''
    This is the object for all powerups
    '''

    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.resx = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        self.resy = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE

        self.spriteIcon = pygame.sprite.Group()

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
    def spriteIcon(self):
        return self.__spriteIcon

    @spriteIcon.setter
    def spriteIcon(self, val):
        if val == None:
            raise RuntimeError('Invalid Assignment')
        self.__spriteIcon = val

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

    
    def addIcon(self, imageFileName, iconNum, alpha, scale = const.ICON_SCALE):
        x = const.ICON_X + const.ICON_SPACING * iconNum
        y = const.ICON_Y
        newIcon = Icon(imageFileName, x, y, scale, alpha)
        self.spriteIcon.add(newIcon)


    def getIconSpriteGroup(self):
        return self.spriteIcon


    def getIconX(self, iconNum):
        return const.ICON_X + const.ICON_SPACING * iconNum


class Icon(pygame.sprite.Sprite):
    '''
    This class encompasess all icons that
    can appear on the status bar
    '''
    def __init__(self, imageFileName, x, y, scale, alpha):
        '''Constructor'''
        pygame.sprite.Sprite.__init__(self)

        try:
            imageFile = str(Path.cwd() / "graphics" / imageFileName)
            if alpha:
                self.image = pygame.image.load(imageFile).convert_alpha()
            else:
                self.image = pygame.image.load(imageFile).convert()
                self.image.set_colorkey(const.TRAN_COL)
            self.image = pygame.transform.scale(self.image, (scale, scale))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        except:
            raise RuntimeError('Error: Unable to load graphics files')