import time, math, numpy as np, random
from dataclasses import dataclass
from game import constants as c, game_logic as game
from math import sqrt, log


def mcts(board: np.ndarray) -> int:
    """Should return the best column option, chose by mcts"""
    node = Node(board)
    mcts = MCTS(node)
    mcts.root = node
    # Set the time limit in seconds
    column =  mcts.search(2)
    return column

class Node:
    def __init__(self, board) -> None:
        self.board = board
        self.parent = None
        self.children = []
        self.exploration_constant = sqrt(2)
        self.visits = 0
        self.wins = 0

    def add_child(self, child) -> bool:
        #se o estado já estiver como filho
        if any(child.board == node.board for node in self.children):
            return False

        self.children.append(child)
        child.parent = self
        return True
    
    def add_children(self , children:list) -> None:
        for child in children:
            self.add_child(child)

    def uct(self) -> float:
        if self.visits == 0:
            return float('inf')
        exploitation = self.wins / self.visits
        exploration = self.exploration_constant * sqrt(2 * log((self.parent.visits) / self.visits), math.e)  if self.parent else 0
        return exploitation + exploration
    
    def win_probability(self) -> float:
        return self.wins / self.visits



class MCTS:
    def __init__(self, root: Node) -> None:
        self.root = root

    def best_child(self , node: Node) -> Node:
        best_child = []
        best_score = float('-inf')
        for child in node.children:
            score = child.uct()
            if score > best_score:
                best_child = [child]
                best_score = score
            elif score == best_score:
                best_child.append(child)
        return random.choice(best_child)
    
    def biggest_win_probability(self):
        best_child = -1
        best_score = float('-inf')
        col = 0 
        best_col = 0
        for child in self.root.children:
            # if not game.is_valid(child, col): continue
            col+=1
            score = child.win_probability()
            if score > best_score:
                best_score = score
                best_col=col

        # print(col)
        return best_col

    def update_state(self , board: Node) -> None:
        self.root = Node(board)
        
    def select(self) -> Node:
        node = self.root
        while len(node.children) > 0:
            node = self.best_child(node)
        return node

    def expand(self , node: Node) -> Node:
        child_moves = game.avaiable_moves(node.board)
        
        for col in child_moves:
            child_state = game.simulate_move(node.board, c.AI_PIECE, col)
            node.add_child(Node(child_state))

        return random.choice(node.children)
        
    def rollout(self , node: Node) -> bool:
        board = node.board.boardCopy()
        while not game.winning_move(board, c.AI_PIECE):
            board = self.rollout_policy(board)
        # retorna true se o jogo ganhou
        return True

    def rollout_policy(self , board: Node):
        col = random.choice(game.avaiable_moves(board))
        board = game.simulate_move(board, c.AI_PIECE, col)
        return board

    def back_propagation(self, node: Node, winner_symbol: bool) -> None:
        while node:
            node.visits += 1
            if game.winning_move(node.board, c.AI_PIECE):
                node.wins += 1
            node = node.parent

    def search(self, max_time:int) -> Node:
        start_time = time.time()
        simulations = 0
        while time.time() - start_time < max_time:
            simulations += 1
            selected = self.select()
            result = game.winning_move(selected.board, c.AI_PIECE)
            if isinstance(result, bool): 
                expanded = self.expand(selected)
                result = self.rollout(expanded)
            self.back_propagation(selected, result)
            
        # print('Foram feitas ' + str(simulations) + ' simulações.')
        return self.biggest_win_probability()
