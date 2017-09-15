# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class Node:
	def __init__(self,state,action):
		self.state = state
		self.action = action
		self.parent = None
		self.cost = 0

	def setParent(self,parent):
		self.parent = parent

	def setCost(self,cost):
		self.cost = cost

	def getActions(self):
		actions=[]
		x=self
		while(x.parent!=None):
			actions.append(x.action)
			x=x.parent
		actions.reverse()
		return actions



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
    stack = util.Stack()
    visited = []
    startNode = Node(problem.getStartState(),None)
    stack.push(startNode)
    while stack.isEmpty()==False:
    	currentNode = stack.pop()
    	if problem.isGoalState(currentNode.state):
    		target=currentNode
    		print target.state
    		print target.getActions()
    		return target.getActions()
    	if currentNode.state not in visited:
    		visited.append(currentNode.state)
    		for successors in problem.getSuccessors(currentNode.state):
    			successorNode = Node(successors[0],successors[1])
    			successorNode.setParent(currentNode)
    			stack.push(successorNode)
    			
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    queue = util.Queue()
    visited = []
    startNode = Node(problem.getStartState(),None)
    queue.push(startNode)
    while queue.isEmpty()==False:
    	currentNode = queue.pop()
    	if problem.isGoalState(currentNode.state):
    		target=currentNode
    		return target.getActions()
    	if currentNode.state not in visited:
    		visited.append(currentNode.state)
    		for successors in problem.getSuccessors(currentNode.state):
    			successorNode = Node(successors[0],successors[1])
    			successorNode.setParent(currentNode)
    			queue.push(successorNode)
    			
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first. """
    pq = util.PriorityQueue()
    visited = []
    startNode = Node(problem.getStartState(),None)
    dist={startNode:0}
    print dist[startNode]
    pq.push(startNode,0)
    while pq.isEmpty()==False:
    	currentNode = pq.pop()
    	if problem.isGoalState(currentNode.state):
    		target=currentNode
    		return target.getActions()
    	if currentNode.state not in visited:
    		visited.append(currentNode.state)
    		for successors in problem.getSuccessors(currentNode.state):
    			successorNode = Node(successors[0],successors[1])
    			dist[successorNode]=successors[2]+dist[currentNode]
    			successorNode.setParent(currentNode)
    			pq.push(successorNode,dist[successorNode])
    			
    return []
    util.raiseNotDefined()
    """
    pq = util.PriorityQueue()
    start = (problem.getStartState(),None,0)
    pq.push(start,start[2])
    parent={start:None}
    dist={start:0}
    visited=[]
    actions=[]
    while pq.isEmpty()==False:
    	currentState = pq.pop()
    	if problem.isGoalState(currentState[0]):
    		target=currentState
    		break
    	if not problem.isVisited(currentState[0],visited):
    		visited.append(currentState[0])
    		for successors in problem.getSuccessors(currentState[0]):
    			dist[successors]=successors[2]+dist[currentState]
    			pq.push(successors,dist[successors])
    			parent[successors]=currentState
    state=target
    while(parent[state]!=None):
    	actions.append(state[1])
    	state=parent[state]
    actions.reverse()
    return actions
    """
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    pq = util.PriorityQueue()
    visited = []
    startNode = Node(problem.getStartState(),None)
    dist={startNode:0}
    print dist[startNode]
    pq.push(startNode,0)
    while pq.isEmpty()==False:
    	currentNode = pq.pop()
    	if problem.isGoalState(currentNode.state):
    		target=currentNode
    		return target.getActions()
    	if currentNode.state not in visited:
    		visited.append(currentNode.state)
    		for successors in problem.getSuccessors(currentNode.state):
    			successorNode = Node(successors[0],successors[1])
    			dist[successorNode]=successors[2]+dist[currentNode]
    			successorNode.setParent(currentNode)
    			pq.push(successorNode,dist[successorNode]+heuristic(successorNode.state,problem))
    			
    return []
    util.raiseNotDefined()
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
