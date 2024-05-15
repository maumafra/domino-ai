import pygame
from pygame.locals import *
# from sys import exit
from Game import *
from Logger import log
from Constants import *


def main():
    # Inicializa o pygame
    pygame.init()

    # Cria a janela principal
    screen = pygame.display.set_mode(RESOLUTION, RESIZABLE, 32)
    pygame.display.set_caption("Dominos!")

    # Inicializa o jogo
    initialize(screen)

    clock = pygame.time.Clock()

    # Loop do jogo
    run = True
    while run:
        # Controlar as execucoes por segundo para reduzir o consumo da GPU/CPU
        clock.tick(FPS)

        # Handler dos eventos
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT

            # Execucao normal do jogo
            else:
                game(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()