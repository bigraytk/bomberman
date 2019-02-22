import pygame
import constants as const


#pygame.init()
#screen = pygame.display.set_mode((800, 600))


class InputBox:

    def __init__(self, screen, x, y, w, h, fontSize, colorInactive, colorActive, text=''):
        self.colorInactive = colorInactive
        self.colorActive = colorActive
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.colorActive
        self.text = text
        self.maxChars = 3
        self.font = pygame.font.Font(None, fontSize)
        self.textSurface = self.font.render(text, True, self.color)
        self.textX = self.rect.x + self.rect.width / 2 - self.textSurface.get_width() / 2
        self.active = True
        self.returnValue = None
        self.screen = screen

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            if self.active:
                self.color = self.colorActive
            else:
                self.color = self.colorInactive
            self.textSurface = self.font.render(self.text, True, self.color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_ESCAPE:
                    self.text = ''
                    #self.active = False
                elif event.key == pygame.K_RETURN:
                    print(self.text)
                    self.returnValue = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.maxChars:
                    self.text += event.unicode
                # Re-render the text.
                self.textSurface = self.font.render(self.text, True, self.color)
            else:
                if event.key == pygame.K_ESCAPE:
                    self.returnValue = 'QUIT'

        return self.returnValue

    def draw(self, screen):
        screen.blit(self.textSurface, (self.rect.x + self.rect.width / 2 - self.textSurface.get_width() / 2, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)



def run():
    clock = pygame.time.Clock()
    #fontSize = 32
    # inputBox = InputBox(320, 240, 58, 32, fontSize, const.GREY, const.GREEN)
    finished = False

    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            
            userInput = inputBox.handle_event(event)
            if userInput == 'QUIT':
                finished = True

        screen.fill(const.BLACK)
        inputBox.draw(self.screen)

        pygame.display.flip()
        clock.tick(60)
    return self.returnValue


if __name__ == '__main__':
    main()
    pygame.quit()
