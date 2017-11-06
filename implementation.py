"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, NEG_INFINITY, INFINITY
from connectfour import ConnectFourBoard


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

STUDENT_ID = 20552650
AGENT_NAME = "DisConnectFour"
COMPETE = True

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    score = 0
    if board.is_game_over():
        score -= 1000
    score += board.longest_chain(board.get_current_player_id()) * 10
    # Prefer having your pieces in the center of the board.
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)

    return score
    #aise NotImplementedError


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.

# alpha_beta_search helper function: Return the minimax value of a particular board,
# given a particular depth to estimate to, with alpha beta pruning
def alpha_beta_search_find_board_value(board, depth, alpha, beta,
                                       eval_fn,
                                       get_next_moves_fn,
                                       is_terminal_fn):
    if is_terminal_fn(depth, board): # if it reaches the terminal state
        return (eval_fn(board), None) # return the estimated value that calculated by evaluation function

    best_val = (NEG_INFINITY, None) # initially, set it to NEG_INFINITY
    
    for move, new_board in get_next_moves_fn(board): # for each possible move
        # calculate the value of next child node
        val = -1 * alpha_beta_search_find_board_value(new_board, depth-1, -beta, -alpha,
                                                      eval_fn, get_next_moves_fn, is_terminal_fn)[0]
        if val > best_val[0]: # if current move gives better value than my best value so far 
            best_val = (val, move) # update the best value with the better move
        if val > alpha: # if current move gives better value than alpha
            alpha = val # update the alpha
        if alpha >= beta: # if pruning condition met
            break # alpha beta prune, do not have to visit the rest of children nodes
    return best_val

# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    """
     board is the current tree node.

     depth is the search depth.  If you specify depth as a very large number then your search will end at the leaves of trees.
     
     def eval_fn(board):
       a function that returns a score for a given board from the
       perspective of the state's current player.
    
     def get_next_moves(board):
       a function that takes a current node (board) and generates
       all next (move, newboard) tuples.
    
     def is_terminal_fn(depth, board):
       is a function that checks whether to statically evaluate
       a board/node (hence terminating a search branch).
    """

    # calling helper to get the best next move 
    best_val = alpha_beta_search_find_board_value(board, depth, NEG_INFINITY, INFINITY, eval_fn,
                                                  get_next_moves_fn, is_terminal_fn)
        
    if 1: # for tracing purpose
        print("DisConnectFour: Decided on column {} with rating {}".format(best_val[1], best_val[0]))

    return best_val[1]
    #raise NotImplementedError


# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=4, eval_fn=focused_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)


# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

def better_evaluate(board):
    score = 0 # initially set to 0
    if board.is_win() == board.get_current_player_id(): # if win, then +1000
        score += 1000
    elif board.is_win() == board.get_other_player_id(): # if lose, then -1000
        score -= 1000 
    # Prefer having 3 in a row than 2 in a row than 1 in a row
    # Prefer having a chain in the center
    for chain in board.chain_cells(board.get_current_player_id()):
        score += len(chain)*len(chain)
        for point in chain:
            score -= 5*abs(3-point[1]) # scale to 5, place in center ones have more chance to win
    for chain in board.chain_cells(board.get_other_player_id()):
        score -= len(chain)*len(chain)*len(chain) # because defense is more important
        for point in chain:
            score += 7*abs(3-point[1]) # scale to 5, place in center ones have more chance to win
    return score
    #raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
#def my_player(board):
#    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=5)

# NOTE:
# set the depth to be 6, at the beginning of each game, it might be slow, take about 5-6s, but will be much
#   faster as the process of the game.
my_player = lambda board: alpha_beta_search(board, depth=6, eval_fn=better_evaluate)
