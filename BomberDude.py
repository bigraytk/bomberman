# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 08:09:12 2019

@author: jkh02
"""

from constants import *
from pathlib import Path
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



def startLevel(num):
    level = Level.Level(num)
    player = Character.PlayerCharacter(level)
    enemies = []
    for i in range(level.numEnemies):
        enemies.append(Character.Enemy(level, i))
    
    return (level, player, enemies)



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
imageFile = str(Path.cwd() / "graphics" / "death_temp.png")     #placeholder
death_test_image = pygame.image.load(imageFile).convert_alpha()
death_test_rect = death_test_image.get_rect()
death_test_rect.x = int(screen_width / 2 - death_test_rect.width / 2)
death_test_rect.y = int(screen_height / 2 - death_test_rect.height / 2)

def checkCollision(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

def userInput(player):
    key=pygame.key.get_pressed()
    if key[pygame.K_UP]:
        player.move(UP, current_level)
    if key[pygame.K_DOWN]:
        player.move(DOWN, current_level)
    if key[pygame.K_LEFT]:
        player.move(LEFT, current_level)
    if key[pygame.K_RIGHT]:
        player.move(RIGHT, current_level)
                
def render(level, player, enemies):
    #Render level
    drawLevel(level)
    
    #Render player
    player.updatePosition(level)
    screen.blit(player.image, player.rect)
    
    #Render enemies
    for i in range(level.numEnemies):
        enemies[i].updatePosition(level)
        screen.blit(enemies[i].image, enemies[i].rect)
        
        #placeholder for proper handling of collision detection
        if checkCollision(enemies[i].xres, enemies[i].yres, TILE_SIZE-8, TILE_SIZE-8, player.xres, player.yres, TILE_SIZE-8, TILE_SIZE-8):
            screen.blit(death_test_image, death_test_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            player.state = STATE_DEAD

    text1 = str(int(clock.get_fps()))
    fps = font.render(text1, True, pygame.Color('white'))
    screen.blit(fps, (25, 25))
################## Testing ########################## Testing ################# ^^^^^


current_level_num = 1
current_level, player, enemies = startLevel(current_level_num)


while gameRunning:
    if player.state == STATE_DEAD:
        current_level, player, enemies = startLevel(current_level_num)
        
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

    #drawLevel(current_level)
    userInput(player)
    #player.updatePosition()

    #for i in range (numEnemies):
    #    enemy[i].updatePosition(current_level)
    render(current_level, player, enemies)

    pygame.display.update()
    screen.fill(colors.Black)
    clock.tick(FRAMERATE)

pygame.display.quit()
pygame.quit()
#exit()