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
        smallest_distance = float('inf')
        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            if distance < smallest_distance:
                smallest_distance = distance
        foodLeft = len(newFood.asList())
        if foodLeft == 0:
            foodLeft = 1
        if smallest_distance == 0:
            smallest_distance = 1
        return successorGameState.getScore() + 1/foodLeft + 1/smallest_distance

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

        def mm_value(state=gameState, depth=self.depth, agentIndex=0, numAgents = gameState.getNumAgents()):
            if agentIndex == numAgents: # if index out of range reset from index 0
                agentIndex = 0
            if (depth==0 and agentIndex==0) or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            if agentIndex == 0:
                return max_value(state, depth-1, agentIndex, numAgents)
            if agentIndex != 0:
                return min_value(state, depth, agentIndex, numAgents)


        def max_value(state, depth, agentIndex, numAgents):
            v_max = float('-inf')
            pacmanLegalMoves = state.getLegalActions(agentIndex)
            for action in pacmanLegalMoves:
                agent_value = mm_value(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, numAgents) # smallest value ghost can return
                agent_value = agent_value[0] # smallest value ghost can return
                if agent_value > v_max: # largest value out of set of actions
                    v_max = agent_value
                    saved_action = action # action that got us there
            return v_max, saved_action

        def min_value(state, depth, agentIndex, numAgents):
            v_min = float('inf')
            ghostLegalMoves = state.getLegalActions(agentIndex)
            for action in ghostLegalMoves:
                v = mm_value(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, numAgents)
                v = v[0] # largest value pacman can return or smallest value next ghost can return
                if v < v_min:
                    v_min = v
            return v_min, None

        mm_value, action = mm_value()
        return action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def ab_value(state=gameState, depth=self.depth, agentIndex=0, numAgents = gameState.getNumAgents(), alpha = float('-inf'), beta = float('inf')):
            if agentIndex == numAgents: # if index out of range reset from index 0
                agentIndex = 0
            if (depth==0 and agentIndex==0) or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            if agentIndex == 0:
                return max_value(state, depth-1, agentIndex, numAgents, alpha, beta)
            if agentIndex != 0:
                return min_value(state, depth, agentIndex, numAgents, alpha, beta)


        def max_value(state, depth, agentIndex, numAgents, alpha, beta):
            v_max = float('-inf')
            pacmanLegalMoves = state.getLegalActions(agentIndex)
            for action in pacmanLegalMoves:
                agent_value = ab_value(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, numAgents, alpha, beta) # smallest value ghost can return
                agent_value = agent_value[0] # smallest value ghost can return
                if agent_value > v_max:
                    v_max = agent_value # largest value out of set of actions
                    saved_action = action # action that got us there
                alpha = max(alpha, v_max)
                if beta < alpha:
                    break
            return v_max, saved_action

        def min_value(state, depth, agentIndex, numAgents, alpha, beta):
            v_best = float('inf')
            ghostLegalMoves = state.getLegalActions(agentIndex)
            for action in ghostLegalMoves:
                v = ab_value(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, numAgents, alpha, beta) # largest value pacman can return or smallest value next ghost can return
                v = v[0] # largest value pacman can return or smallest value next ghost can return
                v_best = min(v_best, v) # best min value out of set of options
                beta = min(beta, v_best)
                if beta < alpha:
                    break
            return v_best, None

        ab_value, action = ab_value()
        return action
        util.raiseNotDefined()

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

        def mm_value(state=gameState, depth=self.depth, agentIndex=0, numAgents=gameState.getNumAgents()):
            if agentIndex == numAgents:  # if index out of range reset from index 0
                agentIndex = 0
            if (depth == 0 and agentIndex == 0) or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            if agentIndex == 0:
                return max_value(state, depth - 1, agentIndex, numAgents)
            if agentIndex != 0:
                return expec_value(state, depth, agentIndex, numAgents)

        def max_value(state, depth, agentIndex, numAgents):
            v_max = float('-inf')
            pacmanLegalMoves = state.getLegalActions(agentIndex)
            for action in pacmanLegalMoves:
                agent_value = mm_value(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, numAgents)  # smallest value ghost can return
                agent_value = agent_value[0]  # smallest value ghost can return
                if agent_value > v_max:  # largest value out of set of actions
                    v_max = agent_value
                    saved_action = action  # action that got us there
            return v_max, saved_action

        def expec_value(state, depth, agentIndex, numAgents):
            v = 0
            ghostLegalMoves = state.getLegalActions(agentIndex)
            numMoves = len(ghostLegalMoves)  # Number of moves for the ghost
            for action in ghostLegalMoves:
                p = 1/numMoves # probability of ghost move
                v += p * mm_value(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, numAgents)[0]
            return v, None

        expec_value, action = mm_value()
        return action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    foodGrid = currentGameState.getFood()
    pos = currentGameState.getPacmanPosition() # pacnman position
    newGhostStates = currentGameState.getGhostStates() # ghost states
    foodLeft = len(foodGrid.asList()) # number of food left for current state
    numRows = numColumns = 0

    smallestFoodDistance = float('inf')
    for food in foodGrid.asList():
        distance = manhattanDistance(pos, food)
        smallestFoodDistance = min(smallestFoodDistance, distance) # distance the closest food object

    ghostDistance = float('inf')
    for ghostState in newGhostStates:
        if ghostState.scaredTimer:
            score += ghostState.scaredTimer/ghostState.scaredTimer+10
            distance = manhattanDistance(pos, ghostState.getPosition())/manhattanDistance(pos, ghostState.getPosition())+ghostState.scaredTimer
        else:
            distance = manhattanDistance(pos, ghostState.getPosition())
        ghostDistance = min(ghostDistance, distance)

    for row in foodGrid:
        numRows += 1
    for column in foodGrid[0]:
        numColumns += 1

    ghostDistanceHeur = 1/(1 - ghostDistance/(numRows*numColumns)/10) # heuristic value based on ghost distance and scared time

    return score + 1/(foodLeft+1) + (1/(smallestFoodDistance+1))*ghostDistanceHeur

    util.raiseNotDefined()
# Abbreviation
better = betterEvaluationFunction
