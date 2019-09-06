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


# Class that represents a coordinate
class Coordinate:

    def __init__(self, x_col: int, y_row: int):
        self.x_col = x_col
        self.y_row = y_row

    # Is the coordinate in bounds of the given dimensions? (Where max_width and max_height are one greater
    # than the last in bound index)
    def is_inbound(self, max_width: int, max_height: int):
        return self.x_col >= 0 and self.y_row >= 0 and self.x_col < max_width and self.y_row < max_height

    # Modify the specified axis using the given operation by a default amount of 1
    def modify(self, axis: str, op: str, amount = 1):
        if op == "subtract" or op == "sub" or op == "minus":
            amount = amount * -1
        # Otherwise, assume add operation
        if axis == "x_col" or axis == "col_x":
            self.x_col = self.x_col + amount
        # Otherwiase assume operation applies to y_row field
        else:
            self.y_row = self.y_row + amount

    def __str__(self):
        return "(" + str(self.x_col) + "," + str(self.y_row) + ")"


# Class that represents a matrix of letters
class LetterMatrix:
    def __init__(self):
        self.rows = []
        self.cols = []
        self.height = 0
        self.width = 0

    # Return the letter at the given coordinate
    def get_letter_at_coord(self, coord: Coordinate):
        # If given a valid coordinate
        if coord.is_inbound(self.width, self.height):
            return self.rows[coord.y_row][coord.x_col]

    # Add a row to the Letter Matrix
    def add_row(self, row: [str]):
        self.rows.append(row)

    # Add a column to the Letter Matrix
    def add_col(self, col: [str]):
        self.cols.append(col)

    def update_dimensions(self):
        self.width = self.rows[0].__len__()
        self.height = self.rows.__len__()

    # Load the rows of the letter matrix into the 'rows' field
    def load_rows(self, line_list: []):
        for line in line_list:
            line_as_arr = line.split(",")
            l_arr_len = line_as_arr.__len__()
            # Remove new line character from end and/or any extra whitespace from end or start
            line_as_arr[l_arr_len-1] = line_as_arr[l_arr_len-1].strip()
            line_as_arr[0] = line_as_arr[0].strip()
            self.add_row(line_as_arr)

    # Transform our list of rows to a list of columns and store them on the 'cols' field
    def load_cols(self):
        for col_i in range(self.width):
            temp_col = []
            for row_i in range(self.height):
                temp_col.append(self.rows[row_i][col_i])
            self.add_col(temp_col)

    # Load a letter matrix to this object from the given file path
    def load_matrix(self, path: str):
        line_list = util.get_lines_from_file(path, ignore_header=True)
        self.load_rows(line_list)
        # Validate the rows in the matrix are all of equal length
        self.validate_rows()
        # Transform the list of rows to a list of columns; We will make it here only if 'validate_rows'
        # runs without exiting the program
        self.load_cols()

    # Make sure the matrix has rows of equal length
    def validate_rows(self):
        # If the matrix exists in the first place
        if self.rows != None and self.rows.__len__() > 0:
            row_1_len = self.rows[0].__len__()
            for i in range(1, self.rows.__len__()):
                if self.rows[i].__len__() != row_1_len:
                    print(Fore.RED + "Error in given letter matrix: 'One or more rows are of "
                                     "unequal length'" + Fore.RESET)
                    exit(-1)
            # If we make it here, then we know we have a valid matrix! Now let's update its dimensions
            self.update_dimensions()
        else:
            # The given matrix is of size 0
            print(Fore.RED + "Error in given letter matrix file: 'No rows found'\n" + Fore.RESET)
            exit(-1)

    # Make a pretty string output of the matrix
    def __str__(self, extra_tab=False):
        # Placeholder for our tab character
        tab_ph = "\t"
        # Add extra tab if specified
        if extra_tab:
            tab_ph = tab_ph + "\t"
        matrix_s = "["
        last_row = self.rows.__len__() - 1
        last_row = self.rows[last_row]
        for row in self.rows:
            matrix_s = matrix_s + "\n" + tab_ph + str(row)
            if row != last_row:
                matrix_s = matrix_s + ","
        # Add tab to end square bracket if specified
        if extra_tab:
            return matrix_s + "\n\t]"
        else:
            return matrix_s + "\n]"


# A class that stores a line of text and its origin from a WordSearchPuzzle matrix
class SearchableLine:

    def __init__(self, line: str, xy_origin: Coordinate, ori: Orientation, dirs: [Direction]):
        self.line = line
        self.orientation = ori
        self.directions = dirs
        self.width = self.line.__len__()
        self.xy_origin = xy_origin
        print(self)

    def directions_as_pretty_str(self):
        dir_s = "["
        for d in self.directions[0:-1]:
            dir_s = dir_s + "'" + str(d.value) + "', "
        return dir_s + "'" + str(self.directions[-1].value) + "']"

    def __str__(self):
        return "SearchableLine {\n" + \
               "\n\tLine: " + self.line + ", Width: " + str(self.width) + ", " + \
               "\n\tOrigin:" + str(self.xy_origin) + ", " + \
               "\n\tOrientation: " + str(self.orientation.value) + ", " + \
               "\n\tDirection(s): " + self.directions_as_pretty_str() + \
               "\n\n}"


