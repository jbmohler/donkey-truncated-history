import copy
import random
import math

from sudoku2 import SudokuConfig, SudokuBoard, Sudoku_FromFile

# I am slightly worried that this doesn't make the correction in quite the way I want it to
# particularly, if you have both sudoku2 and sudoku3 imported in another place (e.g. test_sudoku)
SudokuConfig.good_index = SudokuConfig.good_index_min_choices
