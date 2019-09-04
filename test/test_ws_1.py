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
print("Initialized " + MODULE_NAME + "test module\n")


# Help on learning the unittest library from Source 1 (See bottom of file)
# Run tests on word search function
class TestWordSearch(ut.TestCase):

    def test_solve_word_search(self):
        actual_out = ""
        ctr = 1
        # Put test folder in path b/c tests will be run from main.py outside of test folder
        base_in_out_name = "test/$/ws-test-#-$.txt"
        while ctr <= MAX_TEST_CASES:
            new_base = base_in_out_name.replace("#", str(ctr))
            my_in = new_base.replace("$", "input")
            expected_out = new_base.replace("$", "output")
            if util.does_file_exist(my_in) and util.does_file_exist(expected_out):
                print(my_in + " and " + expected_out + " exists")
            else:
                break
            ctr = ctr + 1
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
    suite = ut.TestLoader().loadTestsFromTestCase(TestWordSearch)
    ut.TextTestRunner().run(suite)


# Source 1: Using unittest
# https://docs.python.org/3/library/unittest.html

# Source 2: More on unittest (not from the command line!)
# https://docs.python.org/2/library/unittest.html#unittest.TestResult
