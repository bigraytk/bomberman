# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:45:40 2019

@author: 
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
LEVEL_ENEMY_GFX   = 5


# Map specifications
TILE_SIZE   = 64
MAP_WIDTH   = 17
MAP_HEIGHT  = 13


# Game specifications
FRAMERATE = 90
SECOND = 1000  #1 second = 1000 milliseconds
PLAYER_DEATH_SCREEN_TIMER = 1.5      #death screen is shown for 1.5 seconds
SCREEN_OFFSET_X_LEFT = 32
SCREEN_OFFSET_Y_TOP = 64
SCREEN_OFFSET_X_RIGHT = 32
SCREEN_OFFSET_Y_BOTTOM = 32
HIT_BOX_OFFSET_X = 20
HIT_BOX_OFFSET_Y = 28


# Enemy Constants
BASIC = 0
RANDOM = 1
ADVANCED = 2
#SMART = 3      # < do we need this?  We can just use ADVANCED for the type and logic
SPEED_HIGH = 2.5
SPEED_MED = 2
SPEED_LOW = 1
ADVANCED_ENEMY_RANGE = 3    #how close an advanced enemy needs to be to player to persue

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


#game states
GAME_STATE_RUNNING = 0
GAME_STATE_PAUSED = 1
GAME_STATE_MENU = 2
GAME_STATE_PLAYER_DEAD = 3
GAME_STATE_QUITTING = 4

#direction constants
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3


#            R    G    B
GREY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)