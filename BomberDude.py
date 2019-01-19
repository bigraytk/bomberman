# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 08:09:12 2019

@author: jkh02
"""

from constants import *
import Level #from level import *
import Wall
import Character
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
                if isinstance(level.layout[row][column], Wall.Wall) and not level.layout[row][column].breakable:
                    screen.blit(level.wallImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
                if isinstance(level.layout[row][column], Wall.Wall) and level.layout[row][column].breakable:
                    screen.blit(level.breakableImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
                if level.layout[row][column] == TILE_DOOR_OPENED:
                    screen.blit(level.doorOpenedImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
                if level.layout[row][column] == TILE_DOOR_CLOSED:
                    screen.blit(level.doorClosedImage, (SCREEN_OFFSET_X_LEFT + column*TILE_SIZE, SCREEN_OFFSET_Y_TOP + row*TILE_SIZE))
            except:
                print("Index out of range error")
                
    

################## Testing ########################## Testing ################# vvvvvv


def userInput():
    key=pygame.key.get_pressed()
    if key[pygame.K_UP]:
        player.move(UP, current_level)
    if key[pygame.K_DOWN]:
        player.move(DOWN, current_level)
    if key[pygame.K_LEFT]:
        player.move(LEFT, current_level)
    if key[pygame.K_RIGHT]:
        player.move(RIGHT, current_level)
                
def render():
    playerRect.x = player.xres
    playerRect.y = player.yres
    screen.blit(playerImage, playerRect)             
                

    text1 = str(int(clock.get_fps()))
    fps = font.render(text1, True, pygame.Color('white'))
    screen.blit(fps, (25, 25))
################## Testing ########################## Testing ################# ^^^^^



player_speed = 3
playerImage = pygame.image.load("test2.png").convert_alpha()
playerRect = playerImage.get_rect()

current_level = Level.Level(1)
player = Character.PlayerCharacter(current_level.playerStartPosit[0], current_level.playerStartPosit[1], DOWN, player_speed)

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
    userInput()
    player.updatePosition()

    #for i in range (numEnemies):
    #    enemy[i].updatePosition(current_level)
    render()

    pygame.display.update()
    screen.fill(colors.Black)
    clock.tick(FRAMERATE)

pygame.quit()
exit()