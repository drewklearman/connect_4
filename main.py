from stratedgy import retrieve_stratedgy
from board import board
import time


class gamestate():
    def __init__(self, strat1, strat2, verbose=True):
        self.board = board(verbose)
        self.turn = 1
        self.strategies = [strat1, strat2]
        self.verbose = verbose
    
    
            
    def play(self):
        if self.verbose:
            self.board.print_board()
        while(self.board.check_win() == -1):  
            if self.verbose:
                time.sleep(2)
            move = self.strategies[self.turn-1](self.board, self.turn)
            if self.verbose:
                print('player', self.turn, 'plays column',move)
            error_check = self.board.place(move, self.turn)
            
            if not error_check:
                self.turn = 1 + (self.turn % 2)
                if self.verbose:
                    self.board.print_board()
          
        winner = int(self.board.check_win())
        if self.verbose:
            if winner == 0:
                print('game is a draw')   
            else:
                print("player", winner, "wins!")
                
        print(winner)
        
        return winner
    

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
            num_layers = input('how many layers')
        strat_1 = retrieve_stratedgy(input1, num_layers)

    input2 = input("choose strat 2")
    if input2 == 'minimax':
        num_layers = input('how many layers')
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