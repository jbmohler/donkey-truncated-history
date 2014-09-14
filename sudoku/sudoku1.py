import copy
import random
import math

class Impossible:
	pass

class Sudoku:
	def __init__( self, small_size = None, size = None ):
		assert small_size is None or size is None 
		if small_size is None:
			self.small_size = int(math.sqrt(float(size)))
		else:
			self.small_size = small_size

		self.board = [[range(1,self.size() + 1) for j in range(self.size())] for k in range(self.size())]

	def index( self, coord ):
		if type( coord ) is tuple:
			return coord[0] * self.size() + coord[1]
		else:
			return coord

	def coordinates( self, coord ):
		if type( coord ) is tuple:
			return coord[0], coord[1]
		else:
			return coord / self.size(), coord % self.size()

	def size( self ):
		return self.small_size ** 2

	def csv_board( self, show_options = True ):
		cellwidth = 2
		if show_options:
			cellwidth = self.size() + 1
		for r in self.board:
			cells = []
			for cell in r:
				s = ''
				if type(cell) is list:
					if show_options:
						s = ''.join( map( lambda x: str(x), cell ) )
					else:
						s = ''
				else:
					s = str( cell )
				cells.append( s )
			print '%s' % ','.join( cells )

	def __repr__( self ):
		self.print_board()
		return ""

	def print_board( self, show_options = True ):
		cellwidth = 2
		if show_options:
			cellwidth = self.size() + 1
		for r in self.board:
			for cell in r:
				s = ''
				if type(cell) is list:
					if show_options:
						s = ''.join( map( lambda x: str(x), cell ) )
					else:
						s = '_'
				else:
					s = str( cell )
				print '%-*s' % (cellwidth, s),
			print '\n',

	def shuffle( self ):
		s = self.size()
		for i in range(s):
			for j in range(s):
				if type(self.board[i][j]) is list:
					random.shuffle( self.board[i][j] )

	def choice( self, coord ):
		x, y = self.coordinates( coord )
		return self.board[x][y]

	def fix_grid( self, content ):
		assert type(content) is list 
		assert len(content) == self.size() 

		for i in range( self.size() ):
			if content[i] != None:
				assert type(content[i]) is list 
				self.fix_row( i, content[i] )

	def fix_row( self, row, content ):
		assert type(content) is list 
		assert len(content) == self.size() 

		for i in range( self.size() ):
			if content[i] != 0 and content[i] != None:
				self.fix_point( (row, i), content[i] )

	def fix_point( self, coord, n ):
		x, y = self.coordinates( coord )
		if not type(self.board[x][y]) is list:
			if n != self.board[x][y]:
				raise Impossible

		self.board[x][y] = n

		for i in range(self.size()):
			if x != i:
				self.remove_choice( (i, y), n )
			if y != i:
				self.remove_choice( (x, i), n )

		offset_x = x/self.small_size
		offset_y = y/self.small_size
		for i in range(self.small_size):
			for j in range(self.small_size):
				this_x = i + offset_x * self.small_size
				this_y = j + offset_y * self.small_size
				if this_x != x and this_y != y:
					self.remove_choice( (this_x, this_y), n )

	def remove_choice( self, coord, n ):
		x, y = self.coordinates( coord )
		if (type(self.board[x][y]) is list) and (n in self.board[x][y]):
			self.board[x][y].remove( n )
			if len(self.board[x][y]) == 1:
				self.fix_point( (x, y), self.board[x][y][0] )
		elif (not type(self.board[x][y]) is list) and n == self.board[x][y]:
			raise Impossible

	def successful( self ):
		pass

	def twarted( self ):
		pass

	def next_index_min_index( self, coord ):
		min_list_size = self.size()
		min_cell = None
		for i in range( self.size() ):
			for j in range( self.size() ):
				if type(self.board[i][j]) is list:
					if len(self.board[i][j]) < min_list_size:
						min_list_size = len(self.board[i][j])
						min_cell = i * self.size() + j

		return min_cell

	def next_index_min_group( self, coord ):
		pass

	next_index = next_index_min_index

	def solve( self ):
		return self.__solve( self.next_index( 0 ) )

	def __solve( self, coord ):
		x, y = self.coordinates( coord )

		if type(self.board[x][y]) is list:
			if len(self.board[x][y]) > 0:
				for n in self.board[x][y]:
					next = copy.deepcopy(self)
					try:
						next.fix_point( (x, y), n )
					except Impossible:
						continue
					next_up = next.next_index( coord )
					if next_up is None:
						next.successful()
						return next
					soln = next.__solve( next_up )
					if soln:
						return soln
			else:
				self.twarted()
				return None
		else:
			next_up = self.next_index( coord )
			if next_up is None:
				self.successful()
				return self
			return self.__solve( next_up )

def Sudoku_FromFile( file ):
	lines = open(file,"r").readlines()
	lines = [l.strip() for l in lines if l != ""]
	s2 = Sudoku(size=len(lines))

	def cell(c):
		if c == '*':
			return 0
		else:
			return int(c)

	for i in range(len(lines)):
		s2.fix_row( i, [cell(c) for c in lines[i]] )

	return s2
