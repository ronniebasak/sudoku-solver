from typing import Dict, List, Tuple


def get_zone_boundary(v):
    zone_id = v//3
    return (zone_id*3, zone_id*3+2)

def get_uniques(arr):
    to_return = list(set(arr))
    to_return.remove(0)
    return to_return

def same_rows(c1, c2):
    x0, _ = c1
    x1, _ = c2
    return x0 == x1

def same_cols(c1, c2):
    _, y0 = c1
    _, y1 = c2
    return y0 == y1

def same_zone(c1, c2):
    x0,y0 = c1
    x1,y1 = c2
    return x0/3 == x1/3 and y0/3==y1/3

def possi(p):
    for key in p:
        print(key, p[key])





class Sudoku:
    board: List[List[int]] = [[0]*9]*9
    possibilities = None

    def __init__(self, board: List[List[int]] = None) -> None:
        if board:
            self.board = board


    def get_value(self, x,y):
        return self.board[y][x]


    def get_col_at(self, x):
        return list(row[x] for row in self.board)


    def get_row_at(self, y):
        return self.board[y]


    def get_zone_at(self, x,y):
        x0,x1 = get_zone_boundary(x)
        y0,y1 = get_zone_boundary(y)
        v = list(row[x0:x1+1] for  row in self.board[y0:y1+1])
        return v[0]+v[1]+v[2]


    def get_blocked_nums(self, x,y):
        if self.get_value(x,y) == 0:
            row = self.get_row_at(y)
            col = self.get_col_at(x)
            zone = self.get_zone_at(x,y)

            consumed = list(set(row+col+zone))
            consumed.remove(0)
            return consumed
        else:
            return False


    def get_possible_nums(self, x,y):
        all_possibles = set(range(1,10))
        _blocked = self.get_blocked_nums(x,y)
        if _blocked:
            blocked = set(_blocked)
            return list(all_possibles - blocked)
        else:
            return False


    def print_board(self):
        output = ""
        for y in range(0,9):
            for x in range(0,9):
                output += " "
                if self.board[y][x] == 0:
                    output += "_"
                else: 
                    output += str(self.board[y][x]) + " "
                if x == 2 or x == 5:
                    output += "|"
            
            if y == 2 or y == 5:
                output += "\n_____________________________"
            output += "\n"

        print(output)




class SudokuSolver:
    possibilities = {}
    sudoku = None

    def __init__(self, sudoku) -> None:
        self.sudoku = sudoku


    def calculate_possibilities(self):
        possibility_space = {}
        for y in range(0,9):
            for x in range(0,9):
                poss = self.sudoku.get_possible_nums(x,y)
                if poss:
                    possibility_space[(x,y)] = poss
        self.possibilities = possibility_space
        return possibility_space


    def set_num(self, x,y, v):
        self.sudoku.board[y][x] = v
        if self.possibilities:
            # delete this value for rows, cols and cell's possibility space
            for cell in self.possibilities:
                if self.possibilities[cell] and cell != (x,y):
                    # check if cell in same row
                    if (same_rows(cell, (x,y)) or same_cols(cell, (x,y)) or same_zone(cell, (x,y))) and v in self.possibilities[cell]:
                        self.possibilities[cell].remove(v)
        # possi(possibility_space)
        return True


    def solve(self, counter = 0):
        if not self.possibilities:
             self.calculate_possibilities()

        # go over the possibility space to find the following constraints
        # 1. is there only one possibility for a given number? then put it there and remove from possibility space
        # 2. if in a row, col or zone, a value occurs once, it goes there
        # possi(possibility_space)

        garbage = []
        nMatches = 0
        for cell in self.possibilities:
            x,y = cell
            if self.possibilities[cell] and len(self.possibilities[cell])==1:
                self.set_num(x,y, self.possibilities[cell][0])
                garbage+= [cell]
                nMatches += 1
            
        
        # collect garbage
        for g in garbage:
            del self.possibilities[g]
        
        # print "POSSIBILITY SPACE ", len(self.possibilities.keys())
        # print "Matches", nMatches
        # print "ROWS", possi_rows
        # print "COLS", possi_cols
        # print "ZONES", possi_zones
        # print 

        if len(self.possibilities.keys()) > 0 and nMatches > 0:
            self.solve(counter+1)

        else:
            self.sudoku.print_board()
        




puzzle_str = """
720090008
050380004
090000001
070806410
002004500
001730960
807000036
010463000
960000200
"""

def puzzle_import(puzzle):
    def listify(v):
        sam = list(v)
        return list(map(int, sam))

    tmp1 = puzzle.strip().split("\n")
    tmp2 = list(map(listify, tmp1))

    return Sudoku(tmp2)


puzzle = puzzle_import(puzzle_str)
solver = SudokuSolver(puzzle)
solver.solve()
