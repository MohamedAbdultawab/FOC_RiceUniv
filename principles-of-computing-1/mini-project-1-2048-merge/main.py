"""
Merge function for 2048 game.
"""


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """

    result = slide_zeros(line)
    for num in range(len(result)):

        if num != len(result) - 1:
            if result[num] != 0 and result[num] == result[num + 1]:
                result[num] *= 2
                result[num + 1] = 0

    return slide_zeros(result)


def slide_zeros(line):
    """
    Function that slide non-zero entries to the beginning of list.
    """

    result = [0 for dummy_num in range(len(line))]
    index = 0

    for num in line:
        if num != 0:
            result[index] = num
            index += 1

    return result
