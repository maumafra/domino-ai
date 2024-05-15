import pygame
from time import sleep
from pygame.locals import *
from Logger import log
from GeneratePieces import generate_game_pieces
from Constants import *
from Piece import *
from Button import *
from Computer import *

#Variáveis e constantes
PLAYER_PIECES = []
COMPUTER_PIECES = []
BOARD_PIECES = []
STOCK_PIECES = []
GREATER_PIECE = []
PLAYER_PIECES_OBJ = []
COMPUTER_PIECES_OBJ = []
BUTTONS = []
WINNER = STILL_NO_WINNER

def initialize(screen):

    global PLAYER_PIECES
    global COMPUTER_PIECES
    global STOCK_PIECES
    global GREATER_PIECE
    global CURRENT_PIECE
    global current_l_end_x
    global current_r_end_x

    # Pegar as pecas geradas e setar nas variaveis
    generated_pieces = generate_game_pieces()
    PLAYER_PIECES = generated_pieces[0]
    COMPUTER_PIECES = generated_pieces[1]
    STOCK_PIECES = generated_pieces[2]
    GREATER_PIECE = generated_pieces[3]
    CURRENT_PIECE = []
    current_r_end_x = RESOLUTION[0] // 2 - 16
    current_l_end_x = current_r_end_x - 64

    # Chamar as funcoes de desenho
    draw_background(screen)
    init_pieces(screen)
    init_buttons(screen)
    draw_pieces()
    draw_buttons()
    log("----- initialize end -----")

def draw_background(screen):
    # Desenhar o retangulo do centro
    center_rectangle_start = (0, RESOLUTION[1] / 4)
    center_rectangle_size = (RESOLUTION[0], RESOLUTION[1] / 2)
    center_rectangle = Rect(center_rectangle_start, center_rectangle_size)
    pygame.draw.rect(screen, INNER_COLOR, center_rectangle)
    draw_upper_lower_bg(screen)

