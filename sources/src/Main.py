import pygame
from pygame.locals import *
# from sys import exit
from Game import *
from Logger import log
from Constants import *

#Variáveis e constantes


def main():
    # Inicializa o pygame
    pygame.init()

    # Cria a janela principal
    screen = pygame.display.set_mode(RESOLUTION, RESIZABLE, 32)
    pygame.display.set_caption("Dominos!")

    # Inicializa o jogo
    initialize(screen)

    # Loop do jogo
    run = True
    while run:

        # Handler dos eventos
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False

            # Game Over
            elif GAME_OVER:
                run = False

            else:
                game(screen)


        pygame.display.update()


if __name__ == "__main__":
    main()