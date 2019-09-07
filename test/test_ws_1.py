# Author: Jacques Mathieu
# Created on 8/31/2019 at 1:35 PM
# Part of the kata-word-search project

import unittest as ut
import utility as util
import ws_func as ws
import os.path as osp
import os
# To color messages printed to terminal
from colorama import Fore, Back, Style

# Set a cap on the number of tests performed per test function
MAX_TEST_CASES = 100
MODULE_NAME = "test_ws_1"

# Notify user test module is loaded
print("Initialized " + MODULE_NAME + " test module\n")


# Help on learning the unittest library from Source 1 (See bottom of file)
# Run tests on word search function
class TestWordSearchPuzzle(ut.TestCase):

    # Get the test files necessary to run these tests
    def get_test_files(self, base_test_name: str):
        test_files = []
        ctr = 1
        while ctr <= MAX_TEST_CASES:
            new_base = base_test_name.replace("#", str(ctr))
            my_in = new_base.replace("$", "input")
            expected_out = new_base.replace("$", "output")
            if util.does_file_exist(my_in) and util.does_file_exist(expected_out):
                test_files.append({"in": my_in, "out": expected_out})
            else:
                # Print if file naming format is incorrect
                if ctr == 1:
                    print("File with format '" + base_test_name + "' does not exist")
                break
            ctr = ctr + 1
        return test_files

    def test_generated_searchable_lines(self):
        # $ represents 'input' or 'output', and # represents number of file
        # Put test folder in path b/c tests will be run from main.py outside of test folder
        base_test_name = "test/$/slnum-test-#-$.txt"
        test_files = self.get_test_files(base_test_name)
        for f in test_files:
            test_puzzle = ws.WordSearchPuzzle(f['in'])
            w = test_puzzle.matrix.width
            h = test_puzzle.matrix.height
            # w = num of vertical lines; h = num of horizontal lines; (w + h - 1) * 2 = num of diagonal lines
            # Multiply this all by 2 to get all DIRECTIONAL lines in the matrix
            num_searchable_lines = (w + h + (2 * (w + h - 1))) * 2
            # Check to make sure the number of lines calculated from the size of the object representation of the matrix
            # matches the actual number of generated 'searchable' lines
            self.assertEqual(test_puzzle.searchable_lines.num_of_lines(), num_searchable_lines,
                     "The number of searchable lines generated does not match the calculated expected amount to"\
                     + " be found.")
            # Check to make sure the static expected amount matches the number of generated searchable lines
            # If not, there is an error in correctly reading in the file to store as a matrix
            expected_num_from_file = int(util.get_first_line(f['out']).strip())
            self.assertEqual(test_puzzle.searchable_lines.num_of_lines(), expected_num_from_file,
                     "The number of searchable lines generated does not match the statically calculated amount of "\
                     + "lines. This means the matrix was loaded incorrectly from the file or the statically calculated"\
                     + " number is incorrect.")

    def test_solve_word_search(self):
        # $ represents 'input' or 'output', and # represents number of file
        # Put test folder in path b/c tests will be run from main.py outside of test folder
        base_test_name = "test/$/ws-test-#-$.txt"
        test_files = self.get_test_files(base_test_name)
        for f in test_files:
            test_puzzle = ws.WordSearchPuzzle(f['in'])
            actual_out = test_puzzle.solve()
            expected_out = util.get_lines_from_file(f['out'])
        self.assertTrue(1, 1)


# Run tests through command line
# Type the following in the cmd prompt: $> python -m unittest test_ws_1
# Do so under the test folder
if __name__ == '__main__':
    ut.main()


# Run this test module through this function call
def run_tests():
    # Thanks to source 2, we don't have to use the command line! Insanely challenging concept that one
    # WOULDN'T want to run tests in the command line! Thank goodness they only wrote a couple lines on this
    # amongst 1262 other lines of text! I'm so glad it took so little time to find, what a life saver! An immense
    # 0.16% of the page was taken up by this KEY information, making it nearly effortless to find!
    suite = ut.TestLoader().loadTestsFromTestCase(TestWordSearchPuzzle)
    ut.TextTestRunner().run(suite)


# Source 1: Using unittest
# https://docs.python.org/3/library/unittest.html

# Source 2: More on unittest (not from the command line!)
# https://docs.python.org/2/library/unittest.html#unittest.TestResult