# A class that stores all lines of searchable text from a matrix of strings as a list of strings
# [As opposed to a list of a list of strings]
class SearchableLines:
    # On init, convert a matrix to a list of all searchable lines in the matrix
    def __init__(self, matrix: LetterMatrix):
        self.matrix = matrix
        self.lines = []
        self.matrix_to_searchable_strings()

    def get_diagonal_searchable_string(self, starting_coord: Coordinate, x_col_op: str, y_row_op: str):
        1

    def matrix_to_searchable_strings(self):
        row_idx = 0
        # Grab each horizontal 'searchable line' in the letter matrix
        for row in self.matrix.rows:
            line = util.list_to_string(row, sep="")
            hr_xy = Coordinate(0, row_idx)
            hl_xy = Coordinate(self.matrix.width - 1, row_idx)
            hr_searchable_line = SearchableLine(line, hr_xy, Orientation.HORIZONTAL, [Direction.RIGHT])
            hl_searchable_line = SearchableLine(util.reverse_string(line), hl_xy, Orientation.HORIZONTAL, [Direction.LEFT])
            self.lines.append(hr_searchable_line); self.lines.append(hl_searchable_line)
            row_idx = row_idx + 1

        col_idx = 0
        # Grab each vertical 'searchable line' in the letter matrix
        for col in self.matrix.cols:
            line = util.list_to_string(col, sep="")
            vd_xy = Coordinate(col_idx, 0)
            vu_xy = Coordinate(col_idx, self.matrix.height - 1)
            vd_searchable_line = SearchableLine(line, vd_xy, Orientation.VERTICAL, [Direction.DOWN])
            vu_searchable_line = SearchableLine(util.reverse_string(line), vu_xy, Orientation.VERTICAL, [Direction.UP])
            self.lines.append(vd_searchable_line); self.lines.append(vu_searchable_line)
            col_idx = col_idx + 1

        # To get all diagonal searchable lines, we will need to start at column 0 and go from row 0 to row 'n'. After we
        # reach the last row, we then begin to increment the column number until column 'n' while the row remains at 'n'
        col_idx = 0
        row_idx = 0
        while row_idx < self.matrix.height and col_idx < self.matrix.width:

            # Up Right diagonal string
            ur_diag_s = ""
            temp_coord = Coordinate(col_idx, row_idx)
            # Increment coordinate diagonally up and to the right by one unit until out of bounds,
            # then move on to the next diagonal
            while temp_coord.is_inbound(self.matrix.width, self.matrix.height):
                ur_diag_s = ur_diag_s + self.matrix.get_letter_at_coord(temp_coord)
                temp_coord.modify("x_col", "add"); temp_coord.modify("y_row", "add")

            up_right_diag = ur_diag_s
            down_left_diag = util.reverse_string(ur_diag_s)

            # If we reach the last row, start increasing the column index
            if row_idx + 1 >= self.matrix.height:
                col_idx = col_idx + 1
            # Otherwise continue until we get to the last row
            else:
                row_idx = row_idx + 1




class WordSearchPuzzle:

    def __init__(self, path):
        self.path = path
        # Load the letter matrix into an object from the file at the given path
        self.matrix = LetterMatrix()
        self.matrix.load_matrix(self.path)
        self.load_words()
        self.load_searchable_lines()

    def load_words(self):
        w_list_as_str = util.get_first_line(self.path)
        self.words = w_list_as_str.split(",")
        words_len = self.words.__len__()
        # Remove new line character from end and/or any extra whitespace from end or start
        self.words[words_len-1] = self.words[words_len-1].strip()
        self.words[0] = self.words[0].strip()

    # Load all searchable lines in matrix
    def load_searchable_lines(self):
        self.searchable_lines = SearchableLines(self.matrix)

    # # Return the matrix in a readable string format
    # def matrix_as_pretty_str(self, extra_tab=False):
    #

    def __str__(self):
        return "WordSearchPuzzle {\n" + \
               "\n\tPath: " + self.path + ", " + \
               "\n\tWords: " + str(self.words) + ", " + \
               "\n\tMatrix: " + self.matrix.__str__(extra_tab=True) + \
               "\n\n}"


# Solve the word search for the given WordSearchPuzzle
def solve_word_search(puzzle: WordSearchPuzzle):
    return None
