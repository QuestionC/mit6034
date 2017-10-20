# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.
import itertools
def focused_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_win() == board.get_current_player_id():
        return 1000
    if board.is_win() == board.get_other_player_id():
        return -1000
    
    score = board.longest_chain(board.get_current_player_id()) * 10
    # Prefer having your pieces in the center of the board.
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)

    return score

## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
# run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

# For a given move, evaluate as far as you can using the provided alpha_beta values.
# Return the best val, or the one which caused you to abort using alpha beta rules.
def alpha_beta_board_val(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, my_bottom, enemy_bottom):
    # Leaf node just return val
    if is_terminal_fn(depth, board):
        return (None, eval_fn(board))

    my_best_val = None

    # Otherwise, we evaluate each of the enemy moves and our val is the negative of that
    for move, new_board in get_next_moves_fn(board):
        enemy_val = alpha_beta_board_val(new_board, depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, enemy_bottom, my_bottom)
        if enemy_val == None:
            #  It was pruned for some reason
            continue

        enemy_score = enemy_val[1]
        my_score = -enemy_score

        if enemy_bottom != None and enemy_score < enemy_bottom:
            # This move would cause a bad board state for enemy, but he has better choices and won't let me reach this branch, so get out now
            return (move, my_score)
    
        if my_bottom == None or my_score > my_bottom:
            # Nice choice, we have a new bottom
            # This will make future searches more efficient
            my_bottom = my_score

        if my_best_val == None or my_score > my_best_val[1]:
            my_best_val = (move, my_score)

    return my_best_val

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    return alpha_beta_board_val(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, None, None)[0]    

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
# run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.
def better_evaluate(board):
    if board.is_win() == board.get_current_player_id():
        return 1000
    if board.is_win() == board.get_other_player_id():
        return -1000
    
    score = board.longest_chain(board.get_current_player_id()) * 10

    # Prefer having your pieces in the center of the board.
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)

    for x in range(7):
        for y in reversed(range(6)):
            # Skip the sides
            if x == 0 or x == 6:
                continue

            is_top = y == 0
            is_bottom = y == 5

            neighbors = [ 
                    ((y, x - 1), (y, x + 1)),
                    ((y - 1, x - 1), (y + 1, x + 1)),
                    ((y + 1, x - 1), (y - 1, x + 1))
                    ]

            for p,n in neighbors:

                if is_top or is_bottom:
                    # Do not process diagonals on top or bottom row.
                    if p[0] != y:
                        continue

                if board.get_cell(*p) == board.get_cell(*n):
                    if board.get_cell(*p) == board.get_current_player_id():
                        score += 2
                    elif board.get_cell(*p) == board.get_other_player_id():
                        score -= 2

    return score

# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
# run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = 20
WHAT_I_FOUND_INTERESTING = "Minmax tree"
WHAT_I_FOUND_BORING = "Connect 4 state programming"
NAME = "James"
EMAIL = "no"

