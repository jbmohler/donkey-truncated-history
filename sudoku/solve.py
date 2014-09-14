#!/usr/bin/env python
import argparse
import sudoku2

parser = argparse.ArgumentParser('sudoku solver cli')
parser.add_argument( "-p", "--puzzle-file", default=None, dest="puzzle_file" )
args = parser.parse_args()

s2 = sudoku2.Sudoku_FromFile(args.puzzle_file)
s2.shuffle()
print s2.solve()
print "Original:"
print s2
