# Author: Jacques Mathieu
# Created on 8/31/2019 at 2:02 PM
# Part of the kata-word-search project

from test import ws_test_module as wst
import utility as util


# What to run for the bulk of the project
def main():
    print("Running Kata Word Search Project")
    # Run the ws_test_module
    util.run_cmd("cd test && python -m unittest ws_test_module")


# Run the main method of the main file
main()
