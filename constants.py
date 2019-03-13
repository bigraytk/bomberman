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
TILE_BOSS_SPAWN   = 'L'

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
FRAMERATE = 60
SECOND = 1000  #1 second = 1000 milliseconds
PLAYER_DEATH_SCREEN_TIMER = 2      #death screen is shown for 2 seconds
BOMB_TIMER = 4
BOMB_EXPIDITE = 0.02#0.015
BOMB_FLASH_SPEED = 2 #lower is faster
BLAST_TIMER = 0.1
FADE_START = 255
SCREEN_OFFSET_X_LEFT = 32
SCREEN_OFFSET_Y_TOP = 64
SCREEN_OFFSET_X_RIGHT = 32
SCREEN_OFFSET_Y_BOTTOM = 32
HIT_BOX_OFFSET_X = 20
HIT_BOX_OFFSET_Y = 28
ICON_X = 32
ICON_Y = 20
ICON_SPACING = 70
ICON_SCALE = 40
SCORE_X = 860


# Enemy Constants
BASIC = 0
RANDOM = 1
ADVANCED = 2

SPEED_BOMB_KICKED = 5
SPEED_HIGH = 2.5
SPEED_MED = 2
SPEED_LOW = 1
ADVANCED_ENEMY_RANGE = 3    #how close an advanced enemy needs to be to player to persue

# Power Up Constants
POWERUP_RANGE = 0
POWERUP_COUNT = 1
POWERUP_BOOT = 2

#character constants
PC = 0
ENEMY = 1
BOSS = 2
GRID_MOVE_SCALE = 1
RES_MOVE_SCALE = 5
PLAYER_SPEED = 3
PLAYER_DEFAULT_NUM_BOMBS = 1  #number of starting bombs
PLAYER_ANIM_FRAMES = 4
PLAYER_ANIM_SPEED = 0.085
LIVES = 3
BOSS_HEALTH = 3


#character/bomb states
STATE_IDLE = 0
STATE_MOVING_UP = 1
STATE_MOVING_DOWN = 2
STATE_MOVING_LEFT = 3
STATE_MOVING_RIGHT = 4 
STATE_DEAD = 5
STATE_DYING = 6
STATE_PLAYER_WINS = 7

#bomb state
STATE_KICKED = 8
STATE_STOPPING = 9


#game states
GAME_STATE_RUNNING = 0
GAME_STATE_PAUSED = 1
GAME_STATE_MENU = 2
GAME_STATE_PLAYER_DEAD = 3
GAME_STATE_PLAYER_WINS = 4
GAME_STATE_QUITTING = 5
GAME_STATE_HIGHSCORES = 6


#direction constants
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3


#            R    G    B
BLACK    = (  0,   0,   0)
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
TRAN_COL = (255,   0, 255)

#Blast Constants
CENTER_FLAME = 0
RIGHT_FLAME = 1
LEFT_FLAME = 2
UP_FLAME = 3
DOWN_FLAME = 6
VERT_EXTENDER = 4
HOR_EXTENDER = 5
INITIAL_BOMB_TIMER = 0.5

#Score Constants
PLAYER_DIED = -10
ENEMY_DIED = 5
PICK_UP_POWER_UP = 10
BREAKABLE_WALL_DESTROYED = 20
LEVEL_CHANGE = 100
BOSS_DIED = 1000