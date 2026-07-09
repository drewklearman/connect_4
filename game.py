import numpy as np

class Connect4:
    #tested and works well
    def __init__(self):

        self.row_count = 6 
        self.col_count = 7
        self.wc = 4 #amount in a row needed to win

    def get_initial_state(self):
        return np.zeros([self.row_count, self.col_count])
   

    def get_valid_moves(self, state):
        return [state[0, i] == 0 for i in range(self.col_count)]


    def make_move(self, state, player, action):
        if state[0][action] != 0:
            raise "illegal move, column full"

        if action < 0 or action >= self.col_count:
            raise "action is out of range"

        new_state = state.copy()

        for i in reversed(range(self.row_count)):
            if new_state[i, action] == 0:
                new_state[i, action] = player
                return new_state
        
            
    def print_board(self, state):
        print(f'  {" ".join([str(i) for i in range(self.col_count)])}')
        print('  ----------------')
        print(state.astype(int))
        print('  ----------------')

    
    def check_win(self, state, action) -> bool:
        """True denotes a win, False means no winners"""

        col = action
        row = None
        player = None

        # the last move is the topmost occupied cell in the played column
        for i in range(self.row_count):
            if state[i, col] != 0:
                player = state[i, col]
                row = i
                break

        if player is None:
            return False

        def count_dir(dr, dc):
            """Count consecutive `player` cells starting one step away in (dr, dc)."""
            count = 0
            r, c = row + dr, col + dc
            while 0 <= r < self.row_count and 0 <= c < self.col_count and state[r, c] == player:
                count += 1
                r += dr
                c += dc
            return count

        # for each axis, span = the placed piece + the run on both sides
        for dr, dc in ((1, 0), (0, 1), (1, 1), (1, -1)):
            span = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
            if span >= self.wc:
                return True

        return False


    def get_value_and_terminated(self, state, action) -> (int, bool):
        if self.check_win(state, action):
            return 1, True
        if not any(self.get_valid_moves(state)):
            return 0, True
        return 0, False


    def get_opponent(self, player):
        return player * -1
    
    
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
        