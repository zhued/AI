import sys
import math
import os.path

# used for keeping track of each district
District = []

class voter():
    ''' voter()
    A voter object represents one node on our inputted graph.
    Eventually, this node will be assigned to a district, which is
    tracked using the District[] list, and each node has a value, 
    which is what is inputted in the files.
    '''

    def __init__(self, vote):
        ''' __init__(vote)
        initializes the specified node with a specific value 'vote'
        '''
        self.district = None
        self.vote = vote

def build_graph():
    ''' build_graph()
    Builds a graph using the filename given in argv[1]
    Returns a nxn matrix of voter()'s where n is the number of lines in the file
    We have to assume that each graph is to be square
    '''
    # check to make sure we have enough arguments   
    if (len(sys.argv) < 2):
        print "ERROR: not enough arguments. usage: \n$ python gerrymander.py filename.txt"
        exit()
    # check to make sure the file to be read actually exists
    filename = sys.argv[1]
    if not (os.path.isfile(filename)):
        print "ERROR: file does not exist: '%s'  Exiting..." % filename
        exit()

    # building a nxn matrix from the input file.
    print 'Reading from %s' % filename
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    size = len(lines)
    graph = []
    for i in range(len(lines)):
        temp = []
        for j in lines[i].split():
            temp.append(voter(j))
        graph.append(temp)
    # necessary for ignoring the trailing blank line in largeNeighborhood.txt
    if graph[size-1]==[]:
        graph.pop(size-1)
    return graph


def is_valid_move(move, graph):
    for x,y in move:
        if graph[x][y].district != None:
            return False
    return True

def find_starting_node(x,y,graph):
    for i in range(x,len(graph)):
        for j in range(y,len(graph[i])):
            if graph[i][j].district == None:
                return i,j
    return None,None

def heuristic(move, graph):
    r = d = 0
    for x,y in move:
        if graph[x][y].vote == 'R':
            r = r+1
        elif graph[x][y].vote == 'D':
            d = d+1
    if r>d: return 1
    elif r<d: return -1
    else: return 0

def find_potential_move(x,y,graph):
    best_move = []
    move = []
    value = -2
    length = len(graph)
    # starting in the left most column
    if (y == 0):
        for i in range(length):
            for j in range(length):
                if graph[i][j].district == None:
                    move.append((i,j))
                if len(move) == length:
                    if is_valid_move(move,graph):
                        print 'valid move'
                        if heuristic(move,graph) > value:
                            best_move = move
                            value = heuristic(move,graph)
                            print 'value = %i' % value
                            print 'best_move' + str(best_move)
                            move = []
                        else:
                            print 'move is the same or worse, skipping'
                            move = []
                    else:
                        print 'invalid move'
                        move = []
    # starting in the top row
    if (x == 0):
        for j in range(length):
            for i in range(length):
                move.append((i,j))
                if len(move) == length:
                    if is_valid_move(move,graph):
                        print 'valid move'
                        if heuristic(move,graph) > value:
                            best_move = move
                            value = heuristic(move,graph)
                            print 'value = %i' % value
                            print 'best_move' + str(best_move)
                            move = []
                        else:
                            print 'move is the same or worse, skipping'
                            move = []
                    else:
                        print 'invalid move'
                        move = []

    return best_move


#TODO: make cases where no valid moves exist from the found starting node
# actually search through the graph to find ideal districts

#TODO: implement minimax search in here:
# involves building a tree of valid moves, and searching through to find the best one.
# start with trivial case, where each district is a 4x1 starting from (0,x)
def make_move(graph):
    if len(District) == len(graph):
        print "Warning: districts are already full, no moves are left."
        return graph

    x,y = find_starting_node(0,0,graph)
    if (x == None or y == None):
        print "no more valid starting nodes... somethings wrong"
        exit()
    move = find_potential_move(x,y,graph)
    print 'returned move' + str(move)
    # incomplete move, includes less than 4 nodes
    if (len(move) < len(graph)):
        print "ERROR: system found an invalid move.  Exiting..."
        exit()
    
    District.append(move)
    district_num = len(District)
    for x,y in move:
        graph[x][y].district = district_num

    return graph

def print_results(graph):
    print 'Printing results...'
    print
    print '*********************************************'
    print     
    print 'MAX=R'
    print 'MIN=D'
    print
    print '*********************************************'
    print
    for i in range(len(District)):
        tmp = []
        for x,y in District[i]:
            tmp.append(graph[x][y].vote)
        print 'District ' + str(i+1) + ': ' + str(tmp)
    print
    print '*********************************************'
    print
    R=D=0
    for i in range(len(District)):
        d = r = 0
        for x,y in District[i]:
            vote = graph[x][y].vote
            if vote == 'R':
                r = r+1
            elif vote == 'D':
                d = d+1 
        if r>d:
            result = 'R'
            R = R+1
        elif d>r:
            result = 'D'
            D=D+1
        else: #r==d
            result = 'T'
        print 'District ' + str(i+1) + ': ' + result
    print
    print '*********************************************'
    print
    if D>R:
        print 'Election outcome: D wins %i,%i,%i' % (R,D,len(graph)-R-D)
    elif R>D:
        print 'Election outcome: R wins %i:%i:%i' % (R,D,len(graph)-R-D)
    elif D==R:
        print 'Election outcome: Tied game'
    print
    print '*********************************************'

def gerrymander():
    graph = build_graph()
    print 'Gerrymandering.....'
    i = 1
    while len(District) < len(graph):
        print
        print 'move %i' % i
        graph = make_move(graph)
        i = i+1
    i=0
    print_results(graph)

gerrymander()