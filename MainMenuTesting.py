import constants as const
import colors
import Level
import Wall
import Character
import random
from pathlib import Path
import pygame
import sys

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)


graphicsDir = Path.cwd() / "graphics"
pygame.init()


screenWidth = const.MAP_WIDTH * const.TILE_SIZE + const.SCREEN_OFFSET_X_LEFT + const.SCREEN_OFFSET_X_RIGHT
screenHeight = const.MAP_HEIGHT * const.TILE_SIZE + const.SCREEN_OFFSET_Y_TOP + const.SCREEN_OFFSET_Y_BOTTOM
screenSize = (screenWidth,screenHeight)
DISPLAYSURF = pygame.display.set_mode(screenSize)
DISPLAYSURF.fill(GRAY)
pygame.display.set_caption('BomberDude!')


MainMenuBanner = str(graphicsDir.joinpath("MainMenuTest.png"))
banner = pygame.image.load(MainMenuBanner)


NewGameButton = str(graphicsDir.joinpath("NewGameButton.png"))
newGameButt = pygame.image.load(NewGameButton)

NewGameButtonR = str(graphicsDir.joinpath("NewGameButton_Red.png"))
newGameButtRed = pygame.image.load(NewGameButtonR)


ngRect = pygame.Rect(500,200,200,50)
#NEW_SURF,   NEW_RECT   = makeText('New Game', CYAN, NAVYBLUE, screenWidth - 120, screenHeight - 60)


mousex = 0
mousey = 0


while True:
    mouseClicked = False
    DISPLAYSURF.blit(banner,(500,100))
    DISPLAYSURF.blit(newGameButt,(500,200))
    #pygame.draw.rect(DISPLAYSURF,RED,ngRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            '''
        elif event.type == pygame.MOUSEMOTION:
            mousex,mousey = event.pos
            if ngRect.collidepoint(mousex,mousey):
                DISPLAYSURF.blit(newGameButtRed,(500,200))
'''
        elif event.type == pygame.MOUSEBUTTONUP:
            mousex,mousey = event.pos
            print(mousex,mousey)
            if ngRect.collidepoint(mousex,mousey):
                print('You hit it!')
                DISPLAYSURF.blit(newGameButt,(500,300))
            
            
    pygame.display.update()


