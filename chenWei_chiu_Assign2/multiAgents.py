# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """
        The idea is to calculate the distance from Pacman to (1) the food and (2) the ghosts, and use the reciprocals for evaluation.
        """
        # Initialize the score value
        totalScore = 0.0

        # Get the food list, and initialize a min food value
        foodList = newFood.asList()
        minFood = float('inf')
        # Find the min food value
        for food in foodList:
            foodDist = util.manhattanDistance(newPos, food)
            minFood = min(minFood, foodDist)
        totalScore += 1.0 / minFood

        # Now find the position of the ghosts; avoid getting too close to ghosts by penalizing total score
        for ghost in newGhostStates:
            ghostDist = util.manhattanDistance(newPos, ghost.getPosition())
            # If the Pacman is next to the ghost, penalize
            if (ghostDist <= 1):
                totalScore -= successorGameState.getScore() ** (2 * ghostDist)

        return successorGameState.getScore() + totalScore

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        """
        ---Pseudo-code from lecture---
        def value(state):
            if the state is a terminal state: return the state's utility
            if the next agent is MAX: return max-value(state)
            if the next agent is MIN: return min-value(state)

        def max-value(state):
            initialize v = float('-inf')
            for each successor of state:
                v = max(v, value(successor))
            return v

        def min-value(state):
            initialize v = float('inf')
            for each successor of state:
                v = min(v, value(successor))
            return v 
        """
        # Get number of agents
        numAgents = gameState.getNumAgents()
        # print(numAgents)

        # Pacman starts the call
        # Using only the action from the returned tuple of (action, action value)
        return self.maxValue(gameState, 0, numAgents, 0)[0]
    
    # Returns the value from the decision selected by the minimax agent
    def value(self, gameState, agentIndex, numAgents, depth):
        # Case if the state is a terminal state: end of depth in the decision tree, win, or loss
        if depth is self.depth * numAgents or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        # Case if the next agent is MAX (Pacman)
        if agentIndex is 0:
            return self.maxValue(gameState, agentIndex, numAgents, depth)[1]
        # Case if the next agent is MIN (ghosts)
        else:
            return self.minValue(gameState, agentIndex, numAgents, depth)[1]
    
    # Max-value function for Pacman; returns a tuple of (action, action value)
    def maxValue(self, gameState, agentIndex, numAgents, depth):
        # Initialize v to -inf
        decision = ("max", float('-inf'))
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            # Constructs successor
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorVal = self.value(successorState, (depth + 1) % numAgents, numAgents, depth + 1)
            # Update decision if successor has higher value
            if successorVal > decision[1]:
                decision = (action, successorVal)
        
        return decision

    # Min-value function for ghosts; returns a tuple of (action, action value)
    def minValue(self, gameState, agentIndex, numAgents, depth):
        # Initialize v to inf
        decision = ("min", float('inf'))
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            # Constructs successor
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorVal = self.value(successorState, (depth + 1) % numAgents, numAgents, depth + 1)
            # Update decision if successor has lower value
            if successorVal < decision[1]:
                decision = (action, successorVal)
        
        return decision

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """
        ---Pseudo-code from lecture---
        def value(state):
            if the state is a terminal state: return the state's utility
            if the next agent is MAX: return max-value(state)
            if the next agent is MIN: return min-value(state)

        def max-value(state, alpha, beta):
            initialize v = float('-inf')
            for each successor of state:
                v = max(v, value(successor))
                if v > beta
                    return v
                alpha = max(alpha, v)
            return v

        def min-value(state):
            initialize v = float('inf')
            for each successor of state:
                v = min(v, value(successor))
                if v < alpha
                    return v
                beta = min(beta, v)
            return v 
        """
        # Get number of agents
        numAgents = gameState.getNumAgents()

        # Initialize the alpha and beta values
        alpha = float('-inf')
        beta = float('inf')

        # Pacman starts the call
        # Using only the action from the returned tuple of (action, action value)
        return self.maxValue(gameState, 0, numAgents, 0, alpha, beta)[0]
    
    # Returns the value from the decision selected by the minimax agent
    def value(self, gameState, agentIndex, numAgents, depth, alpha, beta):
        # Case if the state is a terminal state
        if depth is self.depth * numAgents or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        # Case if the next agent is MAX (Pacman)
        if agentIndex is 0:
            return self.maxValue(gameState, agentIndex, numAgents, depth, alpha, beta)[1]
        # Case if the next agent is MIN (ghosts)
        else:
            return self.minValue(gameState, agentIndex, numAgents, depth, alpha, beta)[1]
    
    # Max-value function for Pacman; returns a tuple of (action, action value)
    def maxValue(self, gameState, agentIndex, numAgents, depth, alpha, beta):
        # Initialize v to -inf
        decision = ("max", float('-inf'))
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            # Constructs successor
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorVal = self.value(successorState, (depth + 1) % numAgents, numAgents, depth + 1, alpha, beta)
            # Update decision if successor has higher value
            if successorVal > decision[1]:
                decision = (action, successorVal)

            # The pruning step
            if decision[1] > beta:
                return decision
            else:
                alpha = max(alpha, decision[1])
        
        return decision

    # Min-value function for ghosts; returns a tuple of (action, action value)
    def minValue(self, gameState, agentIndex, numAgents, depth, alpha, beta):
        # Initialize v to inf
        decision = ("min", float('inf'))
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            # Constructs successor
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorVal = self.value(successorState, (depth + 1) % numAgents, numAgents, depth + 1, alpha, beta)
            # Update decision if successor has lower value
            if successorVal < decision[1]:
                decision = (action, successorVal)

            # The pruning step
            if decision[1] < alpha:
                return decision
            else:
                beta = min(beta, decision[1])
        
        return decision

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
