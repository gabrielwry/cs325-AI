# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provghostNumed that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provghostNume clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student sghostNume autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provghostNumed as a gughostNume.  You are welcome to change
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
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        #print newGhostStates
        #print
        #print newScaredTimes
        #print
        
        foodList = newFood.asList()
        ghostPosition = successorGameState.getGhostPositions()
        distFromGhost = []
        distToFood = []
        score = successorGameState.getScore()

        closestGhost = float("inf")
        closestGhostIndex = 0;
        for i,ghost in enumerate(ghostPosition):
          dist = manhattanDistance(ghost,newPos)
          distFromGhost.append(dist)
          if dist < closestGhost:
            closestGhost = dist
            closestGhostIndex = i
          if ghost is newPos:
            if newScaredTimes[i] > 0:
              score+=500

        closestFood = float("inf")
        for foodpos in foodList:
          dist = manhattanDistance(foodpos, newPos)
          distToFood.append(dist)
          if dist < closestFood:
            closestFood = dist

        numFood = len(foodList)


        if closestGhost < 2:
          if newScaredTimes[closestGhostIndex] > 3:
            closestGhost+=500
          else:            
            closestGhost-=5

        score += (closestGhost-3.0*closestFood-100.0*numFood)

        if successorGameState.isWin():
          return 100000

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
      This class provghostNumes some common elements to all of your
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

          Here are so me method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        agentNum = gameState.getNumAgents()
        def maxAgent(gameState, ghostNum, depth):
            # if reach the specific depth, or the gameState is at win or lose, no need to keep finding
            # further action, return the evaluate function
            if depth is self.depth or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)

            actions = gameState.getLegalActions(0)
            bestScore = -float("inf")
            bestAction = None

            for action in actions:
                state = gameState.generateSuccessor(0, action)
                score = minAgent(state, 1, depth)[0]
                if (score > bestScore):
                    bestScore = score
                    bestAction = action
            return (bestScore, bestAction)



        def minAgent(gameState, ghostNum, depth):
            if depth is self.depth or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)

            actions = gameState.getLegalActions(ghostNum)
            bestScore = float("inf")
            bestAction = None

            for action in actions:
                state = gameState.generateSuccessor(ghostNum, action)
                """
                main difference from pseudocode:
                keep track of the number of ghost

                """
                if (ghostNum is gameState.getNumAgents() - 1): #find steps for all ghost
                    score = maxAgent(state, ghostNum, depth+1)[0]
                else:
                    score = minAgent(state, ghostNum+1, depth)[0]
                if (score < bestScore):
                    bestScore = score
                    bestAction = action
            return (bestScore, bestAction)

        return maxAgent(gameState,agentNum,0)[1]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        agentNum = gameState.getNumAgents()
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, ghostNum, depth, alpha, beta):
            if depth is self.depth or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)

            actionList = gameState.getLegalActions(0)
            bestScore = -float("inf")
            bestAction = None

            for action in actionList:
                if alpha > beta:
                    return (bestScore, bestAction)
                state = gameState.generateSuccessor(0, action)
                score = minValue(state, 1, depth, alpha, beta)[0]
                if score > bestScore:
                    bestScore = score
                    bestAction = action
                if score > alpha:
                    alpha = score
            return (bestScore, bestAction)



        def minValue(gameState, ghostNum, depth, alpha, beta):
            if depth is self.depth or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            actionList = gameState.getLegalActions(ghostNum)
            bestScore = float("inf")
            bestAction = None

            for action in actionList:
                if alpha > beta:
                    return (bestScore, bestAction)

                state = gameState.generateSuccessor(ghostNum, action)
                if ghostNum is agentNum - 1:
                    score = maxValue(state, ghostNum, depth + 1, alpha, beta)[0]
                else:
                    score = minValue(state, ghostNum + 1, depth, alpha, beta)[0]

                if score < bestScore:
                    bestScore = score
                    bestAction = action
                if score < beta:
                    beta = score
            return (bestScore, bestAction)

        return maxValue(gameState, agentNum, 0, -float("inf"), float("inf"))[1]


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
        agentNum = gameState.getNumAgents()
        def maxAgent(gameState, ghostNum, depth):
            if depth is self.depth or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)

            actionList = gameState.getLegalActions(0)
            bestScore = -float("inf")
            bestAction = None

            for action in actionList:
                state = gameState.generateSuccessor(0, action)
                score = randAgent(state, 1, depth)[0]
                if (score > bestScore):
                    bestScore, bestAction = score, action
            return (bestScore, bestAction)



        def randAgent(gameState, ghostNum, depth):
            if depth is self.depth or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)
            actions = gameState.getLegalActions(ghostNum)
            totalScore = 0
            bestAction = None

            for action in actions:
                state = gameState.generateSuccessor(ghostNum, action)
                if (ghostNum == gameState.getNumAgents() - 1):
                    score = maxAgent(state,ghostNum, depth + 1)[0]
                else:
                    score = randAgent(state, ghostNum + 1, depth)[0]
                totalScore += score/len(actions)
            return (totalScore, bestAction)

        return maxAgent(gameState, agentNum, 0)[1]
        util.raiseNotDefined()






def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: By Priority
      1. safety: manhattanDist to the closestGhost-- get away if not aidble, approach if it is

      2. greedy: manhattanDist to the closestFood-- take the inverse of this to maximize greedy

      3. efficiency: number of foods dist 3 or less if move to next step -- go for more food

    """
    """
    if win or lose, return inf

    """
    """
    if currentGameState.isWin():
      return float("inf")
    if currentGameState.isLose():
      return -float("inf")

    """
    #useful information

    
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood() #food available from current state 
    capsules=currentGameState.getCapsules() #power pellets/capsules available from current state
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPosition = currentGameState.getGhostPositions()

    foodList = food.asList()
    distFromGhost = []
    distToFood = []
    ghostNum = currentGameState.getNumAgents()-1

    """
    #Safety:
    #closestFood and closestGhost

    """
    saftey = 0
    closestFood = float("inf")
    for food in foodList:
      dist = manhattanDistance(pos,food)
      if dist < closestFood:
        closestFood = dist

    closestGhost = (ghostNum+1,float("inf"))
    for i,ghost in enumerate(ghostPosition):
      dist = manhattanDistance(ghost,pos)
      if dist < closestGhost:
        closestGhost = (i,dist)

    closestGhostIndex = closestGhost[0]
    closestGhostDist = closestGhost[1]

    safety = -1.5*closestFood - 2*closestGhostDist
    if closestGhostDist < 2 :
      if scaredTimes[closestGhostIndex] > 0:
        safety += 10 #prefer to get close to this "scared" little piece of s...
      else:
        safety -= 10 #just get away
    if scaredTimes[closestGhostIndex] > 3:
      safety += 5 #let's go hunting

    """
    #Greedy:
    #length of foodList and palletList

    """
    greedy = 0
    greedy = -4*len(foodList)-20*len(capsules)
    """
    #Efficiency:
    #the number of food dist 2 from next step

    """
    efficiency = 0
    count = 0
    for x in range(pos[0]-5, pos[0]+5):
      for y in range(pos[1]-5, pos[1]+5):
        if (x,y) in range (0, len(foodList)) and food[x][y]:
          count+=1
    efficiency = -count

    if (len(foodList)==0):
      return float("inf")


    score = currentGameState.getScore()
    score += 1*safety+2*greedy+3*efficiency  #adjust the parameters

    return score

# Abbreviation
better = betterEvaluationFunction



class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

