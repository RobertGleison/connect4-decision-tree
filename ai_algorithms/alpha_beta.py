from game import constants as c, game_logic as game
from heuristics import heuristic as h
import time, logging, numpy as np


NODES_VISITED = 1
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def alpha_beta(board: np.ndarray) -> int:
    start_time = time.time()
    global NODES_VISITED
    NODES_VISITED = 1
    best_score = float('-inf')
    best_move = -1
    depth_limit = 5
    children = get_children(board, c.AI_PIECE)

    for col in range(c.COLUMNS):
        child_board = children[col]
        if not game.is_valid(child_board, col): continue
        current_score = min_value(child_board, 0, float('-inf'), float('+inf'), depth_limit, c.HUMAN_PIECE)
        if current_score > best_score:
            best_move = col
            best_score = current_score
        logging.info(f"Number of nodes visited = {NODES_VISITED}")
        logging.info(f"Score = {best_score}")
    end_time = time.time()
    logging.info(f"Tempo de resposta = {end_time-start_time}")
    
    return best_move


def max_value(board: np.ndarray, depth: int, alpha: int, beta: int, depth_limit: int, piece: int) -> int:
    max_eval = float('-inf')
    childrens = get_children(board, c.AI_PIECE)

    if game.winning_move(board, piece) or depth == depth_limit:
        # return te.evaluate_board(board)
        return h.calculate_board_score(board, c.AI_PIECE, c.HUMAN_PIECE)

    for move in childrens:
        score = min_value(move, depth+1, alpha, beta, depth_limit, c.AI_PIECE)
        global NODES_VISITED
        NODES_VISITED+=1
        score = max(score, max_eval)
        alpha = max(alpha, score)
        if beta <= alpha: break
    # logging.info(f"Score: {score}")
    return score


def min_value(board: np.ndarray, depth: int, alpha: int, beta: int, depth_limit: int, piece: int) -> int:
    if game.winning_move(board, piece) or depth == depth_limit:
        # return te.evaluate_board(board)
        return h.calculate_board_score(board, c.AI_PIECE, c.HUMAN_PIECE)
    min_eval = float('+inf')
    childrens = get_children(board, c.HUMAN_PIECE)
    for move in childrens:
        score = max_value(move, depth+1, alpha, beta, depth_limit, c.HUMAN_PIECE)
        global NODES_VISITED
        NODES_VISITED+=1
        score = min(score, min_eval)
        beta = min(beta, score)
        if beta <= alpha: break
    # logging.info(f"Score: {score}")
    return score


def get_children(board, piece: int) -> list:
    childrens = []
    for col in range(c.COLUMNS):
        copy_board = game.simulate_move(board, piece, col)
        childrens.append(copy_board)
    return childrens
