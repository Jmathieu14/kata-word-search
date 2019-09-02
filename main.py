# Author: Jacques Mathieu
# Created on 8/31/2019 at 2:02 PM
# Part of the kata-word-search project

from test import test_ws_1 as wst1
import ws_func as ws
import utility as util
import unittest as ut


# What to run for the bulk of the project
def main():
    # Run the test_ws_1 test module
    wst1.run_tests()
    print("\nRunning Kata Word Search Project\n")
    puzzle_path1 = "test/input/ws-test-1-input.txt"
    puzzle1 = ws.WordSearchPuzzle(puzzle_path1)
    print(puzzle1)


# Run the main method of the main file
main()
