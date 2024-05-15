import pygame
from Logger import log


class Button(object):
    def __init__(self, x, y, screen, image, scale):
        width = image.get_width()
        height = image.get_height()
        self._clicked = False
        self._screen = screen
        self._image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self._rect = self._image.get_rect()
        self._rect.topleft = (x, y)

    def draw(self):
        self._screen.blit(self._image, (self._rect.x, self._rect.y))

    def handle_mouse_events(self):
        action = False
        # Pegar a pos do mouse
        pos = pygame.mouse.get_pos()

        # Verifica mouseover e click
        if self._rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self._clicked == False:
                self._clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self._clicked = False
        return action
