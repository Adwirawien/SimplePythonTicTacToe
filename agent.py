from game import TicTacToe
from player_type import Player
import time
import math
import random
import pickle

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def random_weighted_boolean(percent=50):
    return random.randrange(100) < percent

class Agent:
    ai = False # will do random moves if set to False
    learning_rate = 0.2
    decay_gamma = 0.3

    q_table = None
    history = []

    def __init__(self, ai: bool, q_table):
        self.ai = ai
        self.q_table = q_table

    def reset_history(self):
        self.history = []

    def reward(self, reward):
        for m in self.history:
            if m['hash'] not in self.q_table.table:
                self.q_table.table[m['hash']] = {}
            if m['move'] not in self.q_table.table[m['hash']]:
                self.q_table.table[m['hash']][m['move']] = 0

            self.q_table.table[m['hash']][m['move']] += self.learning_rate * (self.decay_gamma * reward - self.q_table.table[m['hash']][m['move']])
            reward = self.q_table.table[m['hash']][m['move']]
        self.history = []

    def iterate(self, game: TicTacToe, train: bool=False, print_q: bool=False):
        moves = game.get_legal_moves()
        move = self.random_move(moves)
        field_hash = game.get_hash()

        if self.ai:
            move = self.get_optimal_move(moves, field_hash, print_q, train)
            self.history = [{"hash": field_hash, "move": str(move)}] + self.history
        
        game.input(int(move))
    
    def random_move(self, moves):
        return moves[random.randint(0, len(moves)-1)]
    
    def get_optimal_move(self, moves, field_hash: int, print_q: bool, training: bool):
        if field_hash in self.q_table.table and (not random_weighted_boolean(30) or training):
            if print_q:
                print("found hash", field_hash)
            optimal_move = {"value": 0, "field": self.random_move(moves)}
            entry = self.q_table.table[field_hash]
            for m in moves:
                if str(m) in entry and entry[str(m)] >= optimal_move['value']:
                    optimal_move = {"value": entry[str(m)], "field": str(m)}

            if print_q is True:
                for i in range(9):
                    print('%.2f' % entry[str(i)] if str(i) in entry else '0.00', end='')

                    if (i+1) % 3 == 0:
                        print()
                    else:
                        print(" | ", end='')

            return optimal_move['field']
        else:
            if print_q:
                print("choosing random move")
            return self.random_move(moves)



def train(debug, iterations, table):
    game = TicTacToe()
    ai1 = Agent(True, table)
    ai2 = Agent(True, table)

    try:
        while True:
            if iterations == 0:
                table.save_q_table()
                break

            if iterations > 0:
                #if iterations < 50:
                #    debug = True


                iterations -= 1
                if iterations % 100_000 == 0:
                    print(iterations)
                    print("q_table len", len(table.table))
                
                if game.is_board_full() or game.get_winner():
                    if game.get_winner() is Player.ONE:
                        ai1.reward(1)
                        ai2.reward(0)
                    elif game.get_winner() is Player.TWO:
                        ai1.reward(0)
                        ai2.reward(1)
                    else:
                        ai1.reward(0.1)
                        ai2.reward(0.5)
                    game.reset()

                    ai1.reset_history()
                    ai2.reset_history()
                    continue

                ai1.iterate(game, print_q=debug) if game.get_player() == Player.ONE else ai2.iterate(game)
                if debug:
                    print()
                    print(game.get_hash())
                    game.print_board()
                    time.sleep(0.1)

                continue 
    except KeyboardInterrupt:
            table.save_q_table()
            exit()
