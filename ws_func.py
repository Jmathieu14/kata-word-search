# Author: Jacques Mathieu
# Created on 9/2/2019 at 4:49 PM
# Part of the kata-word-search project
# Contains functions necessary to find locations of words in given letter matrix

import utility as util


class WordSearchPuzzle:

    def __init__(self, path):
        self.path = path
        self.load_words()
        self.load_matrix()

    def load_words(self):
        w_list_as_str = util.get_first_line(self.path)
        self.words = w_list_as_str.split(",")
        words_len = self.words.__len__()
        # Remove new line character from end and/or any extra whitespace from end or start
        self.words[words_len-1] = self.words[words_len-1].strip()
        self.words[0] = self.words[0].strip()

    def load_matrix(self):
        self.matrix = []
        line_list = util.get_lines_from_file(self.path, ignore_header=True)
        for line in line_list:
            line_as_arr = line.split(",")
            l_arr_len = line_as_arr.__len__()
            # Remove new line character from end and/or any extra whitespace from end or start
            line_as_arr[l_arr_len-1] = line_as_arr[l_arr_len-1].strip()
            line_as_arr[0] = line_as_arr[0].strip()
            self.matrix.append(line_as_arr)

    # Return the matrix in a readable string format
    def matrix_as_str(self, extra_tab=False):
        # Placeholder for our tab character
        tab_ph = "\t"
        # Add extra tab if specified
        if extra_tab:
            tab_ph = tab_ph + "\t"
        matrix_s = "["
        last_row = self.matrix.__len__() - 1
        last_row = self.matrix[last_row]
        for row in self.matrix:
            matrix_s = matrix_s + "\n" + tab_ph + str(row)
            if row != last_row:
                matrix_s = matrix_s + ","
        # Add tab to end square bracket if specified
        if extra_tab:
            return matrix_s + "\n\t]"
        else:
            return matrix_s + "\n]"

    def __str__(self):
        return "WordSearchPuzzle {\n" + \
               "\n\tPath: " + self.path + ", " + \
               "\n\tWords: " + str(self.words) + ", " + \
               "\n\tMatrix: " + self.matrix_as_str(extra_tab=True) + \
               "\n\n}"


# Solve the word search given the words to find in the given puzzle matrix
# words: list of strings representing the words to find
# puzzle_matrix: a multidimensional array representing the positions of each letter in the
# matrix for the word search problem
def solve_word_search(words, puzzle_matrix):
    return None
