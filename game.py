import numpy as np

class Connect4:
    #tested and works well
    def __init__(self):

        self.row_count = 6 
        self.col_count = 7

    def get_initial_state(self):
        return np.zeros([self.row_count, self.col_count], dtype=np.uint8)
   


    def get_valid_moves(self, state):
        return [i for i in range(self.col_count) if state[0][i] == 0]


    def make_move(self, state, player, action):
        if state[0][action] != 0:
            raise "illegal move, column full"

        if action < 0 or action >= self.col_count:
            raise "action is out of range"

        for i in reversed(range(self.row_count)):
            if state[i][action] == 0:
                state[i][action] == player
                return state

        
        
    def place(self, col, player):
        #-1 denotes error
        #0 denotes move made
        if col < 0 or col > 6:
            return -1
        elif self.heights[col] >5:
            return -1
        else:
            self.board[5-self.heights[col]][col] = player
            self.heights[col] += 1
            return 0
        
            
    def print_board(self, state):
        print(f'  {" ".join([str(i) for i in range(self.col_count)])}')
        print('  ----------------')
        print(state)
        print('  ----------------')

    
    def check_win(self):
        # -1 denotes no winner yet
        # 0 denotes draw
        # 1,2 denotes respective winners
        
        
        padded = np.zeros((12,13))
        padded[3:9,3:10] = self.board
        
        for i in range(3,9):
            for j in range(3,10):
                player = padded[i][j]
                
                if player != 0:
                    #check right
                    if all([padded[i][j+x] == player for x in range(4)]):
                        return player
                    
                    #check down
                    if all([padded[i+x][j] == player for x in range(4)]):
                        return player
                    
                    #check SE
                    if all([padded[i+x][j+x] == player for x in range(4)]):
                        return player
                    
                    #check SW
                    if all([padded[i+x][j-x] == player for x in range(4)]):
                        return player
        
        if min(self.heights) == 6:
            return 0
        
                  
        return -1
    
    def score_player(self, player): # assumes no winners, which will be computed in the minimax alg
        
        score = 0
        
        padded = np.ones((12,13)) * 9
        padded[3:9,3:10] = self.board
        
        #awards one point per chip in the middle:
        score += sum([padded[x][6] == player for x in range(3,9)])
        
        
        #score 7's:
        for i in range(3,9):
            for j in range(3,10):
                
                #                     0
                #score 7's i.e. 1 1 1 0
                #               x 1
                #               1
                # normal 7
                if all(padded[i][j-x]==player and padded[i+x][j-x]==player for x in range(3)):
                    if padded[i][j+1] == 0 and padded[i-1][j+1] == 0:
                        score += 30
                #upside down 7
                if all(padded[i][j-x]==player and padded[i-x][j-x]==player for x in range(3)):
                    if padded[i][j+1] == 0 and padded[i+1][j+1] == 0:
                        score += 30
                        
                #backward 7
                if all(padded[i][j+x]==player and padded[i+x][j+x]==player for x in range(3)):
                    if padded[i][j-1] == 0 and padded[i-1][j-1] == 0:
                        score += 30
                        
                #backward and upside down 7:
                if all(padded[i][j+x]==player and padded[i-x][j+x]==player for x in range(3)):
                    if padded[i][j-1] == 0 and padded[i+1][j-1] == 0:
                        score += 30
                        
                
                #score double ended 3 in a rows! i.e. 0 1 1 1 0
                #horizontal
                if all([padded[i][j+x] == player for x in range(3)]):
                    if padded[i][j-1] == 0 and padded[i][j+3] == 0:
                        score += 30
                        
                #vertical
                if all([padded[i+x][j] == player for x in range(3)]):
                    if padded[i-1][j] == 0 and padded[i+3][j] == 0:
                        score += 30
                    
                #SE
                if all([padded[i+x][j+x] == player for x in range(3)]):
                    if padded[i-1][j-1] == 0 and padded[i+3][j+3] == 0:
                        score += 30
                    
                #SW
                if all([padded[i+x][j-x] == player for x in range(3)]):
                    if padded[i-1][j+1] == 0 and padded[i+3][j-3] == 0:
                        score += 30 
                
                #check for windows with holes i.e. 1 0 1 1
                h_window = np.array([padded[i][j+x] for x in range(4)])
                v_window = np.array([padded[i+x][j] for x in range(4)])
                se_window = np.array([padded[i+x][j+x] for x in range(4)])
                sw_window = np.array([padded[i+x][j-x] for x in range(4)])
                windows = [h_window, v_window, se_window, sw_window]
                
                for window in windows:
                    player_count = sum(window == player)
                    empty_count = sum(window==0)
                    
                    if player_count== 3 and empty_count == 1:
                        score += 10
                    elif player_count == 2 and empty_count == 2:
                        score += 2
        
        return score
    
    
    def score(self):
        score = 0
        score += self.score_player(1)
        score -= self.score_player(2)
        return score
        