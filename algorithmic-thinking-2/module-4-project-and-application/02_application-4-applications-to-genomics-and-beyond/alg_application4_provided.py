#!/usr/bin python3.5
"""
Provide code and solution for Application 4
"""

import math
import random

import matplotlib.pyplot as plt
# import alg_project4_solution as student
import matrix_and_alignment_func as student

# URLs for data files
PAM50 = "alg_PAM50.txt"
HUMAN_EYELESS = "alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS = "alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX = "alg_ConsensusPAXDomain.txt"
WORD_LIST = "assets_scrabble_words3.txt"


###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = open(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = open(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = open(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print("Loaded a dictionary with", len(word_list), "words")
    return word_list


def delete_all(string, key='-'):
    new_string = ''
    idx = string.find(key)
    if idx == -1:
        return string
    new_string += string[:idx]
    new_string += delete_all(string[idx + 1:], key)
    return new_string


def similarity_percentage(seq, consensus):
    seq = delete_all(seq, '-')
    alignment_matrix = student.compute_alignment_matrix(seq,
                                                        consensus,
                                                        scoring_matrix,
                                                        True)
    score, seq_align, con_align = student.compute_global_alignment(seq,
                                                                   consensus,
                                                                   scoring_matrix,
                                                                   alignment_matrix)
    matches = 0
    align_len = len(seq_align)
    for idx in range(align_len):
        if seq_align[idx] == con_align[idx]:
            matches += 1

    return float(matches) / align_len


def shuffle_sequence(seq):
    seq = list(seq)
    random.shuffle(seq)
    return ''.join(seq)


def generate_null_distribution(seq_x,
                               seq_y,
                               scoring_matrix,
                               num_trials):
    scoring_distribution = {}
    for dummy_i in range(num_trials):

        rand_y = shuffle_sequence(seq_y)
        alignment_matrix = student.compute_alignment_matrix(seq_x,
                                                            rand_y,
                                                            scoring_matrix,
                                                            False)
        alignment = student.compute_local_alignment(seq_x,
                                                    rand_y,
                                                    scoring_matrix,
                                                    alignment_matrix)
        try:
            scoring_distribution[alignment[0]] += 1
        except KeyError:
            scoring_distribution[alignment[0]] = 1

    return scoring_distribution


human_eyeless_protein = read_protein(HUMAN_EYELESS)
fruitfly_eyeless_protein = read_protein(FRUITFLY_EYELESS)
scoring_matrix = read_scoring_matrix(PAM50)


score, align_x, align_y = student.compute_local_alignment(human_eyeless_protein,
                                                          fruitfly_eyeless_protein,
                                                          scoring_matrix,
                                                          student.compute_alignment_matrix(human_eyeless_protein,
                                                                                           fruitfly_eyeless_protein,
                                                                                           scoring_matrix,
                                                                                           False))

consensus_PAX_domain = read_protein(CONSENSUS_PAX)


# dist = generate_null_distribution(human_eyeless_protein,
#                                   fruitfly_eyeless_protein,
#                                   scoring_matrix,
#                                   1000)
def edit_dist(seq_x, seq_y, scoring_matrix):
    alignment_matrix = student.compute_alignment_matrix(seq_x,
                                                        seq_y,
                                                        scoring_matrix,
                                                        True)
    return len(seq_x) + len(seq_y) - student.compute_global_alignment(seq_x,
                                                                      seq_y,
                                                                      scoring_matrix,
                                                                      alignment_matrix)[0]


def check_spelling(checked_word, dist, word_list):
    scoring_matrix = student.build_scoring_matrix(set(list('abcdefghijklmnopqrstuvwxyz')), 2, 1, 0)
    words = set([])
    for word in word_list:
        if edit_dist(checked_word, word, scoring_matrix) <= dist:
            words.add(word)
    return words


word_list = read_words(WORD_LIST)

humble = check_spelling('humble', 1, word_list)
firefly = check_spelling('firefly', 2, word_list)
