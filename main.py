# Author: Jacques Mathieu
# Created on 8/31/2019 at 2:02 PM
# Part of the kata-word-search project

from test import test_ws_1 as wst1
import ws_func as ws
import sys
import utility as util
import unittest as ut


# What to run for the bulk of the project
def main(input_path=""):
    # If run from command line, set 'input_path' to the path typed in the terminal
    if sys.argv.__len__() > 1:
        input_path = sys.argv[1]
    if input_path != "":
        # Run the test_ws_1 test module
        wst1.run_tests()
        print("\nRunning Kata Word Search Project\n")
        puzzle = ws.WordSearchPuzzle(input_path)
        print(puzzle.solve())


# Run the main method of the main file through IDE with specified file path
# example_path1 = "input/readme-example-input.txt"
# main(example_path1)

# Run the main method using the command line
main()

# Source 1: sys.argv help
# https://www.pythonforbeginners.com/system/python-sys-argv
