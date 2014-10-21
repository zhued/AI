# Project 1: Search (search.py, to accompany searchAgents.py)
# CSCI 3202 - Fall 2014
#
# Author: Edward Zhu
# Collaborators: Steven Tang

#
# ATTENTION !!!THE 4 WRITTEN QUESTIONS WILL BE RIGHT AFTER DFS SEARCH FUNCTION
#

# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    fringe = util.Stack()
    fringe.push( (problem.getStartState(), []) )
    while not fringe.isEmpty():
        state, path = fringe.pop()

        if problem.isGoalState(state):
            return path
        elif state not in visited:
            visited.add(state)
            for nextState, nextPath, cost in problem.getSuccessors(state):
                fringe.push((nextState, path + [nextPath] ))
    print "Unable to find a solution with DFS."
    return []

    
# 4 WRITTEN QUESTIONS
# 1. Is the exploration order what you would have expected?
#      Yes, because we are using a Stack, the Last in First Out 
#      property still holds true here. It will go all the way down 'side' of a 
#      tree to find the goal state, ALTHOUGH it doesn't traverse all 
#      paths; apparently it goes through and find a single working path
#      and returns it.
# 2. Does Pacman actually go to all the explored squares on his way to the goal?
#      No, because according to the behavior of the mazes given in this
#      assignment, DFS will just go through and find A path that works, after 
#      that it just returns the path, so it may not have traversed all the 
#      squares before reaching its goal.
# 3. Is this a least cost solution? If not, what is it doing wrong.
#      No because it doesn't find all the paths and compare them, it just finds
#      one path that ends at the goal state and returns it, whether or not that
#      is the optimal path because it doesn't compare anything to it. This is
#      apparent when running some of the tests, where DFS doesn't go for the optimal
#      paths, but the first path that it can find to the goal state
# 4. What happens to openMaze for the various search strategies?
#      BFS and Uniform Search traverses almost all the nodes and finds the optimal 
#      path in the end. But A* Search traverses less paths, but still finds the optimal 
#      path. DFS on the other hand, travels relevant to where the goal state is to the 
#      starting state.
#

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    fringe = util.Queue()
    fringe.push( (problem.getStartState(), []) )
    while not fringe.isEmpty():
        state, path = fringe.pop()
        visited.add(state)

        if problem.isGoalState(state):
            return path

        for nextState, nextPath, cost in problem.getSuccessors(state):
            if nextState not in visited:
                visited.add(nextState)
                fringe.push((nextState, path + [nextPath]))
    print "Unable to find a solution with BFS."
    return []         


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    visited = set()
    fringe = util.PriorityQueue()
    fringe.push( (problem.getStartState(), []), 0 )
    while not fringe.isEmpty():
        state, path = fringe.pop()
 
        if problem.isGoalState(state):
            return path

        if state not in visited:
            visited.add(state)
            for nextState, nextPath, cost in problem.getSuccessors(state):
                fringe.push((nextState, path + [nextPath]), problem.getCostOfActions(path + [nextPath]))
    print "Unable to find a solution with uniformCostSearch."
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    visited = set()
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    fringe.push( (startState, []), heuristic(startState, problem) )
    while not fringe.isEmpty():
        state, path = fringe.pop()
 
        if problem.isGoalState(state):
            return path

        if state not in visited:
            visited.add(state)
            for nextState, nextPath, cost in problem.getSuccessors(state):
                score = problem.getCostOfActions(path + [nextPath]) + heuristic(nextState, problem)
                fringe.push((nextState, path + [nextPath]), score)
    print "Unable to find a solution with aStarSearch."
    return []


class makeNode(object):
    def __init__(self,state=None,path=[],cost=0, h=0):
        self.state = state
        self.path  = path
        self.cost  = cost
        self.h     = h
    def __eq__(self, item):
        if item == None: return False
        return (self.state == item.state)&(self.path==item.path)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
