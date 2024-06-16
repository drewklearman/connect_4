from stratedgy import retrieve_stratedgy
from board import board, gamestate
    

def main():
    num_layers = 0
    input1 = input("choose strat 1")
    if input1 == 'minimax':
        num_layers = input('how many layers')
    strat_1 = retrieve_stratedgy(input1, num_layers)
    
    while strat_1 == -1:
        print("invalid stratedgy")
        input1 = input("choose strat 1")
        if input1 == 'minimax':
            num_layers = int(input('how many layers'))
        strat_1 = retrieve_stratedgy(input1, num_layers)

    input2 = input("choose strat 2")
    if input2 == 'minimax':
        num_layers = int(input('how many layers'))
    strat_2 = retrieve_stratedgy(input2, num_layers)
    
    while strat_2 == -1:
        print("invalid stratedgy")
        input1 = input("choose strat 2")
        if input2 == 'minimax':
            num_layers = input('how many layers')
        strat_2 = retrieve_stratedgy(input2, num_layers)

    game = gamestate(strat_1, strat_2)
    game.play()

if __name__ == "__main__":
    main()