# Author: Jacques Mathieu
# Created on 9/2/2019 at 4:49 PM
# Part of the kata-word-search project
# Contains functions necessary to find locations of words in given letter matrix

import utility as util
from enum import Enum as E
# To color messages printed to terminal
from colorama import Fore, Back, Style


# Class of enums that represent the original orientation of a given line of text
class Orientation(E):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL = "diagonal"


# Class of enums that represent the original direction of a given line of text
class Direction(E):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"


# A class that stores a line of text and its origin from a WordSearchPuzzle matrix
class SearchableLine:

    def __init__(self, line: str, ori: Orientation, dirs: [Direction]):
        self.line = line
        self.orientation = ori
        self.directions = dirs
        print(self)

    def directions_as_pretty_str(self):
        dir_s = "["
        for d in self.directions[0:-1]:
            dir_s = dir_s + "'" + str(d.value) + "', "
        return dir_s + "'" + str(self.directions[-1].value) + "']"

    def __str__(self):
        return "SearchableLine {\n" + \
               "\n\tLine: " + self.line + ", " + \
               "\n\tOrientation: " + str(self.orientation.value) + ", " + \
               "\n\tDirections: " + self.directions_as_pretty_str() + \
               "\n\n}"


# A class that stores all lines of searchable text from a matrix of strings as a list of strings
# [As opposed to a list of a list of strings]
class SearchableLines:
    # On init, convert a matrix to a list of all searchable lines in the matrix
    def __init__(self, matrix: list):
        self.matrix = matrix
        self.lines = []
        self.matrix_to_searchable_strings()

    def matrix_to_searchable_strings(self):
        # Grab each horizontal 'searchable line' in the matrix
        for row in self.matrix:
            line = util.list_to_string(row, sep="")
            searchable_line = SearchableLine(line, Orientation.HORIZONTAL, [Direction.RIGHT])
            self.lines.append(searchable_line)


class WordSearchPuzzle:

    def __init__(self, path):
        self.path = path
        self.load_matrix()
        self.validate_matrix()
        self.load_words()
        self.load_searchable_lines()

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

    # Make sure the matrix has rows of equal length
    def validate_matrix(self):
        # If the matrix exists in the first place
        if self.matrix != None and self.matrix.__len__() > 0:
            row_1_len = self.matrix[0].__len__()
            for i in range(1, self.matrix.__len__()):
                if self.matrix[i].__len__() != row_1_len:
                    print(Fore.RED + "Error in given letter matrix: 'One or more rows are of unequal length'" + Fore.RESET)
                    exit(-1)

    # Load all searchable lines in matrix
    def load_searchable_lines(self):
        self.searchable_lines = SearchableLines(self.matrix)

    # Return the matrix in a readable string format
    def matrix_as_pretty_str(self, extra_tab=False):
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
               "\n\tMatrix: " + self.matrix_as_pretty_str(extra_tab=True) + \
               "\n\n}"


# Solve the word search for the given WordSearchPuzzle
def solve_word_search(puzzle: WordSearchPuzzle):
    return None
