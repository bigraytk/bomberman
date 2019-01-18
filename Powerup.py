

class Powerup(object):

    '''
    This is the object for all powerups
    '''

    def __init__(self,kind):
        if kind != RANGE and kind != COUNT and kind != BOOT:
            raise RuntimeError(str(kind) + ' is not a valid kind of powerup')

        self.kind = kind

    def pickUp(self):
        '''This method is called when a PC occupies the same space as a powerup.
        This returns the value of the powerup'''
        return self.kind
    
    def destroy(self):
        '''This method is called when a powerup would be destroyed for any reason'''
        pass
