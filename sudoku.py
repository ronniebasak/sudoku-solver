# puzzle = [
#     [6,0,0,9,5,0,4,0,0],
#     [0,2,0,0,0,0,0,0,8],
#     [1,8,5,0,0,4,0,0,7],
#     [9,0,0,7,2,0,0,0,0],
#     [0,4,2,8,0,3,7,6,0],
#     [0,0,0,0,4,9,0,0,3],
#     [8,0,0,3,0,0,1,7,5],
#     [3,0,0,0,0,0,0,2,0],
#     [0,0,1,0,6,7,0,0,4]
# ]
puzzle = """
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

def listify(v):
    sam = list(v)
    return map(int, sam)

puzzle = puzzle.strip()
puzzle = puzzle.split("\n")
puzzle = map(listify, puzzle)


def get_num_at(x,y):
    return puzzle[y][x]

def get_col_at(x):
    return list(row[x] for row in puzzle)

def get_row_at(y):
    return puzzle[y]


def get_zone_boundary(v):
    zone_id = v/3
    return (zone_id*3, zone_id*3+2)

def get_zone_at(x,y):
    x0,x1 = get_zone_boundary(x)
    y0,y1 = get_zone_boundary(y)
    v = list(row[x0:x1+1] for  row in puzzle[y0:y1+1])
    return v[0]+v[1]+v[2]
    

def get_uniques(arr):
    to_return = list(set(arr))
    to_return.remove(0)
    return to_return

def get_blocked_nums(x,y):
    if get_num_at(x,y) == 0:
        row = get_row_at(y)
        col = get_col_at(x)
        zone = get_zone_at(x,y)

        consumed = list(set(row+col+zone))
        consumed.remove(0)
        return consumed
    else:
        return False

def get_possible_nums(x,y):
    all_possibles = set(range(1,10))
    _blocked = get_blocked_nums(x,y)
    if _blocked:
        blocked = set(_blocked)
        return list(all_possibles - blocked)
    else:
        return False

# hash the x,y co-ordinates and fill it up, 
# any value that is not here is guaranteed to have a value
# keys will contain a tuple of x,y pairs and values will contain an array
# when possibility space is zero, it's solved

def calculate_possibilities():
    possibility_space = {}
    for y in range(0,9):
        for x in range(0,9):
            poss = get_possible_nums(x,y)
            if poss:
                possibility_space[(x,y)] = poss
    
    return possibility_space

def print_board():
    for y in xrange(0,9):
        for x in xrange(0,9):
            if puzzle[y][x] == 0:
                print "_",
            else: 
                print puzzle[y][x],
            if x == 2 or x == 5:
                print "|",
        
        if y == 2 or y == 5:
            print "\n______________________"
        print "\n"




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

def set_num(x,y, v, possibility_space=None):
    puzzle[y][x] = v
    if possibility_space:
        # delete this value for rows, cols and cell's possibility space
        for cell in possibility_space:
            if possibility_space[cell] and cell != (x,y):
                # check if cell in same row
                if (same_rows(cell, (x,y)) or same_cols(cell, (x,y)) or same_zone(cell, (x,y))) and v in possibility_space[cell]:
                    possibility_space[cell].remove(v)

    # possi(possibility_space)
    return True

def possi(p):
    for key in p:
        print key, p[key]


def solve(possibility_space=None, counter = 0):
    # calculate initial possibility space if a state is not passed
    if not possibility_space:
        possibility_space = calculate_possibilities()
        # for key in possibility_space:
        #     print key, possibility_space[key]
    # go over the possibility space to find the following constraints
    # 1. is there only one possibility for a given number? then put it there and remove from possibility space
    # 2. if in a row, col or zone, a value occurs once, it goes there
    # possi(possibility_space)

    garbage = []
    nMatches = 0
    # possi_rows = {0:[], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    # possi_cols = {0:[], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    # possi_zones = {0:[], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

    for cell in possibility_space:
        x,y = cell
        # possi_rows[x] += [possibility_space[cell]]
        # possi_cols[y] += [possibility_space[cell]]
        # possi_zones[x/3+(y/3)*3] += [possibility_space[cell]]

        if possibility_space[cell] and len(possibility_space[cell])==1:
            set_num(x,y, possibility_space[cell][0], possibility_space)
            garbage+= [cell]
            nMatches += 1
        
    
    # collect garbage
    for g in garbage:
        del possibility_space[g]
    
    # print "POSSIBILITY SPACE ", len(possibility_space.keys())
    # print "Matches", nMatches
    # print "ROWS", possi_rows
    # print "COLS", possi_cols
    # print "ZONES", possi_zones
    # print 

    if len(possibility_space.keys()) > 0 and nMatches > 0:
        solve(possibility_space, counter+1)

    else:
        print_board()
    




solve()