#!/usr/bin python3.5
"""
Project 4 of Algorithmic thinking (part 2) course
Fundamentals of computing (Rice university) Specialization
https://www.coursera.org/specializations/computer-fundamentals
"""


# Matrix Functions
def build_scoring_matrix(alphabet,
                         diag_score,
                         off_diag_score,
                         dash_score):
    """
    Takes as input a set of characters alphabet
    and three scores diag_score, off_diag_score, and dash_score.
    Returns a dictionary of dictionaries whose entries
    are indexed by pairs of characters in alphabet plus '-'.
    The score for any entry indexed by one or more dashes is dash_score.
    The score for the remaining diagonal entries is diag_score.
    The score for the remaining off-diagonal entries is off_diag_score.
    """

    alphabet = alphabet.copy()
    alphabet.add('-')
    mat = {char_i: {char_j: (diag_score if (char_i == char_j and
                                            all([char_i != '-',
                                                 char_j != '-']))
                             else (dash_score if any([char_i == '-',
                                                      char_j == '-'])
                                   else off_diag_score))
                    for char_j in alphabet}
           for char_i in alphabet}

    return mat


def normalize(val, flag):
    """
    determines whether to compute the local or global alignment.
    """
    if flag:
        return val
    return max(val, 0)


def compute_alignment_matrix(seq_x,
                             seq_y,
                             scoring_matrix,
                             global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements
    share a common alphabet with the scoring matrix scoring_matrix.
    Returns the alignment matrix for seq_x and seq_y.
    If global_flag is True, global alignment is computed, otherwise local alignment.
    """
    seq_x_len = len(seq_x) + 1  # +1 is for the '-' to be added to the sequence
    seq_y_len = len(seq_y) + 1
    mat = [[0 for col in range(seq_y_len)] for row in range(seq_x_len)]

    for row in range(1, seq_x_len):
        mat[row][0] = normalize(mat[row - 1][0] +
                                scoring_matrix[seq_x[row - 1]]['-'],
                                global_flag)

    for col in range(1, seq_y_len):
        mat[0][col] = normalize(mat[0][col - 1] +
                                scoring_matrix['-'][seq_y[col - 1]],
                                global_flag)

    for row in range(1, seq_x_len):
        for col in range(1, seq_y_len):
            mat[row][col] = normalize(max(mat[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]],
                                          mat[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-'],
                                          mat[row][col - 1] + scoring_matrix['-'][seq_y[col - 1]]),
                                      global_flag)

    return mat


# Alignment Functions
def compute_global_alignment(seq_x,
                             seq_y,
                             scoring_matrix,
                             alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet
    With the scoring matrix scoring_matrix.
    Returns a tuple of the form (score, align_x, align_y)
    where score is the score of the global alignment align_x and align_y.
    """
    idx_x = len(seq_x)
    idx_y = len(seq_y)
    algin_x = ''
    algin_y = ''
    while idx_x != 0 and idx_y != 0:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y -1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            algin_x = seq_x[idx_x - 1] + algin_x
            algin_y = seq_y[idx_y - 1] + algin_y
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
                algin_x = seq_x[idx_x - 1] + algin_x
                algin_y = '-' + algin_y
                idx_x -= 1
            else:
                algin_x = '-' + algin_x
                algin_y = seq_y[idx_y - 1] + algin_y
                idx_y -= 1

    while idx_x != 0:
        algin_x = seq_x[idx_x - 1] + algin_x
        algin_y = '-' + algin_y
        idx_x -= 1

    while idx_y != 0:
        algin_x = '-' + algin_x
        algin_y = seq_y[idx_y - 1] + algin_y
        idx_y -= 1

    score = 0
    for idx in range(len(algin_y)):
        score += scoring_matrix[algin_x[idx]][algin_y[idx]]

    return (score, algin_x, algin_y)


def compute_local_alignment(seq_x,
                            seq_y,
                            scoring_matrix,
                            alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet
    with the scoring matrix scoring_matrix.
    Returns a tuple of the form (score, align_x, align_y)
    where score is the score of the optimal local alignment align_x and align_y.
    """
    max_value_index = max(((x, (i, j))
                           for i, row in enumerate(alignment_matrix)
                           for j, x in enumerate(row)),
                          key=lambda x, *tup: x)
    idx_x = max_value_index[1][0]
    idx_y = max_value_index[1][1]
    algin_x = ''
    algin_y = ''
    while idx_x != 0 and idx_y != 0 and alignment_matrix[idx_x][idx_y] != 0:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            algin_x = seq_x[idx_x - 1] + algin_x
            algin_y = seq_y[idx_y - 1] + algin_y
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
                algin_x = seq_x[idx_x - 1] + algin_x
                algin_y = '-' + algin_y
                idx_x -= 1
            else:
                algin_x = '-' + algin_x
                algin_y = seq_y[idx_y - 1] + algin_y
                idx_y -= 1

    while idx_x != 0 and alignment_matrix[idx_x][idx_y] != 0:
        algin_x = seq_x[idx_x - 1] + algin_x
        algin_y = '-' + algin_y
        idx_x -= 1

    while idx_y != 0 and alignment_matrix[idx_x][idx_y] != 0:
        algin_x = '-' + algin_x
        algin_y = seq_y[idx_y - 1] + algin_y
        idx_y -= 1

    score = 0
    for idx in range(len(algin_y)):
        score += scoring_matrix[algin_x[idx]][algin_y[idx]]

    return (score, algin_x, algin_y)
