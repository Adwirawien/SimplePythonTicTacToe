from player_type import Player
import zlib
import random

win_combinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

class TicTacToe:
    board_state = [Player.EMPTY]*9
    player = Player.ONE

    def __init__(self):
        print("TicTacToe is starting")

    def reset(self):
        self.board_state = [Player.EMPTY]*9
        self.player = Player.ONE if random.randint(0,2) == 1 else Player.TWO

    def get_hash(self):
        return zlib.adler32(bytes(''.join(str(p) for p in self.board_state), 'utf-8'))

    def input(self, field: int):
        if self.is_board_full():
            raise OverflowError("Board is full")

        if not self.is_legal_move(field):
            raise ValueError("Move is illegal")

        self.board_state[field] = self.player
        self.player = Player.ONE if self.player is Player.TWO else Player.TWO

    def is_board_full(self):
        return not any(field is Player.EMPTY for field in self.board_state)

    '''returns all empty fields'''
    def get_legal_moves(self):
        return [i for i in range(len(self.board_state)) if self.board_state[i] == Player.EMPTY]

    '''evaluates if move is legal'''
    def is_legal_move(self, field: int):
        return self.board_state[field] is Player.EMPTY

    '''returns current player, human can make it human readable'''
    def get_player(self, human=False):
        if human:
            return "Player One" if self.player is Player.ONE else "Player Two"
        return self.player

    '''checks if any player is in winning combination'''
    def get_winner(self):
        winner = Player.EMPTY

        for combination in win_combinations:
            combination_type = Player.EMPTY

            for index in combination:
                if self.board_state[index] is Player.EMPTY:
                    combination_type = Player.EMPTY
                    break
                elif combination_type is Player.EMPTY or combination_type is self.board_state[index]:
                    combination_type = self.board_state[index]
                else:
                    combination_type = Player.EMPTY
                    break
            
            if combination_type is not Player.EMPTY:
                winner = combination_type
                break
            
        if winner is not Player.EMPTY:
            return winner
        else:
            return None
    
    '''prints board readable to humans'''
    def print_board(self):
        for index, field in enumerate(self.board_state):
            if field is Player.EMPTY:
                print('-', end='')
            if field is Player.ONE:
                print('X', end='')
            if field is Player.TWO:
                print('O', end='')

            if (index+1) % 3 == 0:
                print()
            else:
                print(" | ", end='')
