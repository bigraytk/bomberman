# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 08:09:12 2019

@author: jkh02
"""

from constants import *
import level #from level import *
import Wall
import colors
import pygame, sys
import random
pygame.init()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
gameRunning = True

screen_width = MAP_WIDTH * TILE_SIZE + SCREEN_OFFSET_X_LEFT + SCREEN_OFFSET_X_RIGHT
screen_height = MAP_HEIGHT * TILE_SIZE + SCREEN_OFFSET_Y_TOP + SCREEN_OFFSET_Y_BOTTOM
size = screen_width, screen_height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BomberDude")





def drawLevel(level):
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            screen.blit(level.backgroundImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
            try:
                if isinstance(level.layout[row][column], Wall.Wall) and not level.layout[row][column].breakable:#TILE_WALL:
                    screen.blit(level.wallImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
                #if level.layout[row][column] == TILE_BREAKABLE:
                if isinstance(level.layout[row][column], Wall.Wall) and level.layout[row][column].breakable:
                    screen.blit(level.breakableImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
                #if level.layout[row][column] == TILE_DOOR_HIDDEN:
                    #screen.blit(level.breakableImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
                if level.layout[row][column] == TILE_DOOR_OPENED:
                    screen.blit(level.doorOpenedImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
                if level.layout[row][column] == TILE_DOOR_CLOSED:
                    screen.blit(level.doorClosedImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
            except:
                print("Index out of range error")
                
    

################## Testing ########################## Testing ################# vvvvvv
player_speed = 5
ball2 = pygame.image.load("test2.png").convert_alpha()
ballrect2 = ball2.get_rect()

def userInput():
    key=pygame.key.get_pressed()
    if key[pygame.K_UP]:
        ballrect2[1] -= player_speed
    if key[pygame.K_DOWN]:
        ballrect2[1] += player_speed
    if key[pygame.K_LEFT]:
        ballrect2[0] -= player_speed
    if key[pygame.K_RIGHT]:
        ballrect2[0] += player_speed  
                
def render():
    screen.blit(ball2, ballrect2)                
                
ball = []#pygame.image.load("intro_ball.gif").convert_alpha()
speed = []
num_balls = 0#300
ballrect = []
for i in range(num_balls):
    #ball.append( pygame.image.load("intro_ball.gif").convert_alpha() )
    ball.append( pygame.image.load("test2.png").convert_alpha() )
    ballrect.append(ball[i].get_rect())
    ballrect[i].x = random.randint(0, 800) 
    ballrect[i].y = random.randint(1, 800)
    speed.append( [random.randint(2, 8), random.randint(2, 4)] )

def ball_test():
    for i in range(num_balls):
        screen.blit(ball[i], ballrect[i])#(ball_x, ball_y))
        ballrect[i] = ballrect[i].move(speed[i])
        if ballrect[i].left < 0 or ballrect[i].right > screen_width:
            speed[i][0] = -speed[i][0]
        if ballrect[i].top < 0 or ballrect[i].bottom > screen_height:
            speed[i][1] = -speed[i][1]
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fps, (25, 25))
################## Testing ########################## Testing ################# ^^^^^

current_level = level.Level(1)
while gameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameRunning = False
                if event.key == pygame.K_z:
                    current_level.show_door()
                if event.key == pygame.K_x:
                    current_level.open_door()


    drawLevel(current_level)
    ball_test()     ## Testing ##
    userInput()
    render()

    pygame.display.update()
    screen.fill(colors.Black)
    clock.tick(FRAMERATE)

pygame.quit()
exit()