# this project has to be run in codeskulptor.org
"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists
def remove_duplicates(lst):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(lst) >= 2:
        if lst[0] != lst[1]:
            return [lst[0]] + remove_duplicates(lst[1:])
        else:
            return remove_duplicates(lst[1:])
    return lst


def intersect(lst1, lst2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both lst1 and lst2.

    This function can be iterative.
    """
    if len(lst1) > 0:
        if lst1[0] in lst2:
            return [lst1[0]] + intersect(lst1[1:], lst2)
        return intersect(lst1[1:], lst2)
    return []


# Functions to perform merge sort
def merge(lst1, lst2):  # O(n1 + n2) Time and O(n1 + n2) Extra Space
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    new_lst = []

    counter_i, counter_j, = 0, 0
    while counter_i < len(lst1) and counter_j < len(lst2):
        if lst1[counter_i] < lst2[counter_j]:
            new_lst.append(lst1[counter_i])
            counter_i += 1
        else:
            new_lst.append(lst2[counter_j])
            counter_j += 1

    while counter_i < len(lst1):
        new_lst.append(lst1[counter_i])
        counter_i += 1

    while counter_j < len(lst2):
        new_lst.append(lst2[counter_j])
        counter_j += 1

    return new_lst


def split_list(lst):
    """
    Split list into 2 lists of half size
    """
    return lst[:int(round(len(lst) / 2.0))], lst[int(round(len(lst) / 2.0)):]


def merge_sort(lst):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(lst) <= 1:
        return lst
    lst1, lst2 = split_list(lst)
    return merge(merge_sort(lst1), merge_sort(lst2))


def insert_letter(letter, word):
    """
    Inserts a letter in every position in word
    """
    lst = list(word)
    word_list = []
    for idx in range(len(word) + 1):
        lst.insert(idx, letter)
        word_list.append(''.join(lst))
        lst.pop(idx)
    return word_list


# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) < 1:
        return [word]
    elif len(word) == 1:
        return [word, '']
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
    res = list(rest_strings)
    for string in rest_strings:
        res.extend(insert_letter(first, string))
    return res


# print gen_all_strings('')
# print gen_all_strings('a')
# print gen_all_strings('ab')
# print gen_all_strings('abc')

# Function to load words from a file

# def load_words(filename):
#     """
#     Load word list from the file named filename.

#     Returns a list of strings.
#     """
#     return []

# def run():
#     """
#     Run game.
#     """
#     words = load_words(WORDFILE)
#     wrangler = provided.WordWrangler(words, remove_duplicates, 
#                                      intersect, merge_sort, 
#                                      gen_all_strings)
#     provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
