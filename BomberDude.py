# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 08:09:12 2019

@author: 
"""

import constants as const
import colors
import Level
import Wall
import Character
import random
from pathlib import Path
import pygame, sys

pygame.init()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
gameRunning = True

screenWidth = const.MAP_WIDTH * const.TILE_SIZE + const.SCREEN_OFFSET_X_LEFT + const.SCREEN_OFFSET_X_RIGHT
screenHeight = const.MAP_HEIGHT * const.TILE_SIZE + const.SCREEN_OFFSET_Y_TOP + const.SCREEN_OFFSET_Y_BOTTOM
screenSize = screenWidth, screenHeight
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("BomberDude")



def startLevel(num):
    level = Level.Level(num)
    player = Character.PlayerCharacter(level)
    enemies = []
    for i in range(level.numEnemies):
        enemies.append(Character.Enemy(level, i))
    
    return (level, player, enemies)



def drawLevel(level):
    for row in range(const.MAP_HEIGHT):
        for column in range(const.MAP_WIDTH):
            drawTile(level.backgroundImage, column, row)
            try:
                if isinstance(level.layout[row][column], Wall.Wall) and not level.layout[row][column].breakable:
                    drawTile(level.wallImage, column, row)
                    #screen.blit(level.wallImage, (const.SCREEN_OFFSET_X_LEFT + column * const.TILE_SIZE, const.SCREEN_OFFSET_Y_TOP + row * const.TILE_SIZE))
                if isinstance(level.layout[row][column], Wall.Wall) and level.layout[row][column].breakable:
                    drawTile(level.breakableImage, column, row)
                    #screen.blit(level.breakableImage, (const.SCREEN_OFFSET_X_LEFT + column*  const.TILE_SIZE, const.SCREEN_OFFSET_Y_TOP + row * const.TILE_SIZE))
                if level.layout[row][column] == const.TILE_DOOR_OPENED:
                    drawTile(level.doorOpenedImage, column, row)
                    #screen.blit(level.doorOpenedImage, (const.SCREEN_OFFSET_X_LEFT + column * const.TILE_SIZE, const.SCREEN_OFFSET_Y_TOP + row * const.TILE_SIZE))
                if level.layout[row][column] == const.TILE_DOOR_CLOSED:
                    drawTile(level.doorClosedImage, column, row)
                    #screen.blit(level.doorClosedImage, (const.SCREEN_OFFSET_X_LEFT + column * const.TILE_SIZE, const.SCREEN_OFFSET_Y_TOP + row * const.TILE_SIZE))
            except:
                print("Index out of range error")



def drawTile(image, x, y):
    xres = const.SCREEN_OFFSET_X_LEFT + x * const.TILE_SIZE
    yres = const.SCREEN_OFFSET_Y_TOP + y * const.TILE_SIZE
    screen.blit(image, (xres, yres))
        #const.SCREEN_OFFSET_X_LEFT + column * const.TILE_SIZE, const.SCREEN_OFFSET_Y_TOP + row * const.TILE_SIZE))
                
    

################## Testing ########################## Testing ################# vvvvvv
imageFile = str(Path.cwd() / "graphics" / "death_temp.png")     #placeholder
death_test_image = pygame.image.load(imageFile).convert_alpha()
death_test_rect = death_test_image.get_rect()
death_test_rect.x = int(screenWidth / 2 - death_test_rect.width / 2)
death_test_rect.y = int(screenHeight / 2 - death_test_rect.height / 2)

def checkCollision(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

def userInput(player):
    key=pygame.key.get_pressed()
    if key[pygame.K_UP]:
        player.move(const.UP, currentLevel)
    if key[pygame.K_DOWN]:
        player.move(const.DOWN, currentLevel)
    if key[pygame.K_LEFT]:
        player.move(const.LEFT, currentLevel)
    if key[pygame.K_RIGHT]:
        player.move(const.RIGHT, currentLevel)
                
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
        if checkCollision(enemies[i].xres, enemies[i].yres, const.TILE_SIZE-8, const.TILE_SIZE-8, player.xres, player.yres, const.TILE_SIZE-8, const.TILE_SIZE-8):
            screen.blit(death_test_image, death_test_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            player.state = const.STATE_DEAD

    text1 = str(int(clock.get_fps()))
    fps = font.render(text1, True, pygame.Color('white'))
    screen.blit(fps, (25, 25))
################## Testing ########################## Testing ################# ^^^^^


currentLevelNum = 1
currentLevel, player, enemies = startLevel(currentLevelNum)


while gameRunning:
    if player.state == const.STATE_DEAD:
        currentLevel, player, enemies = startLevel(currentLevelNum)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameRunning = False
                if event.key == pygame.K_z:
                    currentLevel.showDoor()
                if event.key == pygame.K_x:
                    currentLevel.openDoor()
                if event.key == pygame.K_f:
                    if screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode(screenSize)
                    else:
                        pygame.display.set_mode(screenSize, pygame.FULLSCREEN)

    #drawLevel(currentLevel)
    userInput(player)
    #player.updatePosition()

    #for i in range (numEnemies):
    #    enemy[i].updatePosition(currentLevel)
    render(currentLevel, player, enemies)

    pygame.display.update()
    screen.fill(colors.Black)
    clock.tick(const.FRAMERATE)

pygame.display.quit()
pygame.quit()
#exit()