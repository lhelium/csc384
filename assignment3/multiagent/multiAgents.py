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

        """Add more of your code here if you want to"""

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
        # if successor state is a win state, return a really high number
        # if the successor state is a lose state, return a really low number
        if successorGameState.isWin():
          score = float("inf")
          return score
        elif successorGameState.isLose():
          score = -float("inf")
          return score
        
        # get current position
        curPos = currentGameState.getPacmanPosition()

        # distance to food in current position
        curFoodList = currentGameState.getFood().asList()
        curFoodDistance = [manhattanDistance(food, curPos) for food in curFoodList]
        minCurFoodDistance = min(curFoodDistance) if len(curFoodDistance) > 0 else float("inf")

        # distance to food in new position
        newFoodList = newFood.asList()
        newFoodDistance = [manhattanDistance(food, newPos) for food in newFoodList]
        minNewFoodDistance = min(newFoodDistance) if len(newFoodDistance) > 0 else float("inf")

        # distance from ghosts in current position
        curGhostStates = currentGameState.getGhostStates()
        curGhostPos = [ghost.getPosition() for ghost in curGhostStates]
        curGhostDistance = [manhattanDistance(ghost, curPos) for ghost in curGhostPos]
        minCurGhostDistance = min(curGhostDistance) if len(curGhostDistance) > 0 else float("inf")

        # distance from ghosts in new position
        newGhostPos = [ghost.getPosition() for ghost in newGhostStates]
        newGhostDistance = [manhattanDistance(ghost, newPos) for ghost in newGhostPos]
        minNewGhostDistance = min(newGhostDistance) if len(newGhostDistance) > 0 else float("inf")
        
        score = 0

        # add score of new position relative to current position
        score += (successorGameState.getScore() - currentGameState.getScore())

        # reward: in new position, ghosts are further away
        if minNewGhostDistance > minCurGhostDistance:
          score += 1./minNewGhostDistance

        # reward: in new position, pacman is closer to food
        if minNewFoodDistance < minCurFoodDistance:
          score += 1./minNewFoodDistance

        return score

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
        #util.raiseNotDefined()

        # pacman is MAX so its corresponding agentIndex is 0
        # ghosts are MIN so their corresponding agentIndex is 1
        # pacman starts first
        def DFMiniMax(gameState, numMoves):
          agentIndex = numMoves % gameState.getNumAgents()
          currentDepth = numMoves/gameState.getNumAgents()

          bestMove = None

          if gameState.isWin() or gameState.isLose() or int(currentDepth) >= self.depth:
            return bestMove, self.evaluationFunction(gameState)
          
          if agentIndex == 0: # equivalent to "if player(pos) == MAX"
            value = -float("inf")
          else: # equivalent to "if player(pos) == MIN"
            value = float("inf")

          for move in gameState.getLegalActions(agentIndex):
            nextState = gameState.generateSuccessor(agentIndex, move)
            nextMove, nextVal = DFMiniMax(nextState, numMoves + 1)

            if agentIndex == 0 and value < nextVal:
              value, bestMove = nextVal, move
            if agentIndex != 0 and value > nextVal:
              value, bestMove = nextVal, move

          return bestMove, value

        bestMove, score = DFMiniMax(gameState, 0)

        return bestMove
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        def AlphaBeta(gameState, alpha, beta, numMoves):
          agentIndex = numMoves % gameState.getNumAgents()
          currentDepth = numMoves/gameState.getNumAgents()

          bestMove = None

          if gameState.isWin() or gameState.isLose() or int(currentDepth) >= self.depth:
            return bestMove, self.evaluationFunction(gameState)
          
          if agentIndex == 0: # equivalent to "if player(pos) == MAX"
            value = -float("inf")
          else: # equivalent to "if player(pos) == MIN"
            value = float("inf")

          for move in gameState.getLegalActions(agentIndex):
            nextState = gameState.generateSuccessor(agentIndex, move)
            nextMove, nextVal = AlphaBeta(nextState, alpha, beta, numMoves + 1)

            if agentIndex == 0:
              if value < nextVal:
                value, bestMove = nextVal, move

              if value >= beta:
                return bestMove, value

              alpha = max(alpha, value)

            if agentIndex != 0:
              if value > nextVal:
                value, bestMove = nextVal, move

              if value <= alpha:
                return bestMove, value
              
              beta = min(beta, value)

          return bestMove, value

        bestMove, value = AlphaBeta(gameState, -float("inf"), float("inf"), 0)

        return bestMove

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
        #util.raiseNotDefined()

        # compute the probability of a move
        # all ghosts choose uniformly at random from their legal moves
        # so probability = 1/len(number of legal moves)
        def prob(num_actions):
          ret = 1./num_actions
          return ret

        def Expectimax(gameState, numMoves):
          agentIndex = numMoves % gameState.getNumAgents()
          currentDepth = numMoves/gameState.getNumAgents()
          num_legal_actions = len(gameState.getLegalActions(agentIndex))

          bestMove = None

          if gameState.isWin() or gameState.isLose() or int(currentDepth) >= self.depth:
            return bestMove, self.evaluationFunction(gameState)
          
          if agentIndex == 0: # equivalent to "if player(pos) == MAX"
            value = -float("inf")
          else: # equivalent to "if player(pos) == CHANCE"
            value = 0

          for move in gameState.getLegalActions(agentIndex):
            nextState = gameState.generateSuccessor(agentIndex, move)
            nextMove, nextVal = Expectimax(nextState, numMoves + 1)

            if agentIndex == 0 and value < nextVal:
              value, bestMove = nextVal, move

            if agentIndex != 0:
              value = value + prob(num_legal_actions) * nextVal

          return bestMove, value

        bestMove, value = Expectimax(gameState, 0)

        return bestMove

