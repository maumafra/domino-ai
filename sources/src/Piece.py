import pygame
from pygame.locals import *
from Constants import *
from Logger import log


class Piece(object):
    def __init__(self, number1, number2, screen, X, Y):
        self._number1 = number1
        self._number2 = number2

        self._clicked = False

        self._X = X
        self._Y = Y
        self._rect = Rect((self._X, self._Y), (64, 128))

        self._screen = screen

        number1_place = "../images/domino_pieces/" + str(self._number1) + ".png"
        self._square1 = pygame.image.load(number1_place).convert_alpha()

        number2_place = "../images/domino_pieces/" + str(self._number2) + ".png"
        self._square2 = pygame.image.load(number2_place).convert_alpha()

        blank_place = "../images/domino_pieces/8.png"
        self._blank = pygame.image.load(blank_place).convert_alpha()

    def get_numbers(self):
        return [self._number1, self._number2]

    def to_str(self):
        return str(self._number1)+", "+str(self._number2)

    def show_horizontal(self):
        self._screen.blit(pygame.transform.rotate(self._square1, 90), (self._X, self._Y))
        self._screen.blit(pygame.transform.flip(pygame.transform.rotate(self._square2, -90), False, True), ((self._X + 32), self._Y))
        pygame.display.update()

    def show_vertical(self):
        self._screen.blit(self._square1, (self._X, self._Y))
        self._screen.blit(pygame.transform.flip(self._square2, False, True), (self._X, (self._Y + 32)))
        pygame.display.update()

    def show_vertical_scaled(self, x, y):
        self._X = x
        self._Y = y
        self._rect = Rect((self._X, self._Y), (64, 128))
        scaled_piece = pygame.transform.scale(self._square1, (64, 64))
        self._screen.blit(scaled_piece, (x, y))
        scaled_piece = pygame.transform.scale(self._square2, (64, 64))
        self._screen.blit(pygame.transform.flip(scaled_piece, False, True), (x, (y + 64)))

    def show_blank_vertical(self, x, y):
        scaled_piece = pygame.transform.scale(self._blank, (64, 64))
        self._screen.blit(scaled_piece, (x, y))
        self._screen.blit(pygame.transform.flip(scaled_piece, False, True), (x, (y + 64)))

    def show_played_vertical(self):
        pygame.draw.rect(self._screen, OUTER_COLOR, self._rect)
        pygame.display.update()

    def handle_mouse_events(self):
        # Pegar a pos do mouse
        pos = pygame.mouse.get_pos()

        action = False

        # Verifica mouseover e click
        if self._rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self._clicked == False:
                self._clicked = True
                action = True
                log('Clicked piece '+self.to_str())

        if pygame.mouse.get_pressed()[0] == 0:
            self._clicked = False

        return action
