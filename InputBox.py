import pygame
from pathlib import Path
import constants as const


#pygame.init()
#screen = pygame.display.set_mode((800, 600))


class InputBox(object):

    def __init__(self, screen, x, y, w, h, fontSize, colorInactive, colorActive, text=''):
        '''Class that handles the user inputing a name to be attached to a score in the high score list'''

        if not isinstance(screen,pygame.Surface):
            raise RuntimeError('Error: screen must be an instance of pygame.Surface')

        if not isinstance(x,int) or not isinstance(y,int) or not isinstance(w,int) or not isinstance(h,int) or not isinstance(fontSize,int):
            raise RuntimeError('Error: InputBox parameters x,y,w,h  and fontsize must be ints')

        if not isinstance(colorInactive,tuple) or not isinstance(colorActive,tuple):
            raise RuntimeError('Error: colorInactive and colorActive must be tuples')

        if not isinstance(text,str):
            raise RuntimeError('Error: text must be a str')


        self.__colorInactive__ = colorInactive
        self.__colorActive__ = colorActive
        self.__rect__ = pygame.Rect(x, y, w, h)
        self.__color__ = self.__colorActive__
        self.__text__ = text
        self.maxChars = 3
        self.__font__ = pygame.font.Font(None, fontSize)
        self.__textSurface__ = self.__font__.render(text, True, self.__color__)
        self.__textX__ = self.__rect__.x + self.__rect__.width / 2 - self.__textSurface__.get_width() / 2
        self.__returnValue__ = None
        self.__screen__ = screen

        graphicsDir = Path.cwd() / "graphics"

        imageFile = str(graphicsDir.joinpath("new_high_score.png"))
        self.__background__ = pygame.image.load(imageFile)


    def handle_event(self, event):
        '''Translates events into proper return value for InputBox.run()'''
        #if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
        #    if self.__rect__.collidepoint(event.pos):
                # Toggle the active variable.
        #        self.active = not self.active
        #    else:
        #        self.active = False
            # Change the current color of the input box.
        #    if self.active:
        #        self.__color__ = self.__colorActive__
        #    else:
        #        self.__color__ = self.__colorInactive__
        #    self.__textSurface__ = self.__font__.render(self.__text__, True, self.__color__)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.__returnValue__ = self.__text__
                self.__text__ = ''
            elif event.key == pygame.K_BACKSPACE:
                self.__text__ = self.__text__[:-1]
            elif len(self.__text__) < self.maxChars:
                self.__text__ += event.unicode
            # Re-render the text.
            self.__textSurface__ = self.__font__.render(self.__text__, True, self.__color__)

        return self.__returnValue__


    def draw(self, screen):
        '''Draws the user input onto the screen'''
        self.__screen__.blit(self.__background__, (0,0))
        screen.blit(self.__textSurface__, (self.__rect__.x + self.__rect__.width / 2 - self.__textSurface__.get_width() / 2, self.__rect__.y + 5))
        pygame.draw.rect(screen, self.__color__, self.__rect__, 2)



    def run(self):
        '''Maintains the loop gets the user intput from the keyboard and updates the input field'''
        clock = pygame.time.Clock()
        #fontSize = 32
        # inputBox = InputBox(320, 240, 58, 32, fontSize, const.GREY, const.GREEN)
        finished = False

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                
                userInput = self.handle_event(event)
                if userInput == 'QUIT':
                    finished = True
                if userInput:
                    finished = True

            self.__screen__.fill(const.BLACK)
            self.draw(self.__screen__)

            pygame.display.flip()
            clock.tick(60)
        return self.__returnValue__


if __name__ == '__main__':
    main()
    pygame.quit()
