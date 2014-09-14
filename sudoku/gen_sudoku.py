#!/usr/bin/python
import sudoku2
import optparse
import random

parser = optparse.OptionParser()
parser.add_option( "-s", "--size", default=9, dest="size" )
parser.add_option( "-f", "--fixed", default=5, dest="fixed" )
(options, args) = parser.parse_args()

s = sudoku2.Sudoku( size = options.size )
s.shuffle()
soln = s.solve()

to_print = sudoku2.Sudoku( size = int(options.size) )
for i in random.sample( range(s.size() ** 2), int(options.fixed) ):
	to_print.fix_point( i, soln.choice( i ) )

print to_print
print "The Solution:"
print soln
