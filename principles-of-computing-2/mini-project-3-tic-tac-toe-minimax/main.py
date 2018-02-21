# this project has to be run in codeskulptor.org
"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    score = None
    if board.check_win() is not None:
        if board.check_win() == provided.DRAW:
            score = 0
        else:
            score = SCORES[board.check_win()]
        return (score, (-1, -1))

    empty_squares = board.get_empty_squares()

    results = []

    for move in empty_squares:
        cloned = board.clone()
        cloned.move(*move, player=player)
        result = mm_move(cloned, provided.switch_player(player))

        results.append((result[0], move))

    if len(results) > 1:
        # multiplying the results by the current player to get the scores of this level
        scores = [SCORES[player] * results[idx][0] for idx in range(len(results))]
        max_val = max(scores)
        max_val_indx = scores.index(max_val)

        results = [results[max_val_indx]]
    return results[0]


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
