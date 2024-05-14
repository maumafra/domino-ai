import pygame
from time import sleep
from pygame.locals import *
from Logger import log
from GeneratePieces import generate_pieces
from Constants import *
from Piece import *
from Button import *

#Variáveis e constantes
PLAYER_PIECES = []
COMPUTER_PIECES = []
BOARD_PIECES = []
STOCK_PIECES = []
GREATER_PIECE = []
PLAYER_PIECES_OBJ = []
COMPUTER_PIECES_OBJ = []
BUTTONS = []

def initialize(screen):

    global PLAYER_PIECES
    global COMPUTER_PIECES
    global STOCK_PIECES
    global GREATER_PIECE
    global current_l_end_x
    global current_r_end_x

    # Pegar as pecas geradas e setar nas variaveis
    generated_pieces = generate_pieces()
    PLAYER_PIECES = generated_pieces[0]
    COMPUTER_PIECES = generated_pieces[1]
    STOCK_PIECES = generated_pieces[2]
    GREATER_PIECE = generated_pieces[3]
    current_r_end_x = RESOLUTION[0] // 2 - 32
    current_l_end_x = current_r_end_x - 64

    # Chamar as funcoes de desenho
    draw_background(screen)
    init_pieces(screen)
    init_buttons(screen)
    draw_pieces()
    draw_buttons()

def draw_background(screen):
    # Desenhar o retangulo do centro
    center_rectangle_start = (0, RESOLUTION[1] / 4)
    center_rectangle_size = (RESOLUTION[0], RESOLUTION[1] / 2)
    center_rectangle = Rect(center_rectangle_start, center_rectangle_size)
    pygame.draw.rect(screen, INNER_COLOR, center_rectangle)

    # Desenhar o retangulo de cima e de baixo
    upper_rectangle_start = (0, 0)
    upper_rectangle_size = (RESOLUTION[0], RESOLUTION[1] / 4)
    lower_rectangle_y = RESOLUTION[1] - RESOLUTION[1] / 4
    lower_rectangle_start = (0, lower_rectangle_y)
    lower_rectangle_size = (RESOLUTION[0], RESOLUTION[1] / 4)
    upper_rectangle = Rect(upper_rectangle_start, upper_rectangle_size)
    lower_rectangle = Rect(lower_rectangle_start, lower_rectangle_size)
    pygame.draw.rect(screen, OUTER_COLOR, upper_rectangle)
    pygame.draw.rect(screen, OUTER_COLOR, lower_rectangle)