def find_average(a_list):
  # return the average of the elements of a list
  # return inf if the list is empty
  avg = sum(a_list)/len(a_list) if len(a_list) > 0 else float("inf")
  return avg

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # if successor state is a win state, return a really high number
    # if the successor state is a lose state, return a really low number
    if currentGameState.isWin():
      score = float("inf")
      return score
    elif currentGameState.isLose():
      score = -float("inf")
      return score

    # get current position
    curPos = currentGameState.getPacmanPosition() 

    # distance to food in current position
    curFoodList = currentGameState.getFood().asList()
    curFoodDistance = [manhattanDistance(food, curPos) for food in curFoodList]
    #minCurFoodDistance = min(curFoodDistance) if len(curFoodDistance) > 0 else float("inf")

    # distance from ghosts in current position
    curGhostStates = currentGameState.getGhostStates()
    curGhostPos = [ghost.getPosition() for ghost in curGhostStates]
    curGhostDistance = [manhattanDistance(ghost, curPos) for ghost in curGhostPos]
    #minCurGhostDistance = min(curGhostDistance) if len(curGhostDistance) > 0 else float("inf")

    # distance to capsules in current position
    curCapsulesList = currentGameState.getCapsules()
    curCapsulesDistance = [manhattanDistance(capsule, curPos) for capsule in curCapsulesList]
    #minCurCapsuleDistance = min(curCapsulesDistance) if len(curCapsulesDistance) > 0 else float("inf")

    # scared times
    curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]
    sumCurScaredTimes = sum(curScaredTimes)

    score = 0

    # add score of new position relative to current position
    score += currentGameState.getScore()

    # avg distance to food (lower is better)
    avgCurFoodDistance = find_average(curFoodDistance)

    # encourage ghost to eat food
    # more food eaten (hence shorter list) is better
    numFood = len(curFoodList)
        
    # avg distance to capsule (lower is better)
    avgCurCapsuleDistance = find_average(curCapsulesDistance)

    # encourage ghost to eat capsules if number of food > 1
    numCapsules = len(curCapsulesList)

    # avg distance to ghosts
    avgCurGhostDistance = find_average(curGhostDistance)
    
    ghostScore = 0
    # if ghosts are scared, you can move closer to ghosts
    if sumCurScaredTimes > 0:
      ghostScore = min(curGhostDistance) if len(curGhostDistance) > 0 else float("inf")
    # otherwise, stay far away from ghosts
    else:
      ghostScore = max(curGhostDistance)  if len(curGhostDistance) > 0 else -float("inf")

    # calculate scores

    # if only one food left, encourage pacman to eat the food to end the game
    if numFood == 1:
      foodScore = 10 #1./avgCurFoodDistance + 10000 * 1./numFood if avgCurFoodDistance != 0 and numFood != 0 else 0
    else:
      foodScore = 1./avgCurFoodDistance + 1./numFood if avgCurFoodDistance != 0 and numFood != 0 else 0

    capsuleScore = 1./avgCurCapsuleDistance + 1./numCapsules if avgCurCapsuleDistance != 0 and numCapsules != 0 else 0

    ghostScore = 1./ghostScore if ghostScore != 0 else 0
    score += foodScore + capsuleScore + ghostScore

    return score
# Abbreviation
better = betterEvaluationFunction
