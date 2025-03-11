import numpy as np

def random_strat(board, player):
    return np.random.choice(board.get_valid_moves())

def manual_strat(board, player):
    return int(input("which column do you select?"))

def custom_minimax(layers):
    def minimax(board, player):
        def alg(board, depth, alpha, beta, player): # returns (optimal column, value achieved)
        
            winner = board.check_win()
            if winner == 1:
                return (None, 1000000)
            elif winner == 2:
                return (None, -1000000)
            elif winner == 0:
                return (None, 0)
            elif depth == 0:
                return (None, board.score())

            if player==1: #Maximizer

                opt_value = -np.inf
                for col in board.get_valid_moves():
                    copy = board.copy()
                    copy.place(col, player)
                    _, value = alg(copy, depth - 1, alpha, beta, 1 + (player % 2))

                    if value > opt_value:
                        opt_value = value
                        opt_col = col

                    #pruning for increased speed    
                    alpha = max(alpha, opt_value)
                    if alpha >= beta:
                        break
                    
                    
                return (opt_col, opt_value)

            else: #minimizer

                opt_value = np.inf
                for col in board.get_valid_moves():
                    copy = board.copy()
                    copy.place(col, player)
                    a= depth - 1
                    b = alpha
                    c = beta
                    d = 1 + (player % 2)
                    _, value = alg(copy, depth - 1, alpha, beta, 1 + (player % 2))

                    if value < opt_value:
                        opt_value = value
                        opt_col = col
                    
                    #pruning for increased speed    
                    beta = min(beta, opt_value)
                    if alpha >= beta:
                        break

                return (opt_col, opt_value)

        return alg(board, int(layers), -np.inf, np.inf, player)[0]
    
    return minimax


def retrieve_stratedgy(name, layers=4):
    if name == 'manual':
        return manual_strat
    elif name == 'random':
        return random_strat
    elif name == 'minimax':
        return custom_minimax(layers)
    else:
        return -1
