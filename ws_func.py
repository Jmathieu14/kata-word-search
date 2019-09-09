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

    # See if this coordinate equals another
    def equals(self, other):
        return self.x_col == other.x_col and self.y_row == other.y_row

    # Update this coordinate to the new x and y values
    def update(self, x_val: int, y_val: int):
        self.x_col = x_val
        self.y_row = y_val

    # Return this Coordinate's axis that matches the given string axis
    def get_axis(self, axis: str):
        if axis == "x_col" or axis == "col_x":
            return self.x_col
        # Otherwise assume y row was requested
        else:
            return self.y_row

    # Set the value of the specified axis to the given value
    def set_axis(self, axis: str, value: int):
        if axis == "x_col" or axis == "col_x":
            self.x_col = value
        # Otherwise assume y row was requested
        else:
            self.y_row = value

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
        return self

    # Return a copy of this Coordinate
    def copy(self):
        return Coordinate(self.x_col, self.y_row)

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

    def gen_coords_in_range(self, start: Coordinate, end: Coordinate, axes_plus_ops: [{}]):
        coord_list = []
        coord_list_filled = False
        for axis_op in axes_plus_ops:
            temp_coord = start.copy()
            coord_list_idx = 0
            # While the temp_coord does not have the same x or y axis as does the end coordinate...
            while temp_coord.modify(axis=axis_op['axis'], op=axis_op['op']).get_axis(axis_op['axis']) \
                    != end.get_axis(axis_op['axis']):
                # print("Temp: " + str(temp_coord) + " vs. End: " + str(end))
                if coord_list_filled == False:
                    coord_list.append(temp_coord.copy())
                else:
                    coord_list[coord_list_idx].set_axis(axis=axis_op['axis'],
                                                        value=temp_coord.get_axis(axis_op['axis']))
                coord_list_idx = coord_list_idx + 1
            coord_list_filled = True
        if coord_list.__len__() == 0:
            coord_list.append(start.copy())
        else:
            coord_list.insert(0, start.copy())
        coord_list.append(end.copy())
        return coord_list

    # Find the coordinates of the given substring in the line field of this SearchableLine using its orientation and
    # direction to determine these coordinates in relation to its position in a LetterMatrix
    def find_coords(self, substr: str):
        idx = self.line.find(substr)
        # If idx is > -1, the substring IS in the string 'line' field
        if idx > -1:
            sub_len_1 = substr.__len__() - 1
            end_point = Coordinate(self.xy_origin.x_col, self.xy_origin.y_row)
            starting_point = Coordinate(self.xy_origin.x_col, self.xy_origin.y_row)
            # The operations to apply to the specified axes to generate all points from the starting_point
            # to the end_point
            axes_ops = []

            # The following two code blocks calculate the starting and end point of the substring in this line in
            # relation to the LetterMatrix it is a part of.

            # (Calculate the x value for starting point; Calculate x value for end point)
            if Direction.RIGHT in self.directions:
            # Add idx to the x value of this line's point of origin
                starting_point.modify("x_col", "add", amount=idx)
                end_point.update(starting_point.x_col + sub_len_1, end_point.y_row)
                axes_ops.append({'axis': 'x_col', 'op': 'add'})
            elif Direction.LEFT in self.directions:
            # Subtract idx from the x value of this line's point of origin
                starting_point.modify("x_col", "minus", amount=idx)
                end_point.update(starting_point.x_col - sub_len_1, end_point.y_row)
                axes_ops.append({'axis': 'x_col', 'op': 'minus'})

            # (Calculate the y value for starting point; Calculate y value for end point)
            if Direction.UP in self.directions:
                starting_point.modify("y_row", "minus", amount=idx)
                end_point.update(end_point.x_col, starting_point.y_row - sub_len_1)
                axes_ops.append({'axis': 'y_row', 'op': 'minus'})
            elif Direction.DOWN in self.directions:
                starting_point.modify("y_row", "add", amount=idx)
                end_point.update(end_point.x_col, starting_point.y_row + sub_len_1)
                axes_ops.append({'axis': 'y_row', 'op': 'add'})

            # Generate the entire coordinate list as specified with the start and end points
            # along with appropriate operations to perform on the specified axes
            coord_list = self.gen_coords_in_range(starting_point, end_point, axes_ops)

            return coord_list

    # Return a list of Coordinates as a string
    def coord_list_to_str(self, coords: [Coordinate]):
        if coords is not None and coords.__len__() > 0:
            # print(coords)
            s = ""
            for i in range(0, coords.__len__()-1):
                s = s + str(coords[i]) + ","
            return s + str(coords[coords.__len__()-1])
        else:
            return "<No Coordinates>"

    # Do the same as above, but return as a string
    def find_coords_as_str(self, substr: str):
        coords = self.find_coords(substr)
        # If the coordinates ARE found
        if coords is not None:
            return substr + ": " + self.coord_list_to_str(coords)

    def directions_as_pretty_str(self):
        dir_s = "["
        for d in self.directions[0:-1]:
            dir_s = dir_s + "'" + str(d.value) + "', "
        return dir_s + "'" + str(self.directions[-1].value) + "']"

    def __str__(self):
        return "SearchableLine {\n" + \
               "\n\tLine: " + self.line + ", Width: " + str(self.width) + ", " + \
               "\n\tOrigin: " + str(self.xy_origin) + ", " + \
               "\n\tOrientation: " + str(self.orientation.value) + ", " + \
               "\n\tDirection(s): " + self.directions_as_pretty_str() + \
               "\n\n}"


