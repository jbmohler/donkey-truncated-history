import copy
import random
import math

class Impossible:
    pass

class SudokuConfig:
    def __init__( self, small_size = None, size = None ):
        assert small_size is None or size is None 
        if small_size is None:
            self.small_size = int(math.sqrt(float(size)))
        else:
            self.small_size = small_size

        self.rSize = range(self.size())
        self.rSmallSize = range(self.small_size)

        self.groups = []
        for i in self.rSize:
            self.groups.append(tuple(self.index((i,y)) for y in self.rSize))
            self.groups.append(tuple(self.index((x,i)) for x in self.rSize))

        for subx in self.rSmallSize:
            for suby in self.rSmallSize:
                self.groups.append(tuple(self.index((i+subx*self.small_size,j+suby*self.small_size)) for i in self.rSmallSize for j in self.rSmallSize))

        self.membership = [None]*(self.size()**2)
        for i in range(self.size()**2):
            self.membership[i] = tuple(g for g in self.groups if i in g)

    def size(self):
        return self.small_size**2

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

    def __repr__(self):
        return "Sudoku groups for a %ix%i grid." % (self.size(), self.size())

    def fix_point( self, board, coord, n ):
        idx = self.index( coord )
        if not type(board[idx]) is list:
            if n != board[idx]:
                raise Impossible

        board[idx] = n

        to_review=set()
        for mem in self.membership[idx]:
            for i in mem:
                if i != idx:
                    self.remove_choice(board,i,n)
                    if (type(board[i]) is list) and (n in board[i]):
                        for j in self.membership[i]:
                            to_review.add(j)
        for x in to_review:
            #TODO TODO TODO -- we must do some check since this can lead to in-appropriate point fixing.
            possibilities = [idx for idx in x if type(board[idx]) is list and (n in board[idx])]
            if len(possibilities) == 1:
                self.fix_point(board,possibilities[0],n)

    def remove_choice( self, board, coord, n ):
        idx = self.index( coord )
        if (type(board[idx]) is list) and (n in board[idx]):
            board[idx].remove( n )
            if len(board[idx]) == 1:
                self.fix_point( board, idx, board[idx][0] )
        elif (not type(board[idx]) is list) and n == board[idx]:
            raise Impossible

    def good_index_min_choices(self, board):
        min_list_size = self.size()
        min_cell = None
        for idx in range(self.size()**2):
            if type(board[idx]) is list:
                if len(board[idx]) < min_list_size:
                    min_list_size = len(board[idx])
                    min_cell = idx

        return min_cell

    def good_index_min_group( self, board ):
        #pass
        weights = []
        for g in self.groups:
            weights.append( (g,sum([len(board[idx]) for idx in g if type(board[idx]) is list])) )
        weights.sort(key=lambda x: x[1])
        grp = None
        for i in range(len(weights)):
            if weights[i][1] > 0:
                grp = weights[i][0]
                break

        if grp is None:
            return None
        else:
            min_list_size = self.size()
            min_cell = None
            for idx in grp:
                if type(board[idx]) is list:
                    if len(board[idx]) < min_list_size:
                        min_list_size = len(board[idx])
                        min_cell = idx

            return min_cell

    good_index = good_index_min_group

    def solve( self, board ):
        idx = self.good_index(board)
        if idx is None:
            return board
        elif len(board[idx]) == 0:
            raise Impossible
        else:
            for n in board[idx]:
                next_board = copy.deepcopy(board)
                try:
                    #print "Set %i to %i" % (idx,n)
                    self.fix_point( next_board, idx, n )
                    #sb=SudokuBoard(size=self.size())
                    #sb.board = next_board
                    #print sb
                    return self.solve(next_board)
                except Impossible:
                    continue
            raise Impossible

class SudokuBoard:
    def __init__( self, small_size = None, size = None ):
        assert small_size is None or size is None 
        self.config = SudokuConfig(small_size,size)
        self.board = [range(1,self.config.size() + 1) for j in self.config.rSize for k in self.config.rSize]

    def __repr__( self ):
        s = self.config.size()
        rows = []
        for i in self.config.rSize:
            cells = []
            for j in self.config.rSize:
                if type(self.board[self.config.index((i,j))]) is list:
                    cells.append( ''.join(map(str,self.board[self.config.index((i,j))])) )
                else:
                    cells.append( str(self.board[self.config.index((i,j))]) )
            rows.append( ' '.join( map( lambda x: "%-*s" % (s,x), cells ) ) )
        return '\n'.join(rows)

    def size(self):
        return self.config.size()

    def fix_grid( self, content ):
        assert type(content) is list 
        assert len(content) == self.size() 

        for i in self.config.rSize:
            if content[i] != None:
                assert type(content[i]) is list 
                self.fix_row( i, content[i] )

    def fix_row( self, row, content ):
        assert type(content) is list 
        assert len(content) == self.size() 

        for i in self.config.rSize:
            if content[i] != 0 and content[i] != None:
                self.fix_point( (row, i), content[i] )

    def fix_point( self, coord, n ):
        self.config.fix_point( self.board, coord, n )

    def shuffle( self ):
        s = self.size()
        for b in self.board:
            if type(b) is list:
                random.shuffle( b )

    def solve(self):
        newb=self.config.solve(self.board)
        if newb is None:
            return None
        else:
            sb=SudokuBoard(size=self.size())
            sb.board = newb
            return sb

def Sudoku_FromFile( file ):
    lines = open(file,"r").readlines()
    lines = [l.strip() for l in lines if l != ""]
    s2 = SudokuBoard(size=len(lines))

    def cell(c):
        if c == '*':
            return 0
        else:
            return int(c)

    for i in range(len(lines)):
        s2.fix_row( i, [cell(c) for c in lines[i]] )

    return s2
