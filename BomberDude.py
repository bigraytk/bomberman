# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 08:09:12 2019

@author:

Main program
"""

import Game
from LinkedList import *

game = Game.Game()

while game.gameRunning:
    game.update()
