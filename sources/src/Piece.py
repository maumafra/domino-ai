import pygame
from pygame.locals import *
from Constants import *
from Logger import log


class Piece(object):
    def __init__(self, number1, number2, screen, X, Y):
        self._number1 = number1
        self._number2 = number2

        self._played = False
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

    def is_played(self):
        return self._played

    def set_played(self):
        self._played = True

    def show_horizontal(self):
        self._screen.blit(self._square1, (self._X, self._Y))
        self._screen.blit(pygame.transform.flip(self._square2, True, False), ((self._X + 32), self._Y))
        pygame.display.update()

    def show_vertical(self):
        self._screen.blit(self._square1, (self._X, self._Y))
        self._screen.blit(pygame.transform.flip(self._square2, False, True), (self._X, (self._Y + 32)))
        pygame.display.update()

    def show_vertical_scaled(self):
        scaled_piece = pygame.transform.scale(self._square1, (64, 64))
        self._screen.blit(scaled_piece, (self._X, self._Y))
        scaled_piece = pygame.transform.scale(self._square2, (64, 64))
        self._screen.blit(pygame.transform.flip(scaled_piece, False, True), (self._X, (self._Y + 64)))
        pygame.display.update()

    def show_blank_vertical(self):
        scaled_piece = pygame.transform.scale(self._blank, (64, 64))
        self._screen.blit(scaled_piece, (self._X, self._Y))
        self._screen.blit(pygame.transform.flip(scaled_piece, False, True), (self._X, (self._Y + 64)))
        pygame.display.update()

    def show_played_vertical(self):
        pygame.draw.rect(self._screen, OUTER_COLOR, self._rect)
        pygame.display.update()

    def handle_mouse_events(self):
        # Pegar a pos do mouse
        pos = pygame.mouse.get_pos()

        # Verifica mouseover e click
        if self._rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self._clicked == False:
                self._clicked = True
                log('CLICKED '+str(self._number1)+", "+str(self._number2))

        if pygame.mouse.get_pressed()[0] == 0:
            self._clicked = False