def init_pieces(screen):
    global PLAYER_PIECES_OBJ
    global COMPUTER_PIECES_OBJ

    PLAYER_PIECES_OBJ = [None] * len(PLAYER_PIECES)
    COMPUTER_PIECES_OBJ = [None] * len(COMPUTER_PIECES)

    # Criar os objetos das pecas do player
    player_start_x = (RESOLUTION[0] - 565) // 2 + 25
    player_start_y = RESOLUTION[1] - (RESOLUTION[1] // 8) - 64
    for i in range(len(PLAYER_PIECES)):
        temp_piece = Piece(PLAYER_PIECES[i][0], PLAYER_PIECES[i][1], screen, player_start_x, player_start_y)
        PLAYER_PIECES_OBJ[i] = temp_piece
        player_start_x += 80

    # Criar os objetos das pecas do computador
    computer_start_x = (RESOLUTION[0] - 565) // 2 + 25
    cumputer_start_y = (RESOLUTION[1] // 8) - 64
    for i in range(len(COMPUTER_PIECES)):
        temp_piece = Piece(COMPUTER_PIECES[i][0], COMPUTER_PIECES[i][1], screen, computer_start_x, cumputer_start_y)
        COMPUTER_PIECES_OBJ[i] = temp_piece
        computer_start_x += 80

def draw_pieces():
    # Desenhar as pecas do player
    for i in range(len(PLAYER_PIECES_OBJ)):
        piece = PLAYER_PIECES_OBJ[i]
        if piece.is_played():
            piece.show_played_vertical()
        else:
            piece.show_vertical_scaled()

    # Desenhar as pecas do computador
    for i in range(len(COMPUTER_PIECES_OBJ)):
        piece = COMPUTER_PIECES_OBJ[i]
        if piece.is_played():
            piece.show_played_vertical()
        else:
            piece.show_blank_vertical()

def init_buttons(screen):
    global BUTTONS

    BUTTONS = [None] * QT_BUTTONS

    # Carregar as imagens
    pass_button_img = pygame.image.load("../images/deactive_pass.png").convert_alpha()
    replay_button_img = pygame.image.load("../images/normal_replay.png").convert_alpha()
    exit_button_img = pygame.image.load("../images/normal_exit.png").convert_alpha()

    replay_button_x = ((RESOLUTION[0] - 565) // 2 - 162) // 2
    replay_button_y = RESOLUTION[1] - 70 - RESOLUTION[1] // 8
    replay_button = Button(replay_button_x, replay_button_y, screen, replay_button_img, 2)
    BUTTONS[REPLAY_BTN] = replay_button

    exit_button_x = replay_button_x
    exit_button_y = replay_button_y + 70
    exit_button = Button(exit_button_x, exit_button_y, screen, exit_button_img, 2)
    BUTTONS[EXIT_BTN] = exit_button

    pass_button_x = ((RESOLUTION[0] - 565) // 2 + 565) + ((RESOLUTION[0] - 565) // 2 - 99) // 2
    pass_button_y = replay_button_y
    pass_button = Button(pass_button_x, pass_button_y, screen, pass_button_img, 2)
    BUTTONS[PASS_BTN] = pass_button

def draw_buttons():
    for i in range(len(BUTTONS)):
        BUTTONS[i].handle_mouse_events()
        BUTTONS[i].draw()
    pygame.display.update()

def play_piece(piece, screen, side):
    global current_l_end_x
    global current_r_end_x

    piece_x = 0
    if side == RIGHT:
        # Valida se precisa reverter a peca
        if len(BOARD_PIECES) > 0 and piece[1] == BOARD_PIECES[-1][-1]:
            piece.reverse()
        piece_x = current_r_end_x
        BOARD_PIECES.append([piece[0], piece[1]])
    else:
        # Valida se precisa reverter a peca
        if piece[0] == BOARD_PIECES[0][0]:
            piece.reverse()
        piece_x = current_l_end_x
        BOARD_PIECES.insert(0, [piece[0], piece[1]])

    if piece[0] == piece[1]:
        piece_y = RESOLUTION[1] // 2 - 32
        current_r_end_x += 32
        temp_piece = Piece(piece[0], piece[1], screen, piece_x, piece_y)
        temp_piece.show_vertical()
    else:
        piece_y = RESOLUTION[1] // 2 - 16
        current_r_end_x += 64
        temp_piece = Piece(piece[0], piece[1], screen, piece_x, piece_y)
        temp_piece.show_horizontal()

    log("Board Pieces: "+str(BOARD_PIECES))

def player_play(piece, screen, side):
    global PLAYER_TURN

    play_piece(piece, screen, side)
    piece_index = PLAYER_PIECES.index(piece)
    PLAYER_PIECES_OBJ[piece_index].set_played()
    PLAYER_PIECES.remove(piece)
    PLAYER_TURN = False

def computer_play(piece, screen, side):
    global PLAYER_TURN

    sleep(1.5)
    play_piece(piece, screen, side)
    piece_index = COMPUTER_PIECES.index(piece)
    COMPUTER_PIECES_OBJ[piece_index].set_played()
    COMPUTER_PIECES.remove(piece)
    PLAYER_TURN = True

def play_greater_piece(screen):
    if GREATER_PIECE in PLAYER_PIECES:
        sleep(1.5)
        player_play(GREATER_PIECE, screen, RIGHT)
        log("Starting game playing "+str(GREATER_PIECE)+" from Player")
    if GREATER_PIECE in COMPUTER_PIECES:
        computer_play(GREATER_PIECE, screen, RIGHT)
        log("Starting game playing " + str(GREATER_PIECE) + " from Computer")

def player_turn(screen):
    if PLAYER_TURN:
        for i in range(len(PLAYER_PIECES_OBJ)):
            if PLAYER_PIECES_OBJ[i].handle_mouse_events() and PLAYER_TURN:
                validate_piece(PLAYER_PIECES_OBJ[i], screen)

def validate_piece(piece_obj, screen):
    connection_numbers = [BOARD_PIECES[0][0], BOARD_PIECES[-1][-1]]
    piece = piece_obj.get_numbers()
    # Valida peca a esquerda
    if connection_numbers[0] in piece:
        # Joga a peca
        player_play(piece, screen, LEFT)

    # Valida peca a direita
    elif connection_numbers[1] in piece:
        # Joga a peca
        player_play(piece, screen, RIGHT)
    # Peca não entra em nenhum lado
    else:
        log('Illegal move')


def game(screen):
    play_greater_piece(screen)
    player_turn(screen)
    draw_buttons()
    draw_pieces()