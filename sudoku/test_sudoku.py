#!/usr/bin/python

import resource
def cputime(t=0):
    try:
        t = float(t)
    except TypeError:
        t = 0.0
    u,s = resource.getrusage(resource.RUSAGE_SELF)[:2]
    return u+s - t


games=[
#	"examples/near_worst_case.txt",
	"examples/qassim_hamza.txt",
	"examples/sample_01.txt",
	"examples/flight_1107_easy.txt",
	"examples/flight_1107_hard.txt",
	"examples/flight_482_easy.txt",
	"examples/flight_482_hard.txt",
	"examples/flight_482_easy2.txt",
	"examples/flight_482_hard2.txt",
	"examples/top_1465_77.txt"]

import gc
gc.disable()

for g in games:
	print "Game:  %s" % (g,)
	from sudoku1 import *
	s=Sudoku_FromFile(g)
	t1=cputime()
	for i in range(10):
		s.shuffle()
		s.solve()
	t2=cputime()
	print "Sudoku v. 1:  %.3f" % (t2-t1)
	gc.collect()
	
	from sudoku2 import *
	s=Sudoku_FromFile(g)
	t1=cputime()
	for i in range(10):
		s.shuffle()
		s.solve()
	t2=cputime()
	print "Sudoku v. 2:  %.3f" % (t2-t1)
	gc.collect()

	import sudoku5
	s=sudoku5.Sudoku_FromFile(g)
	t1=cputime()
	for i in range(10):
		s.shuffle()
		s.solve()
	t2=cputime()
	print "Sudoku v. 5:  %.3f" % (t2-t1)
	gc.collect()
