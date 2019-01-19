# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:45:40 2019

@author: jkh02
"""

# Map values and parameters
TILE_WALL         = 'W'
TILE_BREAKABLE    = 'B'
TILE_BACKGROUND   = '0'
TILE_DOOR_HIDDEN  = 'D'
TILE_DOOR_CLOSED  = 'C'
TILE_DOOR_OPENED  = 'O'
TILE_PLAYER_START = 'P'
TILE_ENEMY_SPAWN  = 'E'

LEVEL_WIDTH       = 0
LEVEL_HEIGHT      = 1
LEVEL_BG_GFX      = 2
LEVEL_WALL_GFX    = 3
LEVEL_BREAK_GFX   = 4


# Map specifications
TILE_SIZE   = 64
MAP_WIDTH   = 17
MAP_HEIGHT  = 13


# Game specifications
FRAMERATE = 90
SECOND = 1000  #1 second = 1000 milliseconds
SCREEN_OFFSET_X_LEFT = 32
SCREEN_OFFSET_Y_TOP = 32
SCREEN_OFFSET_X_RIGHT = 32
SCREEN_OFFSET_Y_BOTTOM = 32

# Enemy Constants
BASIC = 0
RANDOM = 1
ADVANCED = 2
SMART = 3
HIGH = 4
MED = 5
LOW = 1

# Power Up Constants
RANGE = 0
COUNT = 1
BOOT = 2

#character constants
PC = 0
ENEMY = 1
GRID_MOVE_SCALE = 1
RES_MOVE_SCALE = 5
PLAYER_SPEED = 3

#character states
STATE_IDLE = 0
STATE_MOVING_UP = 1
STATE_MOVING_DOWN = 2
STATE_MOVING_LEFT = 3
STATE_MOVING_RIGHT = 4 
STATE_DEAD = 5

#direction constants
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3