from enum import Enum

class Player(Enum):
    EMPTY = 0
    ONE = 1
    TWO = 2

win_combinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

class TicTacToe:
    board_state = [Player.EMPTY]*9
    player = Player.ONE

    def __init__(self):
        print("TicTacToe is starting")

    def reset(self):
        self.board_state = [Player.EMPTY]*9
        self.player = Player.ONE

    def input(self, field: int):
        if self.is_board_full():
            raise OverflowError("Board is full")

        if not self.is_legal_move(field):
            raise ValueError("Move is illegal")

        self.board_state[field] = self.player
        self.player = Player.ONE if self.player is Player.TWO else Player.TWO

    def is_board_full(self):
        return not any(field is Player.EMPTY for field in self.board_state)

    def is_legal_move(self, field: int):
        return self.board_state[field] is Player.EMPTY

    def get_player(self, human=False):
        if human:
            return "Player One" if self.player is Player.ONE else "Player Two"
        return self.player

    def get_winner(self):
        winner = Player.EMPTY

        for combination in win_combinations:
            combination_type = Player.EMPTY

            for index in combination:
                if self.board_state[index] is Player.EMPTY:
                    combination_type = Player.EMPTY
                    break;
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
                    

game = TicTacToe()
while True:
    print()
    game.print_board()

    if game.is_board_full() or game.get_winner():
        if game.get_winner():
            print(game.get_winner(), "has won!")
        else:
            print("It's a tie!")
        restart = input("Do you want to restart? (Y/n) ")
        if restart is "n":
            break
        else:
            game.reset()
            continue
    
    field = input(str(game.get_player(human=True)) + " it's your turn! Input a field between 1-9: ")

    try:
        field = int(field)-1
        if field < 0 or field > 8:
            raise ValueError
    except ValueError:
        print("ERROR! Please input a field number between 1-9!")
        continue
    
    try:
        game.input(field)
    except ValueError:
        print("ERROR! The field is taken")