# A class that stores all lines of searchable text from a matrix of strings as a list of strings
# [As opposed to a list of a list of strings]
class SearchableLines:
    # On init, convert a matrix to a list of all searchable lines in the matrix
    def __init__(self, matrix: LetterMatrix):
        self.matrix = matrix
        # Add object to this list so there is a type associated with the objects in it for the IDE
        # Remember to reset list to '[]' in first function call to add to this list
        self.lines = [SearchableLine]
        self.matrix_to_searchable_strings(reset=True)

    # Return the number of lines in the SearchableLines object
    def num_of_lines(self):
        return self.lines.__len__()

    # Get the searchable line at index 'idx'
    def get_sl(self, idx: int):
        return self.lines[idx]

    # Return the diagonal string found with the given coordinate and coordinate operations
    # and return the end coordinate as a dict
    def get_diag_str_plus_coord(self, starting_coord: Coordinate, x_col_op: str, y_row_op: str):
        diag_s = ""
        cur_coord = Coordinate(starting_coord.x_col, starting_coord.y_row)
        end_coord = Coordinate(0, 0)
        while cur_coord.is_inbound(self.matrix.width, self.matrix.height):
            diag_s = diag_s + self.matrix.get_letter_at_coord(cur_coord)
            end_coord.update(cur_coord.x_col, cur_coord.y_row)
            cur_coord.modify("x_col", x_col_op); cur_coord.modify("y_row", y_row_op)
        return { "str": diag_s, "coord": end_coord }

    def matrix_to_searchable_strings(self, reset=False):
        # Reset lines to empty list
        if reset:
            self.lines = []
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
        # *NOTE: This only gets all diagonal lines that go up right and down left.*
        # ---------->
        # |   0 1 n
        # | 0 X X X
        # | 1 X X X
        # | n X X X
        # v

        col_idx = 0
        row_idx = 0
        # Iterate for up right/down left diagonals by increasing row value and then by increasing column value
        while col_idx < self.matrix.width:

            cur_coord = Coordinate(col_idx, row_idx)
            # Increment coordinate diagonally up and to the right by one unit until out of bounds
            # Return the resulting string to our Up Right diagonal string variable
            ur_diag_plus_coord = self.get_diag_str_plus_coord(cur_coord, x_col_op="add", y_row_op="sub")
            up_right_diag = ur_diag_plus_coord['str']
            # Reverse for our Down Left diagonal string
            down_left_diag = util.reverse_string(up_right_diag)
            down_left_coord = ur_diag_plus_coord['coord']

            # Now that we have each diagonal line and the relavent starting coordinates for them, let us add that to
            # this object!
            ur_sl = SearchableLine(up_right_diag, cur_coord, Orientation.DIAGONAL, [Direction.UP, Direction.RIGHT])
            dl_sl = SearchableLine(down_left_diag, down_left_coord, Orientation.DIAGONAL, [Direction.DOWN, Direction.LEFT])
            self.lines.append(ur_sl); self.lines.append(dl_sl)

            # If we reach the last row, start increasing the column index
            if row_idx + 1 >= self.matrix.height:
                col_idx = col_idx + 1
            # Otherwise continue until we get to the last row
            else:
                row_idx = row_idx + 1

        col_idx = self.matrix.width - 1
        row_idx = 0
        # Iterate for down right/up left diagonals by decreasing column value and then by increasing row value
        while row_idx < self.matrix.height:

            cur_coord = Coordinate(col_idx, row_idx)
            # Now increment coordinate to the right and down one unit; Store on our Down Right diagonal str variable
            dr_diag_plus_coord = self.get_diag_str_plus_coord(cur_coord, x_col_op="add", y_row_op="add")
            down_right_diag = dr_diag_plus_coord['str']
            # Reverse for our Up Left diagonal string
            up_left_diag = util.reverse_string(down_right_diag)
            up_left_coord = dr_diag_plus_coord['coord']
            # Add lines to lines field
            dr_sl = SearchableLine(down_right_diag, cur_coord, Orientation.DIAGONAL, [Direction.DOWN, Direction.RIGHT])
            ul_sl = SearchableLine(up_left_diag, up_left_coord, Orientation.DIAGONAL, [Direction.UP, Direction.LEFT])
            self.lines.append(dr_sl); self.lines.append(ul_sl)
            # If we reach the first column, start increasing the row index
            if col_idx - 1 < 0:
                row_idx = row_idx + 1
            # Otherwise continue until we get to the first column
            else:
                col_idx = col_idx - 1


