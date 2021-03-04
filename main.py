from game import TicTacToe       
from agent import Agent, train
from player_type import Player
from q_holder import QTable
import multiprocessing
import time

if __name__ == '__main__':
    table = QTable()

    iterations = 500_000_000
    debug = False
    do_training = True
    if do_training is True:
        processes = []
        splits = 1
        for i in range(splits):
            p = multiprocessing.Process(target=train, args=(debug, iterations/splits, table,))
            processes.append(p)
            p.start()
            
        for process in processes:
            process.join()
    else:
        game = TicTacToe()
        ai1 = Agent(True, table)
        table.load_q_table()
        while True:
            print()
            game.print_board()

            if game.is_board_full() or game.get_winner():
                if game.get_winner():
                    print(game.get_winner(), "has won!")
                else:
                    print("It's a tie!")
                restart = input("Do you want to restart? (Y/n) ")
                if restart == "n":
                    break
                else:
                    game.reset()
                    continue

            if game.get_player() is Player.TWO:
                field = input(str(game.get_player(human=True)) + " it's your turn! Input a field between 1-9: ")
            else:
                ai1.iterate(game, False, True)
                continue

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

