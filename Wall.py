


class Wall(object):

    '''Wall class

    This class is the wall for the game. When creating must pass (breakable,power,door).
    breakable and door are type bool, power is int in range 0-3. 
    '''

    def __init__(self,breakable,power,door):
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

    def destroy(self):
        '''This method is called to check if a wall would be destryoed by an explosion.
        will return False if no, True if yes. 
        If the wall contained a powerup or door this method will instantiate an object 
        of that class
        '''
        if self.breakable == False:
            return False
        if self.powerup != 0:
            #create powerup object, pass number contained in self.power
            pass
        elif self.door == True:
            #create a door object
            pass
        return True

if __name__ == '__main__':
    myWall = Wall(False,0,True)
    print('breakable: ' ,myWall.breakable)
    print('power: ' , myWall.powerup)
    print('door: ' , myWall.door)
        