class WordSearchPuzzle:

    def __init__(self, path):
        self.path = path
        if util.does_file_exist(path):
            # Load the letter matrix into an object from the file at the given path
            self.matrix = LetterMatrix()
            self.matrix.load_matrix(self.path)
            self.load_words()
            self.load_searchable_lines()
        else:
            print(">>Given invalid path: '" + path + "'")
            exit(-1)

    def load_words(self):
        w_list_as_str = util.get_first_line(self.path)
        self.words = w_list_as_str.split(",")
        words_len = self.words.__len__()
        # Remove new line character from end and/or any extra whitespace from end or start
        self.words[words_len-1] = self.words[words_len-1].strip()
        self.words[0] = self.words[0].strip()
        self.words_loaded = True

    # Load all searchable lines in matrix
    def load_searchable_lines(self):
        self.searchable_lines = SearchableLines(self.matrix)
        self.lines_loaded = True

    # Solve the WordSearchPuzzle!
    def solve(self):
        if self.words_loaded and self.lines_loaded:
            solution = ""
            for word in self.words:
                for searchable_line in self.searchable_lines.lines:
                    # The searchable line string
                    coords_str = searchable_line.find_coords_as_str(substr=word)
                    # If it's not None, we have found the word in our searchable line!
                    if coords_str is not None:
                        solution = solution + coords_str + "\n"
            return solution
        else:
            print("The words or lines for the given puzzle were not loaded properly. Please check to make sure "+\
                  "the format of the input file is correct.")

    def __str__(self):
        return "WordSearchPuzzle {\n" + \
               "\n\tPath: " + self.path + ", " + \
               "\n\tWords: " + str(self.words) + ", " + \
               "\n\tMatrix: " + self.matrix.__str__(extra_tab=True) + \
               "\n\n}"
