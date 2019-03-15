"""
Created on Fri Jan 11 08:09:12 2019

@author: 
"""
#import sys
import constants as const
import colors
import Level
import Wall
import Character
import Bomb
import Powerup
import MainMenu
import StatusBar
import HighScore
import random
from pathlib import Path
import pygame


class Game(object):

    '''
    This is the game object.  It manages the various states of the game while running.
    '''
    def __init__(self):

        #Game states, tells the game what code to run depending on the current state
        self.states = {const.GAME_STATE_MENU : self.stateMainMenu,
          const.GAME_STATE_RUNNING           : self.stateGameRunning,
          const.GAME_STATE_PLAYER_DEAD       : self.statePlayerDead,
          const.GAME_STATE_PLAYER_WINS       : self.statePlayerWins,
          const.GAME_STATE_QUITTING          : self.stateQuitting,
          const.GAME_STATE_HIGHSCORES        : self.stateHighScores}

        #Initialize pygame
        pygame.init()

        #Setup music and sound
        self.musicFile = str(Path.cwd() / "sounds" / "music1.mp3")
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(self.musicFile)

        self.explodeSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "bomb.wav"))
        self.deathSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "yell.wav"))
        self.bossDieSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "boss_no.wav"))

        #Setup misc pygame settings such as clock for timers and font for text
        self.clock = pygame.time.Clock()
        self.start_ticks = 0
        self.font = pygame.font.Font(None, 30)

        #Setup game progression booleans
        self.gameRunning = True
        self.gameOver = False
        self.playerWins = False
        self.exitingToMenu = False
        self.musicOn = True
        self.soundOn = True

        #Makes game start in main menu
        self.gameState = const.GAME_STATE_MENU

        #Setup screen parameters and the pygame window
        self.screenWidth = const.MAP_WIDTH * const.TILE_SIZE + const.SCREEN_OFFSET_X_LEFT + const.SCREEN_OFFSET_X_RIGHT
        self.screenHeight = const.MAP_HEIGHT * const.TILE_SIZE + const.SCREEN_OFFSET_Y_TOP + const.SCREEN_OFFSET_Y_BOTTOM
        self.screenSize = self.screenWidth, self.screenHeight
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("BomberDude")
        self.screenImage = pygame.Surface(self.screenSize)    #used to store the screen to an image, useful for semi-transparent screens 

        #Setup the MainMenu and High scores Screen
        self.theMainMenu = MainMenu.MainMenu(self.screen, self.screenWidth, self.screenHeight)
        self.highScores = HighScore.HighScore(self.screen, self.screenWidth, self.screenHeight)

        #Load starting level
        self.levelNum = 1
        self.level, self.player, self.enemies, self.boss = Level.startNewLevel(self.levelNum)

        #Retreive total number of levels stored in data directory, requires levels to be numbered sequentially
        self.numLevels = 0
        dataDir = Path.cwd() / "data"
        for f in dataDir.glob("level*.csv"):
            self.numLevels += 1

        #Create sprite groups for all game sprite objects
        self.spritePlayer = pygame.sprite.Group()
        self.spritePlayer.add(self.player)
        self.spriteEnemies = pygame.sprite.Group()
        self.spriteEnemies.add(self.enemies)
        self.spriteBombs = pygame.sprite.Group()
        self.spriteBombBlasts = pygame.sprite.Group()
        self.spriteBossBombBlasts = pygame.sprite.Group()
        self.spritePowerups = pygame.sprite.Group()

        #Create status bar for displaying player information at top of screen
        self.statusBar = StatusBar.StatusBar(0, 0)
        self.statusBar.addIcon("Down.png", 0, True)
        self.statusBar.addIcon("powerup_boot.png", 2, False, const.ICON_SCALE + 5)  #This is offset because the graphic is a little smaller than the icons
        self.statusBar.addIcon("powerup_range.png", 3, False)
        self.statusBar.addIcon("powerup_count.png", 4, False)

        #Player death screen
        imageFile = str(Path.cwd() / "graphics" / "death_screen.png")
        self.death_test_image = pygame.image.load(imageFile).convert_alpha()
        self.death_test_rect = self.death_test_image.get_rect()
        self.death_test_rect.x = int(self.screenWidth / 2 - self.death_test_rect.width / 2)
        self.death_test_rect.y = int(self.screenHeight / 2 - self.death_test_rect.height / 2)

        #Game over screen image
        imageFile = str(Path.cwd() / "graphics" / "game_over_screen.png")    
        self.gameOverImage = pygame.image.load(imageFile).convert_alpha()

        #Player win screen image
        imageFile = str(Path.cwd() / "graphics" / "you_win_screen.png")
        self.playerWinsImage = pygame.image.load(imageFile).convert_alpha()

        #Screen border image
        imageFile = str(Path.cwd() / "graphics" / "border.png")
        self.borderImage = pygame.image.load(imageFile).convert()

        #Debug mode allows cheats, only for developer use
        self.__debugMode = True


    def render(self):

        '''
        Handles drawing and updating all spritegroups, to include movement and interaction 
         between spritegroups.  Handles death of enemies and players, bomb explosions, wall
         destruction, and powerup pickups since all are spritegroup-based interation.
        ''' 

        #Render level
        self.screen.blit(self.borderImage, (0, 0))
        self.drawStatusBar()
        self.drawLevel()
        
        #Update and render enemies
        self.spriteEnemies.update(self.level, self.player)
        self.spriteEnemies.draw(self.screen)

        #Update and render bombs, blasts, and powerups
        self.spriteBombs.update(self.level)
        self.spriteBombs.draw(self.screen)

        self.spriteBombBlasts.update()
        self.spriteBombBlasts.draw(self.screen)

        self.spriteBossBombBlasts.update()
        self.spriteBossBombBlasts.draw(self.screen)

        self.spritePowerups.update()
        self.spritePowerups.draw(self.screen)

        #Update and render player
        self.spritePlayer.update(self.level, self.player)
        self.spritePlayer.draw(self.screen)

        #Check collisions between enemies and players (kill player) / bomb blasts (kill enemy)
        for enemy in self.spriteEnemies:
            if enemy.rect.colliderect(self.player.hitbox) and enemy.state != const.STATE_DYING:
                if pygame.sprite.spritecollide(enemy, self.spritePlayer, False, pygame.sprite.collide_mask):
                    self.killPlayer()
            if pygame.sprite.spritecollide(enemy, self.spriteBombBlasts, False, pygame.sprite.collide_mask):
                if enemy.kind == const.BOSS:
                    if enemy.takeDamage():
                      self.player.increaseScore(const.ENEMY_DIED)
                      if self.soundOn:
                          self.bossDieSound.play()
                else:
                    enemy.destroy()
                    self.player.increaseScore(const.ENEMY_DIED)

        #Check if any enemies left, open door if all enemies gone
        if not self.spriteEnemies:
            self.level.openDoor()

        #Kill player if hit by bomb blast
        for blast in self.spriteBombBlasts:
            if blast.rect.colliderect(self.player.hitbox) and blast.fade_out > const.FADE_START / 2:
                self.killPlayer()

        for blast in self.spriteBossBombBlasts:
            if blast.rect.colliderect(self.player.hitbox) and blast.fade_out > const.FADE_START / 2:
                self.killPlayer()

        #Handle bomb collision with enemies or other bombs when kicked, and handle bomb explosions
        for bomb in self.spriteBombs:
            for enemy in self.spriteEnemies:
                if bomb.state == const.STATE_MOVING_UP and bomb.y == enemy.y +1 and bomb.x == enemy.x:
                    bomb.collision = True
                if bomb.state == const.STATE_MOVING_DOWN and bomb.y == enemy.y - 1 and bomb.x == enemy.x:
                    bomb.collision = True
                if bomb.state == const.STATE_MOVING_LEFT and bomb.y == enemy.y and bomb.x == enemy.x + 1:
                    bomb.collision = True
                if bomb.state == const.STATE_MOVING_RIGHT and bomb.y == enemy.y and bomb.x == enemy.x - 1:
                    bomb.collision = True
            if pygame.sprite.spritecollideany(bomb, self.spriteBombBlasts, collided = None) or pygame.sprite.spritecollideany(bomb, self.spriteBossBombBlasts, collided = None):
                bomb.expiditeExplosion()
            if bomb.exploded:
                if self.soundOn:
                    self.explodeSound.play()
                if not bomb.bossBomb:
                    powerups, blasts = self.level.destroyWalls(bomb.x, bomb.y, self.level, bomb.range)
                    self.spritePowerups.add(powerups)
                    self.spriteBombBlasts.add(blasts)
                    self.level, self.player = bomb.explode(self.level, self.player)
                else:
                    powerups, blasts = self.level.destroyWalls(bomb.x, bomb.y, self.level, bomb.range)
                    self.spriteBossBombBlasts.add(blasts)
                    self.level, self.boss = bomb.explode(self.level, self.boss)
                bomb.kill()

        #Handle player collision with powerup (player collects up powerup on collision)
        for powerup in self.spritePowerups:
            if powerup.rect.colliderect(self.player.hitbox):
                self.player.getPowerup(powerup)
                self.player.increaseScore(const.PICK_UP_POWER_UP)
                powerup.kill()


    def drawStatusBar(self):

        '''
        Draws the status bar on screen.  The status bar shows player information such as
         lives, powerups held, and score.
        ''' 

        self.statusBar.getIconSpriteGroup().draw(self.screen)

        textY = const.ICON_Y + const.ICON_TEXT_Y_OFFSET
        textXOffset = const.ICON_SCALE
        
        #Text for Player Lives Count, active bombs, boot powerup, bomb range, bomb count, and score
        self.drawText('x'+str(self.player.lives), self.statusBar.getIconX(0) + textXOffset, textY, const.YELLOW)
        self.drawText('x' + str(int(self.player.boot)), self.statusBar.getIconX(2) + textXOffset, textY, const.YELLOW)
        self.drawText('x'+ str(self.player.bombRange), self.statusBar.getIconX(3) + textXOffset, textY, const.YELLOW)
        self.drawText('x'+ str(self.player.bombCount), self.statusBar.getIconX(4) + textXOffset, textY, const.YELLOW)
        self.drawText('Score: '+str(self.player.score), const.SCORE_X, textY, const.YELLOW)


    def drawText(self, text, x, y, color):

        '''
        Draws text to the screen
        -text, contains the text to display on screen
        -x, x location where to draw text
        -y, y location where to draw text
        -color, color to use when drawing text
        ''' 
        
        textSurface = self.font.render(text, True, color)
        self.screen.blit(textSurface, (x, y))

    
    def drawLevel(self):

        '''
        Draws all of the tiles onscreen from the current level, to include background, walls,
         breakable walls, and the door
        ''' 

        for row in range(const.MAP_HEIGHT):
            for column in range(const.MAP_WIDTH):   
                self.drawTile(self.level.backgroundImage, column, row)
                try:
                    if isinstance(self.level.layout[row][column], Wall.Wall) and not self.level.layout[row][column].breakable:
                        self.drawTile(self.level.wallImage, column, row)
                    if isinstance(self.level.layout[row][column], Wall.Wall) and self.level.layout[row][column].breakable:
                        self.drawTile(self.level.breakableImage, column, row)
                    if self.level.layout[row][column] == const.TILE_DOOR_OPENED:
                        self.drawTile(self.level.doorOpenedImage, column, row)
                    if self.level.layout[row][column] == const.TILE_DOOR_CLOSED:
                        self.drawTile(self.level.doorClosedImage, column, row)
                except:
                    print("Index out of range error")


    def drawTile(self, image, x, y):

        '''
        Converts the x and y value of each tile based on its location in
         the map grid into x and y coordinates on screen.
        -image, contains the image for the tile being drawn on screen
        -x, the x value based on the tile's index location in the map
        -y, the y value based on the tile's index location in the map
        ''' 

        xres = const.SCREEN_OFFSET_X_LEFT + x * const.TILE_SIZE
        yres = const.SCREEN_OFFSET_Y_TOP + y * const.TILE_SIZE
        self.screen.blit(image, (xres, yres))


    def updateBoss(self):
        
        '''
        Tells the boss to drop and kick a bomb down the screen when ready.
        ''' 

        if self.boss.readyDropBomb:
            newBomb = self.boss.dropBomb(self.level)
            if newBomb:
                self.level.layout[newBomb.y][newBomb.x] = newBomb
                self.spriteBombs.add(newBomb)
                newBomb.kick(const.DOWN, self.level)
    

    def update(self):

        '''
        Updates the state of the game, handles state transitions, 
         and updates the screen.
        ''' 

        #Keeps the music playing if it is turned on.
        if self.musicOn:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        if self.level.bossLevel:
            self.updateBoss()

        #Get user input from the player
        self.getUserInput()

        #Handles switching game states by calling gamestate fucntions from a dictionary
        self.gameState = self.states[self.gameState]()

        #Update the screen
        pygame.display.update()
        self.screen.fill(colors.Black)
        self.clock.tick(const.FRAMERATE)

        #Make sure game finishes cycles before quitting
        if self.gameState == const.GAME_STATE_QUITTING:
            self.quitGame()


    def stateGameRunning(self):

        '''
        Game state for when the game is being played.
        ''' 

        self.render()
        newState = self.checkPlayerProgress()

        return newState


    def statePlayerDead(self):

        '''
        Game state for when the player dies.  Shows the death screen for a
         period of time, and the resets the level.
        ''' 

        self.screen.blit(self.screenImage, (0,0))
        if not self.gameOver:
            self.screen.blit(self.death_test_image, self.death_test_rect)
        else:
            self.screen.blit(self.gameOverImage, self.death_test_rect)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
        newState = self.gameState
        if seconds > const.PLAYER_DEATH_SCREEN_TIMER:
            newState = self.resetLevel()

        return newState


    def statePlayerWins(self):

        '''
        Game state for when the player wins the game.  Displays the win screen
         for a period of time, and then goes to the high schore.
        ''' 

        self.screen.blit(self.screenImage, (0,0))
        self.screen.blit(self.playerWinsImage, self.death_test_rect)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / const.SECOND #calculate how many seconds
        newState = self.gameState
        if seconds > const.PLAYER_DEATH_SCREEN_TIMER:
            newState = const.GAME_STATE_HIGHSCORES
            self.highScores.newScore(self.player.score)

        return newState


    def stateMainMenu(self):

        '''
        Game state for when the user is at the main menu.
        ''' 

        if self.musicOn and self.musicFile != str(Path.cwd() / "sounds" / "musicMainMenu.mp3"):
            self.musicFile = str(Path.cwd() / "sounds" / "musicMainMenu.mp3")
            pygame.mixer.music.load(self.musicFile)
            pygame.mixer.music.play()

        newState = self.theMainMenu.showMenu(self.musicOn)
        if newState == const.GAME_STATE_RUNNING:
            self.levelNum = 1
            newState = self.resetLevel()

        return newState


    def stateHighScores(self):

        '''
        Game state for when the user is in the high score screen.
        ''' 

        newState = self.highScores.display()
        return newState


    def stateQuitting(self):

        '''
        Game state for when user chooses to quit the game.
        ''' 

        return const.GAME_STATE_QUITTING


    def resetLevel(self):

        '''
        Handles resetting a level, to include wiping out all spritegroups and
         loading a level.
        ''' 

        #Destroy all sprites in each spritegroup
        for enemy in self.spriteEnemies:
            enemy.kill()
        for bomb in self.spriteBombs:
            bomb.kill()
        for blast in self.spriteBombBlasts:
            blast.kill()
        for blast in self.spriteBossBombBlasts:
            blast.kill()
        for powerup in self.spritePowerups:
            powerup.kill()

        #Clear out each sprite group
        self.spritePlayer.empty()
        self.spriteEnemies.empty()
        self.spriteBombs.empty()
        self.spriteBombBlasts.empty()
        self.spriteBossBombBlasts.empty()
        
        #Since the player is initialized in the level class, backup the parameters that we want to keep by copying player to temp variable
        tempPlayer = self.player
        self.level, self.player, self.enemies, self.boss = Level.startNewLevel(self.levelNum)
        if self.exitingToMenu:
            self.exitingToMenu = False
            newState = const.GAME_STATE_MENU
        elif self.gameOver:
            self.gameOver = False
            self.highScores.newScore(tempPlayer.score)
            newState = const.GAME_STATE_HIGHSCORES
        else:
            self.player.lives = tempPlayer.lives
            self.player.increaseScore(tempPlayer.score)

            #player keeps powerups when going to next level, but not if player dies or exits to main menu
            if self.gameState == const.GAME_STATE_MENU:
                self.player.lives = const.LIVES
                self.player.score = 0
            elif tempPlayer.state != const.STATE_DEAD:
                self.player.bombCount = tempPlayer.bombCount
                self.player.bombRange = tempPlayer.bombRange
                self.player.boot = tempPlayer.boot
            self.spritePlayer.add(self.player)
            self.player.state = const.STATE_IDLE
            self.spriteEnemies.add(self.enemies)
            
            #Determine which music plays depending on if the current level is a boss level.
            if self.boss:
                self.spriteEnemies.add(self.boss)
                if self.musicOn and self.musicFile != str(Path.cwd() / "sounds" / "musicBoss.mp3"):
                    self.musicFile = str(Path.cwd() / "sounds" / "musicBoss.mp3")
                    pygame.mixer.music.load(self.musicFile)
            else:
                if self.musicOn and self.musicFile != str(Path.cwd() / "sounds" / "music1.mp3"):
                    self.musicFile = str(Path.cwd() / "sounds" / "music1.mp3")
                    pygame.mixer.music.load(self.musicFile)
            newState = const.GAME_STATE_RUNNING
        
        #Destroy temporary player variable since no longer needed
        tempPlayer.kill()

        return newState


    def killPlayer(self):

        '''
        When player is killed, adjust score accordingly, decrement and determine
         if game is over.
        ''' 

        self.player.increaseScore(const.PLAYER_DIED)
        self.player.state = const.STATE_DEAD
        if self.player.lives == 0:
            self.gameOver = True
        else:
            self.player.lives -= 1

        #Play death sound  
        if self.soundOn:
            self.deathSound.play()

    
    def checkPlayerProgress(self):

        '''
        Handles if player has completed a level, has died, or has won the game.
        ''' 

        #If player has reached the door and it is opened, adjust score accordingly and go to next level
        if self.level.layout[self.player.y][self.player.x] == const.TILE_DOOR_OPENED and self.player.state == const.STATE_IDLE:
            self.player.increaseScore(const.LEVEL_CHANGE)

            if self.levelNum < self.numLevels:
                self.levelNum += 1
                self.gameState = self.resetLevel()

        newState = self.gameState

        #If player died, display death screen briefly
        if self.player.state == const.STATE_DEAD:
            self.screenImage.blit(self.screen, (0,0), ((0,0), self.screenSize))    #take a snapshot of the screen
            newState = const.GAME_STATE_PLAYER_DEAD
            self.start_ticks = pygame.time.get_ticks() #starter tick

        #If player won game, display the winning screen briefly
        if self.player.state == const.STATE_PLAYER_WINS:
            self.screenImage.blit(self.screen, (0,0), ((0,0), self.screenSize))    #take a snapshot of the screen
            newState = const.GAME_STATE_PLAYER_WINS
            self.start_ticks = pygame.time.get_ticks() #starter tick

        return newState


    #User keyboard input, game controls
    def getUserInput(self):

        '''
        Get user input, for game controls / keyboard button presses
        ''' 

        #Get non-gameplay inputs
        self.getEvents()

        #Controls for movement and dropping bombs
        if self.gameState == const.GAME_STATE_RUNNING:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.player.move(const.UP, self.level)
            if key[pygame.K_DOWN]:
                self.player.move(const.DOWN, self.level)
            if key[pygame.K_LEFT]:
                self.player.move(const.LEFT, self.level)
            if key[pygame.K_RIGHT]:
                self.player.move(const.RIGHT, self.level)
            if key[pygame.K_SPACE]:
                newBomb = self.player.dropBomb(self.level)
                if newBomb:
                    self.level.layout[newBomb.y][newBomb.x] = newBomb
                    self.spriteBombs.add(newBomb)


    def getEvents(self):

        '''
        Event-driven input.  Handles things such as pressing escape to quit
         the game, 'f' to switch to fullscreen, and 'm'/'s' to toggle music
         and sound.
        ''' 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitingToMenu = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameState = const.GAME_STATE_MENU
                elif event.key == pygame.K_f:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode(self.screenSize)
                    else:
                        pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
                elif event.key == pygame.K_m:
                    if self.musicOn: 
                        self.musicOn = False
                    else:
                        self.musicOn = True
                elif event.key == pygame.K_s:
                    if self.soundOn: 
                        self.soundOn = False
                    else:
                        self.soundOn = True
                
                #If debug mode is on, call the debug mode inputs for 'cheats'
                if self.__debugMode:
                    self.debug_mode(event)
    

    def quitGame(self):

        '''
        Handles gracefully quitting the game.  Turns off music and display before quitting.
        ''' 

        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit()
        self.gameRunning = False


    def debug_mode(self, event):

        '''
        Debug mode is for the developer only, not for the user.  It is used
         to enter 'cheats' for testing gameplay mechanics.
        ''' 

        if event.key == pygame.K_z:     #kills player
            self.killPlayer()
        elif event.key == pygame.K_x:   #reduce lives to 0 for quick testing of highscore
            self.player.lives = 0
        elif event.key == pygame.K_k:   #kill all enemies on screen
            for enemy in self.spriteEnemies:
                enemy.kill()
        elif event.key == pygame.K_COMMA:
            if self.levelNum > 1:
                self.levelNum -= 1
                self.gameState = self.resetLevel()
        elif event.key == pygame.K_PERIOD:
            if self.levelNum < self.numLevels:
                self.levelNum += 1
                self.gameState = self.resetLevel()
        elif event.key == pygame.K_LSHIFT:
            if self.player.state == const.STATE_IDLE:
                powerups, blasts = self.level.destroyWalls(self.player.x, self.player.y, self.level, self.player.bombRange)
                self.spritePowerups.add(powerups)
        elif event.key == pygame.K_q:
            self.player.bombCount = const.POWERUP_MAX
            self.player.bombRange = const.POWERUP_MAX
            self.player.boot = True
        elif event.key == pygame.K_b:
            newBomb = self.boss.dropBomb(self.level)
            if newBomb:
                self.level.layout[newBomb.y][newBomb.x] = newBomb
                self.spriteBombs.add(newBomb)
                self.level.layout[newBomb.y][newBomb.x].kick(const.DOWN, self.level)
