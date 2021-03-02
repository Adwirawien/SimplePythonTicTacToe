from game import TicTacToe
                    

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

