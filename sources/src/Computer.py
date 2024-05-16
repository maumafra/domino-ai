import sys
from Constants import *
from GeneratePieces import generate_pieces

def random_move(board_pieces, computer_pieces):
    possible_moves = get_possible_moves(board_pieces, computer_pieces)
    if len(possible_moves) == 0:
        return []
    best_possible_move = possible_moves[0]
    return [best_possible_move[0], best_possible_move[1]]

def best_move(board_pieces, computer_pieces):
    best_score = -sys.maxsize - 1
    best_computer_move = []
    possible_moves = get_possible_moves(board_pieces, computer_pieces)
    if len(possible_moves) == 0:
        return []
    for move in possible_moves:
        board_copy = board_pieces.copy()
        pieces_copy = computer_pieces.copy()
        pieces_copy.remove(move[0])
        if move[1] == RIGHT:
            board_copy.append(move[0])
        else:
            board_copy.insert(0, move[0])
        #score = minimax(board_copy, pieces_copy, 0, False)
        score = minimax_ab(board_copy, pieces_copy, -sys.maxsize - 1, sys.maxsize, 0, False)
        if score > best_score:
            best_score = score
            best_computer_move = move
    return best_computer_move

def minimax(board_pieces, computer_pieces, depth, maximize):
    if maximize:
        best_score = -sys.maxsize -1
        possible_moves = get_possible_moves(board_pieces, computer_pieces)
        if len(possible_moves) == 0:
            return depth
        for move in possible_moves:
            board_copy = board_pieces.copy()
            pieces_copy = computer_pieces.copy()
            pieces_copy.remove(move[0])
            if move[1] == RIGHT:
                board_copy.append(move[0])
            else:
                board_copy.insert(0, move[0])
            score = minimax(board_copy, pieces_copy, depth + 1, False)
            best_score = max(score, best_score)
        return best_score

    else:
        best_score = sys.maxsize - 1
        possible_moves = get_other_player_possible_moves(board_pieces, computer_pieces)
        if len(possible_moves) == 0:
            return depth
        for move in possible_moves:
            board_copy = board_pieces.copy()
            pieces_copy = computer_pieces.copy()
            if move[1] == RIGHT:
                board_copy.append(move[0])
            else:
                board_copy.insert(0, move[0])
            score = minimax(board_copy, pieces_copy, depth + 1, True)
            best_score = min(score, best_score)
        return best_score

def get_possible_moves(board_pieces, list_of_pieces):
    connection_numbers = [board_pieces[0][0], board_pieces[-1][-1]]
    possible_moves = []
    for piece in list_of_pieces:
        if connection_numbers[0] in piece:
            possible_moves.append([[piece[0], piece[1]], LEFT])
        if connection_numbers[1] in piece:
            possible_moves.append([[piece[0], piece[1]], RIGHT])
    return possible_moves

def get_other_player_possible_moves(board_pieces, computer_pieces):
    possible_player_pieces = generate_pieces()
    for i in board_pieces + computer_pieces:
        try:
            possible_player_pieces.remove(i)
        except ValueError:
            pass
    return get_possible_moves(board_pieces, possible_player_pieces)

def minimax_ab(board_pieces, computer_pieces, alpha, beta, depth, maximize):
    if maximize:
        best_score = -sys.maxsize -1
        possible_moves = get_possible_moves(board_pieces, computer_pieces)
        if len(possible_moves) == 0:
            return depth
        for move in possible_moves:
            board_copy = board_pieces.copy()
            pieces_copy = computer_pieces.copy()
            pieces_copy.remove(move[0])
            if move[1] == RIGHT:
                if len(board_copy) > 0 and move[0][1] == board_copy[-1][-1]:
                    move[0].reverse()
                board_copy.append(move[0])
            else:
                if len(board_copy) > 0 and move[0][0] == board_copy[0][0]:
                    move[0].reverse()
                board_copy.insert(0, move[0])
            score = minimax_ab(board_copy, pieces_copy, depth + 1, alpha, beta, False)
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score

    else:
        best_score = sys.maxsize - 1
        possible_moves = get_other_player_possible_moves(board_pieces, computer_pieces)
        if len(possible_moves) == 0:
            return depth
        for move in possible_moves:
            board_copy = board_pieces.copy()
            pieces_copy = computer_pieces.copy()
            if move[1] == RIGHT:
                if len(board_copy) > 0 and move[0][1] == board_copy[-1][-1]:
                    move[0].reverse()
                board_copy.append(move[0])
            else:
                if len(board_copy) > 0 and move[0][0] == board_copy[0][0]:
                    move[0].reverse()
                board_copy.insert(0, move[0])
            score = minimax_ab(board_copy, pieces_copy, depth + 1, alpha, beta, True)
            best_score = min(score, best_score)
            beta = min(alpha, score)
            if beta <= alpha:
                break
        return best_score
