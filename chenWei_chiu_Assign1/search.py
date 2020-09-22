# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    """
    from game import Directions
    
    # initialize fringe and visited list
    fringe = util.Stack()
    visited = []

    # get start and push into the fringe
    start = problem.getStartState()
    fringe.push((start,[],0))

    # return if the starting point is the goal
    if problem.isGoalState(start):
        return []

    # loop while fringe is not empty
    while not fringe.isEmpty():
        (state, action, cost) = fringe.pop()
        if state not in visited:
            visited.append(state)

            # return action if the current point is the goal state
            if problem.isGoalState(state):
                return action

            # get successors
            successors = problem.getSuccessors(state)

            # push successors to the fringe
            for successor in successors:
                successorState = successor[0]
                successorAction = action + [successor[1]]
                successorCost = cost + successor[2]
                fringe.push((successorState, successorAction, successorCost))
    # print(action)
    # print()
    # util.raiseNotDefined()
    # return action

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    """Same implementation as DFS except that we use Queue here"""
    "*** YOUR CODE HERE ***"
    from game import Directions

    # initialize fringe and visited list
    fringe = util.Queue()
    visited = []

    # get start and push into the fringe
    start = problem.getStartState()
    fringe.push((start,[],0))

    # return if the starting point is the goal
    if problem.isGoalState(start):
        return []

    # pop the point and add to visited
    (state, action, cost) = fringe.pop()
    visited.append(state)

    # loop while goal not yet found
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        # add successors into visited
        for successor in successors:
            successorState = successor[0]
            if not successorState in visited:
                # update action and cost for the point
                successorAction = action + [successor[1]]
                successorCost = cost + successor[2]

                # push the point into the fringe
                fringe.push((successorState, successorAction, successorCost))
                visited.append(successorState)

        # pop the next point in fringe
        (state, action, cost) = fringe.pop()

    # print(action)
    # print()
    # util.raiseNotDefined()
    return action

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from game import Directions

    # initialize fringe and visited list
    fringe = util.PriorityQueue()
    visited = []

    # get start and push into the fringe with priority of 0
    start = problem.getStartState()
    fringe.push((start,[],0), 0)

    # return if the starting point is the goal
    if problem.isGoalState(start):
        return []

    # pop the point and add to visited
    (state, action, cost) = fringe.pop()
    visited.append((state, cost))

    # loop while goal not yet found
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        for successor in successors:
            pointVisited = False
            successorState = successor[0]
            totalCost = cost + successor[2]
            
            # check if current successor is already in visited
            for (visitedState, visitedCost) in visited:
                if (totalCost >= visitedCost) and (successorState == visitedState):
                    pointVisited = True
                    break
            
            # add point if not in visited
            if not pointVisited:
                # update action and cost for the point and push point to the fringe
                successorAction = action + [successor[1]]
                successorCost = cost + successor[2]
                fringe.push((successorState, successorAction, successorCost), successorCost)
                visited.append((successorState, successorCost))
        (state, action, cost) = fringe.pop()

    # print(action)
    # print()
    # util.raiseNotDefined()
    return action

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from game import Directions

    # initialize fringe and visited list
    fringe = util.PriorityQueue()
    visited = []

    # get the start state and heuristic cost, then push into fringe
    start = problem.getStartState()
    start_heuristic_cost = heuristic(start, problem)
    fringe.push((start, [], 0), 0 + start_heuristic_cost)

    # return if the starting point is the goal
    if problem.isGoalState(start):
        return []

    (state, action, cost) = fringe.pop()
    visited.append((state, cost + start_heuristic_cost))

    # loop while goal state not yet found
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        for successor in successors:
            pointVisited = False
            successorState = successor[0]
            totalCost = cost + successor[2]
            # check if current successor is already in visited
            for (visitedState, visitedCost) in visited:
                if (totalCost >= visitedCost) and (successorState == visitedState):
                    pointVisited = True
                    break
            
            # add point if not in visited
            if not pointVisited:
                # update action and cost for the point and push point to the fringe
                successorAction = action + [successor[1]]
                successorCost = cost + successor[2]
                successorHeuristicCost = successorCost + heuristic(successorState, problem)
                fringe.push((successorState, successorAction, successorCost), successorHeuristicCost)
                visited.append((successorState, successorCost))
        (state, action, cost) = fringe.pop()
        
    # print(action)
    # print()
    # util.raiseNotDefined()
    return action


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
