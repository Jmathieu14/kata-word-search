# Author: Jacques Mathieu
# Created on 9/2/2019 at 4:49 PM
# Part of the kata-word-search project
# Contains functions necessary to find locations of words in given letter matrix

import utility as util


class WordSearchPuzzle:

    def __init__(self, path):
        self.path = path
        self.matrix = [[]]
        self.load_words()

    def load_words(self):
        w_list_as_str = util.get_first_line(self.path)
        self.words = w_list_as_str.split(",")
        # Remove any new line characters
        for i in range(self.words.__len__()):
            self.words[i] = self.words[i].strip()

    def __str__(self):
        return "WordSearchPuzzle {\n" + \
               "\n\tPath: " + self.path + ", " + \
               "\n\tWords: " + str(self.words) + ", " + \
               "\n\tMatrix: " + str(self.matrix) + \
               "\n\n}"


# Solve the word search given the words to find in the given puzzle matrix
# words: list of strings representing the words to find
# puzzle_matrix: a multidimensional array representing the positions of each letter in the
# matrix for the word search problem
def solve_word_search(words, puzzle_matrix):
    return None


# Given a file path to a text file, convert the file into a bi-dimensional array representing
# a matrix of letters
def file_to_matrix(path):
    my_matrix = util.file_to_matrix_arr(path, ignore_header=True)
    return my_matrix
