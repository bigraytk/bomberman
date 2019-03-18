
import Level
import Powerup
import constants as const
import random

class Wall(object):
    '''Wall class
    This class is the wall for the game. When creating must pass (breakable,power,door).
    breakable and door are type bool, power is int in range 0-3. 
    '''

    def __init__(self, breakable, power, x, y, door = False):
        '''Constructor
        breakable must be bool.
        power must be 0,1,2,3.
        door must be bool.
        '''
        if not isinstance(breakable,bool):
            raise RuntimeError(str(breakable) + ' is not a bool, cannot set breakabiltiy to this value')
        if power != 0 and power != 1 and power != 2 and power != 3:
            raise RuntimeError(str(power) + ' is not a valid value for power property')
        if not isinstance(door,bool):
            raise RuntimeError(str(door) + ' is not a bool, cannot set door to this value')
        if ((door == True) and (power != 0)):
            raise RuntimeError('Wall cannot contain door and powerup')
        self.breakable = breakable
        self.powerup = power
        self.door = door
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
    
    @property
    def powerup(self):
        return self.__powerup


    @x.setter
    def x(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__x = val

    @y.setter
    def y(self, val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__y = val
    
    @powerup.setter
    def powerup(self,val):
        if val < 0:
            raise RuntimeError('Value is less than 0')
        self.__powerup = val


    def destroy(self, level):
        '''This method is called to check if a wall would be destroyed by an explosion,
        and destroy it if so.  Will return None for no powerup, otherwise return powerup.
        If the wall contained a powerup or door this method will instantiate an object 
        of that class
        - level, this is userd to handle actions modifying a breakable wall
        '''
        if self.breakable:
            if self.door == True:
                #create a door object
                level.layout[self.y][self.x] = const.TILE_DOOR_CLOSED
            else:
                level.layout[self.y][self.x] = None
                if random.randint(0, 10) > 4:
                    powerupType = random.choice([const.POWERUP_RANGE, const.POWERUP_COUNT, const.POWERUP_BOOT])  #TODO uncomment
                    newPowerup = Powerup.Powerup(powerupType, self.x, self.y)     #TODO change parameter to random powerup
                    return newPowerup
        return None

        
