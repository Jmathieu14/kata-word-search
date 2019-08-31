# Author: Jacques Mathieu
# Created on 8/31/2019 at 1:35 PM
# Part of the kata-word-search project

import unittest as ut
import os.path as osp
import os

# Set a cap on the number of tests performed in this file
MAX_TEST_CASES = 100


# Help on learning the unittest library from Source 1 (See bottom of file)
# Run tests on word search function
class TestWordSearch(ut.TestCase):

    def test_word_search(self):
        my_in = ""
        expected_out = ""
        actual_out = ""
        ctr = 1
        base_in_out_name = "ws-test-#-$.txt"
        while ctr <= MAX_TEST_CASES:
            new_base = base_in_out_name.replace("#", str(ctr))
            my_in = new_base.replace("$", "input")
            my_out = new_base.replace("$", "output")
            print(my_in + " " + my_out)
            ctr = ctr + 1
            break
        self.assertTrue(1, 1)


# Run tests through command line
# Type the following in the cmd prompt: $> python -m unittest ws_test_module
# Do so under the test folder
if __name__ == '__main__':
    ut.main()


# Run test through this function call
def run_tests():
    ut.main()


# Source 1: Using unittest
# https://docs.python.org/3/library/unittest.html
