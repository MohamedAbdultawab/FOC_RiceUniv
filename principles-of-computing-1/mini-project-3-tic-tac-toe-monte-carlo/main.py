"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10        # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player):
    """
    Some Docs
    """

    while not board.check_win():
        board.move(*random.choice(board.get_empty_squares()),
                   player=player)
        player = provided.switch_player(player)
    return


def mc_update_scores(scores, board, player):
    """"
    Some Docs
    """

    grid = [(dummy_row, dummy_col) for dummy_col in range(board.get_dim()) for dummy_row in range(board.get_dim())]

    if board.check_win():
        if board.check_win() == provided.DRAW:
            return
        elif board.check_win() == player:
            for row, col in grid:
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER
        elif board.check_win() == provided.switch_player(player):
            for row, col in grid:
                if board.square(row, col) == player:
                    scores[row][col] -= SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER
    return


def get_best_move(board, scores):
    """
    Some Docs
    """
    max_score = None

    if not (len(board.get_empty_squares()) == 0):

        for row, col in board.get_empty_squares():
                if scores[row][col] > max_score:
                    max_score = scores[row][col]
                    max_index = (row, col)

    return max_index

    # max_val = max(map(max, scores))
    # print max_val
    # max_val_indices = []
    # for row, col in board.get_empty_squares():
    #     if scores[row][col] == max_val:
    #         max_val_indices.append((row, col))
    # return random.choice(max_val_indices)


def mc_move(board, player, trials):
    """
    Some Docs
    """

    scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]

    for dummy_trial in range(trials):
        cloned_board = board.clone()
        mc_trial(cloned_board, player)
        mc_update_scores(scores, cloned_board, player)
    return get_best_move(board, scores)


provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
