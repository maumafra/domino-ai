from random import shuffle
from Logger import log
from itertools import combinations_with_replacement

def generate_pieces():
    # Lista das pecas
    dominoes = list(combinations_with_replacement(range(0, 7), 2))
    # Converter lista de tuples para uma lista de listas
    dominoes = [list(x) for x in dominoes]
    return dominoes

def generate_game_pieces():
    # Lista das pecas
    dominoes = list(combinations_with_replacement(range(0, 7), 2))
    # Converter lista de tuples para uma lista de listas
    dominoes = [list(x) for x in dominoes]
    # Embaralhar
    shuffle(dominoes)
    # Coeficiente = metade de 28 (len(dominoes)) = 14
    coefficient = len(dominoes) // 2
    # Vai pegar as primeiras 14 pecas
    stock_pieces = dominoes[:coefficient]
    # Vai pegar as pecas entre as posicoes 14 e 21. (21 => 14 + 14/2)
    computer_pieces = dominoes[coefficient:int(coefficient * 1.5)]
    # Vai pegar as pecas depois da posicao 21
    player_pieces = dominoes[int(coefficient * 1.5):]
    # Vai pegar a maior peca, que sera jogada primeiro
    greater_piece = max([[x, y] for x, y in computer_pieces + player_pieces if x == y])
    ret_list = [player_pieces, computer_pieces, stock_pieces, greater_piece]
    log("Player pieces: "+str(ret_list[0]))
    log("Computer pieces: "+str(ret_list[1]))
    log("Stock pieces: "+str(ret_list[2]))
    log("Greater double: "+str(ret_list[3]))
    return ret_list

#generate_pieces()
