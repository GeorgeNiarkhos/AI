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
import random, util, sys

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        
        newGhostPos = []
        for state in newGhostStates :
          newGhostPos.append(state.getPosition())
        dist = sys.maxint
        for pos in newGhostPos : 
          dist =  min(dist, manhattanDistance(pos, successorGameState.getPacmanPosition()))
        
        if (dist <= 2):
          return -50

        currentFood = currentGameState.getFood().asList()
        maxscore = -10
        for pos in currentFood :
          temp = sys.maxint / (manhattanDistance(pos, successorGameState.getPacmanPosition()) + 1) 
          if ( temp > maxscore ):
            maxscore = temp
        return maxscore

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
    
    def minValue(self, gameState, depth, index):
      if (gameState.isWin() or gameState.isLose()):
        return self.evaluationFunction(gameState)  
      score = sys.maxint
      for a in gameState.getLegalActions(index):
        if ((gameState.getNumAgents() - 1) == index):
          temp = self.maxValue(gameState.generateSuccessor(index, a), depth + 1)
        else:
          temp = self.minValue(gameState.generateSuccessor(index, a), depth, index + 1)
        score = min(score, temp)
      return score

    def maxValue(self, gameState, depth):
      if (gameState.isWin() or gameState.isLose() or self.depth == depth):
        return self.evaluationFunction(gameState)
      score = -sys.maxint - 1
      for a in gameState.getLegalActions(0):
        temp = self.minValue(gameState.generateSuccessor(0, a), depth, 1)
        if (score < temp):
          score = temp
          if (depth == 0):
            action = a
      if (depth == 0): 
        return action
      else:
        return score   

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
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 0)
        
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def minValueAB(self, gameState, a, b, depth, index):
      if (gameState.isWin() or gameState.isLose()):
        return self.evaluationFunction(gameState)  
      score = sys.maxint
      for ac in gameState.getLegalActions(index):
        if ((gameState.getNumAgents() - 1) == index):
          temp = self.maxValueAB(gameState.generateSuccessor(index, ac), a, b, depth + 1)
        else:
          temp = self.minValueAB(gameState.generateSuccessor(index, ac), a, b, depth, index + 1)
        score = min(score, temp)
        if (score < a):
          return score
        b = min(b, score)
      return score

    def maxValueAB(self, gameState, a, b, depth):
      if (gameState.isWin() or gameState.isLose() or self.depth == depth):
        return self.evaluationFunction(gameState)
      score = -sys.maxint - 1
      for ac in gameState.getLegalActions(0):
        temp = self.minValueAB(gameState.generateSuccessor(0, ac), a, b, depth, 1)
        if (score < temp):
          score = temp
          if (depth == 0):
            action = ac
          if (score > b):
            if (depth ==0):
              return action
            else:
              return score
          a = max(a,score)
      if (depth == 0):
        return action
      else:
        return score
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.maxValueAB(gameState, -sys.maxint - 1, sys.maxint, 0)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectValue(self, gameState, depth, index):
      if (gameState.isWin() or gameState.isLose()):
        return self.evaluationFunction(gameState)
      chance = 0
      for a in gameState.getLegalActions(index):
        if ((gameState.getNumAgents() - 1) == index):
          chance = chance + self.maxValue(gameState.generateSuccessor(index, a), depth + 1)
        else:
          chance = chance + self.expectValue(gameState.generateSuccessor(index, a), depth, index + 1)  
      return chance / float(len(gameState.getLegalActions(index)))

    def maxValue(self, gameState, depth):
      if (gameState.isWin() or gameState.isLose() or self.depth == depth):
        return self.evaluationFunction(gameState)
      score = -sys.maxint - 1
      for a in gameState.getLegalActions(0):
        temp = self.expectValue(gameState.generateSuccessor(0, a), depth, 1)
        if (score < temp):
          score = temp
          if (depth == 0):
            action = a
      if (depth == 0): 
        return action
      else:
        return score

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 0)
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    # "*** YOUR CODE HERE ***"
    

    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood().asList()
    curGhostStates = currentGameState.getGhostStates()
    capsulePos = currentGameState.getCapsules()
    
    
    ghostScore = 10.0
    foodScore = 10.0
    eat_ghostScore = 100.0
    capsule_leftScore = 50.0

    score = currentGameState.getScore()
    
    # CAPSULE
    if(len(capsulePos)):
      for pos in capsulePos:
        distance = manhattanDistance(curPos, pos)
        score = score - capsule_leftScore   
    
    
    # GHOSTS
    ghostS = 0
    for state in curGhostStates:
      distance = manhattanDistance(curPos, state.getPosition())  
      if distance > 0:          
        if state.scaredTimer > 0:  
          ghostS = ghostS + eat_ghostScore / (distance/2)
        else:
          ghostS = ghostS - ghostScore / distance
    score = score + ghostS

    # FOOD
    score = score - 2*currentGameState.getNumFood()*foodScore #more value to eat the food
    dist = []
    for pos in curFood:
      dist.append(manhattanDistance(pos, curPos))
    if len(dist):
      score = score + foodScore / (min(dist) + 0.01) # if dist == 1 add something less than foodscore

    return score
    

# Abbreviation
better = betterEvaluationFunction