def draw_upper_lower_bg(screen):
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
    player_start_x = RESOLUTION[0]//2 - (40*len(PLAYER_PIECES_OBJ) - 8)
    player_start_y = RESOLUTION[1] - (RESOLUTION[1] // 8) - 64
    for i in range(len(PLAYER_PIECES_OBJ)):
        PLAYER_PIECES_OBJ[i].show_vertical_scaled(player_start_x, player_start_y)
        player_start_x += 80

    computer_start_x = RESOLUTION[0] // 2 - (40 * len(COMPUTER_PIECES_OBJ) - 8)
    computer_start_y = (RESOLUTION[1] // 8) - 64
    # Desenhar as pecas do computador
    for i in range(len(COMPUTER_PIECES_OBJ)):
        COMPUTER_PIECES_OBJ[i].show_blank_vertical(computer_start_x, computer_start_y)
        computer_start_x += 80

def init_buttons(screen):
    global BUTTONS

    BUTTONS = [None] * QT_BUTTONS

    # Carregar as imagens
    pass_button_img = pygame.image.load("../images/deactive_pass.png").convert_alpha()
    replay_button_img = pygame.image.load("../images/normal_replay.png").convert_alpha()
    exit_button_img = pygame.image.load("../images/normal_exit.png").convert_alpha()
    left_button_img = pygame.image.load("../images/left.png").convert_alpha()
    right_button_img = pygame.image.load("../images/right.png").convert_alpha()

    replay_button_x = (RESOLUTION[0])//7 - 144
    replay_button_y = RESOLUTION[1] - 70 - RESOLUTION[1] // 8
    replay_button = Button(replay_button_x, replay_button_y, screen, replay_button_img, SCALE)
    BUTTONS[REPLAY_BTN] = replay_button

    exit_button_x = replay_button_x + 16
    exit_button_y = replay_button_y + 70
    exit_button = Button(exit_button_x, exit_button_y, screen, exit_button_img, SCALE)
    BUTTONS[EXIT_BTN] = exit_button

    pass_button_x = (RESOLUTION[0]*6)//7
    pass_button_y = replay_button_y
    pass_button = Button(pass_button_x, pass_button_y, screen, pass_button_img, SCALE)
    BUTTONS[PASS_BTN] = pass_button

    left_button_x = pass_button_x - 64 - 6
    left_button_y = pass_button_y
    left_button = Button(left_button_x, left_button_y, screen, left_button_img, SCALE)
    BUTTONS[LEFT_BTN] = left_button

    right_button_x = pass_button_x + int(pass_button_img.get_width() * SCALE)
    right_button_y = pass_button_y
    right_button = Button(right_button_x, right_button_y, screen, right_button_img, SCALE)
    BUTTONS[RIGHT_BTN] = right_button

def draw_buttons():
    for i in range(len(BUTTONS)):
        #BUTTONS[i].handle_mouse_events()
        BUTTONS[i].draw()
    pygame.display.update()

def play_piece(piece_p, screen, side):
    global current_l_end_x
    global current_r_end_x

    piece = [piece_p[0], piece_p[1]]
    piece_x = 0
    if side == RIGHT:
        # Valida se precisa reverter a peca
        if len(BOARD_PIECES) > 0 and piece[1] == BOARD_PIECES[-1][-1]:
            piece.reverse()
        piece_x = current_r_end_x
        if piece[0] == piece[1]:
            current_r_end_x += 32
        else:
            current_r_end_x += 64
        BOARD_PIECES.append([piece[0], piece[1]])
    else:
        # Valida se precisa reverter a peca
        if piece[0] == BOARD_PIECES[0][0]:
            piece.reverse()
        piece_x = current_l_end_x
        if piece[0] == piece[1]:
            piece_x += 32
            current_l_end_x -= 32
        else:
            current_l_end_x -= 64
        BOARD_PIECES.insert(0, [piece[0], piece[1]])

    if piece[0] == piece[1]:
        piece_y = RESOLUTION[1] // 2 - 32
        temp_piece = Piece(piece[0], piece[1], screen, piece_x, piece_y)
        temp_piece.show_vertical()
    else:
        piece_y = RESOLUTION[1] // 2 - 16
        temp_piece = Piece(piece[0], piece[1], screen, piece_x, piece_y)
        temp_piece.show_horizontal()

    log("Board Pieces: "+str(BOARD_PIECES))

def player_play(piece, screen, side):
    play_piece(piece, screen, side)
    piece_index = PLAYER_PIECES.index(piece)
    PLAYER_PIECES_OBJ[piece_index].show_played_vertical()
    PLAYER_PIECES_OBJ.remove(PLAYER_PIECES_OBJ[piece_index])
    PLAYER_PIECES.remove(piece)
    log('Player pieces: ' + str(PLAYER_PIECES))
    switch_turn()
    pygame.display.update()

def computer_play(piece, screen, side):
    play_piece(piece, screen, side)
    piece_index = COMPUTER_PIECES.index(piece)
    COMPUTER_PIECES_OBJ[piece_index].show_played_vertical()
    COMPUTER_PIECES_OBJ.remove(COMPUTER_PIECES_OBJ[piece_index])
    COMPUTER_PIECES.remove(piece)
    log('Computer pieces: '+str(COMPUTER_PIECES))
    switch_turn()
    pygame.display.update()

def play_greater_piece(screen):
    if GREATER_PIECE in PLAYER_PIECES:
        sleep(1.5)
        log("Starting game playing " + str(GREATER_PIECE) + " from Player")
        set_player_turn(True)
        player_play(GREATER_PIECE, screen, RIGHT)
    if GREATER_PIECE in COMPUTER_PIECES:
        sleep(1.5)
        log("Starting game playing " + str(GREATER_PIECE) + " from Computer")
        set_player_turn(False)
        computer_play(GREATER_PIECE, screen, RIGHT)

def set_player_turn(player):
    global PLAYER_TURN

    PLAYER_TURN = player

def switch_turn():
    global PLAYER_TURN

    PLAYER_TURN = not PLAYER_TURN

def player_turn(screen):
    global CURRENT_PIECE

    if PLAYER_TURN:
        for i in range(len(PLAYER_PIECES_OBJ)):
            if PLAYER_PIECES_OBJ[i].handle_mouse_events() and PLAYER_TURN:
                CURRENT_PIECE = []
                validate_piece(PLAYER_PIECES_OBJ[i], screen)
                break

def pass_move(screen, deck, player):
    if has_valid_piece(deck) == False:
        if len(STOCK_PIECES) > 0:
            buy_piece(player, screen)
        else:
            switch_turn()

def has_valid_piece(deck):
    connection_numbers = [BOARD_PIECES[0][0], BOARD_PIECES[-1][-1]]
    for piece in deck:
        if connection_numbers[0] in piece or connection_numbers[1] in piece:
            return True
    return False

def buy_piece(player, screen):
    global STOCK_PIECES

    piece_bought = STOCK_PIECES.pop()
    piece_bought_obj = Piece(piece_bought[0], piece_bought[1], screen, 0, 0)
    if player:
        PLAYER_PIECES.append(piece_bought)
        PLAYER_PIECES_OBJ.append(piece_bought_obj)
        log('Player bought piece '+piece_bought_obj.to_str())
    else:
        COMPUTER_PIECES.append(piece_bought)
        COMPUTER_PIECES_OBJ.append(piece_bought_obj)
        log('Computer bought piece ' + piece_bought_obj.to_str())
    log('Stock pieces: ' + str(STOCK_PIECES))


def buttons_click_event(screen):
    global CURRENT_PIECE

    for i in range(len(BUTTONS)):
        if BUTTONS[i].handle_mouse_events():
            if i == EXIT_BTN:
                log('Clicked on Exit -- Quiting game')
                exit_event = pygame.event.Event(pygame.QUIT)
                pygame.event.post(exit_event)
            if i == REPLAY_BTN:
                #TODO replay
                log('Clicked on Replay -- Restarting')
            if i == PASS_BTN:
                pass_move(screen, PLAYER_PIECES, True)
                log('Clicked on Pass')
            if i == LEFT_BTN:
                if len(CURRENT_PIECE) == 2:
                    player_play(CURRENT_PIECE, screen, LEFT)
                    CURRENT_PIECE = []
                log('Clicked on Left')
            if i == RIGHT_BTN:
                if len(CURRENT_PIECE) == 2:
                    player_play(CURRENT_PIECE, screen, RIGHT)
                    CURRENT_PIECE = []
                log('Clicked on Right')

def validate_piece(piece_obj, screen):
    global CURRENT_PIECE

    connection_numbers = [BOARD_PIECES[0][0], BOARD_PIECES[-1][-1]]
    piece = piece_obj.get_numbers()

    # Valida peca a direita e esquerda
    if connection_numbers[0] in piece and connection_numbers[1] in piece:
        CURRENT_PIECE = piece
        log('Waiting for player to choose which side to play piece '+piece_obj.to_str())

    # Valida peca a esquerda
    elif connection_numbers[0] in piece:
        # Joga a peca
        player_play(piece, screen, LEFT)

    # Valida peca a direita
    elif connection_numbers[1] in piece:
        # Joga a peca
        player_play(piece, screen, RIGHT)
    # Peca não entra em nenhum lado
    else:
        log('Illegal move')

def computer_turn(screen):
    if PLAYER_TURN == False:
        sleep(1.5)
        # best_possible_move = random_move(BOARD_PIECES, COMPUTER_PIECES)
        best_possible_move = best_move(BOARD_PIECES, COMPUTER_PIECES)
        if len(best_possible_move) == 0:
            pass_move(screen, COMPUTER_PIECES, False)
            return
        piece = [best_possible_move[0][0], best_possible_move[0][1]]
        log('Computer is about to play piece '+str(piece))
        computer_play(piece, screen, best_possible_move[1])

def turn(screen):
    if PLAYER_TURN:
        player_turn(screen)
    else:
        computer_turn(screen)

def check_game_over():
    global WINNER
    GAME_OVER = False

    if WINNER in [PLAYER_WIN, TIE, COMPUTER_WIN]:
        return True

    if len(PLAYER_PIECES) == 0:
        GAME_OVER = True
        WINNER = PLAYER_WIN
        print('Player won!')

    if len(COMPUTER_PIECES) == 0:
        GAME_OVER = True
        WINNER = COMPUTER_WIN
        print('Computer won!')

    if len(STOCK_PIECES) == 0 and has_valid_piece(PLAYER_PIECES) == False and has_valid_piece(COMPUTER_PIECES) == False:
        GAME_OVER = True
        WINNER = TIE
        print('Tie')

    return GAME_OVER

def game_over():
    #TODO game over screen
    set_player_turn(False)

def game(screen):
    if check_game_over():
        game_over()
        buttons_click_event(screen)
        return
    play_greater_piece(screen)
    buttons_click_event(screen)
    turn(screen)
    # -- draw --
    draw_upper_lower_bg(screen)
    draw_pieces()
    draw_buttons()
