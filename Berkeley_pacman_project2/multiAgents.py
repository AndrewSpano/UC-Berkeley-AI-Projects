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

        # check if there is a ghost nearby. If there is then the state is bad
        # and therefore it gets evaluated with 0
        for ghostState in newGhostStates:
            if manhattanDistance(newPos, ghostState.getPosition()) <= 1:
                return 0

        # calculate the maximum distanced withing the given grid
        max_hor_dist = len(list(newFood))
        max_vert_dist = len(newFood[0])
        # max_manhattan_distance is an upper bound for the score
        max_manhattan_distance = max_hor_dist + max_vert_dist

        # get the food in the grid
        food_count = newFood.count()
        # if the food is 0, then the state is a goal state, so return the
        # highest possible score
        if food_count == 0:
            return max_hor_dist * max_vert_dist

        # get a the food as a list
        foodList = newFood.asList()
        # find the closest point. The closest_point() function is defined below
        closest = closest_point(newPos, foodList)
        # calculate the distance to the closest point
        closest_dist = manhattanDistance(newPos, closest)

        # the first term is used as an indicator that the food is #1 priority
        # the second term is always a float between 0 and 1, and it's use is
        # that for states with the same food_count, the one that is close to
        # the closest food, gets the highest score.
        # The reason we subtract it instead of adding it is because we want the
        # the term to get smaller (which means that we are getting close to the
        # the closest food)
        return (max_hor_dist * max_vert_dist - food_count) - float(closest_dist) / max_manhattan_distance
        # return successorGameState.getScore()




# return the closest point (food) from the current position
def closest_point(position, itemList):
    # start with the first point in the list, and then compare it with the others
    closest = itemList[0]
    min = manhattanDistance(position, closest)

    # iterate through the list to find the min
    for item in itemList:
        man_dist = manhattanDistance(position, item)
        if man_dist < min:
            min = man_dist
            closest = item

    return closest



# return the farthest point (food) from the current position
def farthest_point(position, itemList):
    # start with the first point in the list, and then compare it with the others
    farthest = itemList[0]
    max = manhattanDistance(position, farthest)

    # iterate through the list to find the max
    for item in itemList:
        man_dist = manhattanDistance(position, item)
        if man_dist < min:
            max = man_dist
            farthest = item

    return farthest


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
        """
        "*** YOUR CODE HERE ***"

        # pretty much self explanatory
        return self.Minimax(gameState, self.depth, 0)



    # Minimax algorithm implemented
    def Minimax(self, gameState, depth, player):

        # get the best move of its children
        max_value = self.MaxValue(gameState, depth, player)
        # max value[0] has the score, and max_value[1] has the action
        return max_value[1]


    # returns the max score of all the successor states, and the action which
    # produces it
    def MaxValue(self, gameState, depth, player):

        # if we reach a leaf, return the evaluation
        if depth == 0:
            return self.evaluationFunction(gameState), None

        # not sure if there is something like -infinity in python
        max_score = -9999999

        # get the legal actions of the maximizing player
        max_player_legal_actions = gameState.getLegalActions(player)
        # if there are no legal actions, then the state is evaluated with the
        # evaluation function
        if len(max_player_legal_actions) == 0:
            return self.evaluationFunction(gameState), None

        # Initialize and keep track of the best action in order to return it
        best_action = max_player_legal_actions[0]

        # for every action available
        for action in max_player_legal_actions:

            # get the successor state that is generated by doing this action
            new_state = gameState.generateSuccessor(player, action)
            # get the action info
            score_and_action = self.MinValue(new_state, depth, player + 1)

            # if it's better than the current maximizing action, update
            if score_and_action[0] > max_score:
                best_action = action
                max_score = score_and_action[0]

        # return the max score and the action which produces it
        return max_score, best_action




    # returns the min score of all the successor states, and the action which
    # produces it
    def MinValue(self, gameState, depth, player):

        # if we reach a leaf, return the evaluation
        if depth == 0:
            return self.evaluationFunction(gameState), None

        # not sure if there is something like infinity in python
        min_score = 9999999

        # get the legal actions of the minimizing player
        min_player_legal_actions = gameState.getLegalActions(player)
        # if there are no legal actions, then the state is evaluated with the
        # evaluation function
        if len(min_player_legal_actions) == 0:
            return self.evaluationFunction(gameState), None

        # Initialize and keep track of the best action in order to return it
        best_action = min_player_legal_actions[0]


        # for every action available
        for action in min_player_legal_actions:

            # get the successor state that is generated by doing this action
            new_state = gameState.generateSuccessor(player, action)

            # if this is the last min player (ghost) that is being explored
            if gameState.getNumAgents() == player + 1:

                # get the action info
                score_and_action = self.MaxValue(new_state, depth - 1, 0)
                # if it's better than the current minimizing action, update
                if score_and_action[0] < min_score:
                    best_action = action
                    min_score = score_and_action[0]

            # else if another ghost will play
            else:

                # get the action info
                score_and_action = self.MinValue(new_state, depth, player + 1)
                # if it's better than the current minimizing action, update
                if score_and_action[0] < min_score:
                    best_action = action
                    min_score = score_and_action[0]


        # return the min score and the action which produces it
        return min_score, best_action




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # pretty much self explanatory
        return self.AlphaBeta(gameState, self.depth, 0)


    # AlphaBeta search algorithm implemented
    def AlphaBeta(self, gameState, depth, player):

        # get the best move of its children
        max_value = self.MaxValue(gameState, depth, player, -9999999, 9999999)
        # max value[0] has the score, and max_value[1] has the action
        return max_value[1]



    # returns the max score of all the successor states, and the action which
    # produces it
    def MaxValue(self, gameState, depth, player, a, b):

        # if we reach a leaf, return the evaluation
        if depth == 0:
            return self.evaluationFunction(gameState), None


        # not sure if there is something like -infinity in python
        max_score = -9999999

        # get the legal actions of the maximizing player
        max_player_legal_actions = gameState.getLegalActions(player)
        # if there are no legal actions, then the state is evaluated with the
        # evaluation function
        if len(max_player_legal_actions) == 0:
            return self.evaluationFunction(gameState), None

        # Initialize and keep track of the best action in order to return it
        best_action = max_player_legal_actions[0]

        # for every action available
        for action in max_player_legal_actions:

            # get the successor state that is generated by doing this action
            new_state = gameState.generateSuccessor(player, action)
            # get the action info
            score_and_action = self.MinValue(new_state, depth, player + 1, a, b)

            # if it's better than the current maximizing action, update
            if score_and_action[0] > max_score:
                best_action = action
                max_score = score_and_action[0]

            # apply pruning to avoid unnecessary checks
            if score_and_action[0] > b:
                return score_and_action

            # update alpha parameter
            a = max(a, score_and_action[0])


        # return the max score and the action which produces it
        return max_score, best_action




    # returns the min score of all the successor states, and the action which
    # produces it
    def MinValue(self, gameState, depth, player, a, b):

        # if we reach a leaf, return the evaluation
        if depth == 0:
            return self.evaluationFunction(gameState), None

        # not sure if there is something like infinity in python
        min_score = 9999999

        # get the legal actions of the minimizing player
        min_player_legal_actions = gameState.getLegalActions(player)
        # if there are no legal actions, then the state is evaluated with the
        # evaluation function
        if len(min_player_legal_actions) == 0:
            return self.evaluationFunction(gameState), None

        # Initialize and keep track of the best action in order to return it
        best_action = min_player_legal_actions[0]


        # for every action available
        for action in min_player_legal_actions:

            # get the successor state that is generated by doing this action
            new_state = gameState.generateSuccessor(player, action)

            # if this is the last min player (ghost) that is being explored
            if gameState.getNumAgents() == player + 1:

                # get the action info
                score_and_action = self.MaxValue(new_state, depth - 1, 0, a, b)
                # if it's better than the current minimizing action, update
                if score_and_action[0] < min_score:
                    best_action = action
                    min_score = score_and_action[0]

                # apply pruning to avoid unnecessary checks
                if score_and_action[0] < a:
                    return score_and_action

                # update parameter b
                b = min(b, score_and_action[0])


            # else if another ghost will play
            else:

                # get the action info
                score_and_action = self.MinValue(new_state, depth, player + 1, a, b)
                # if it's better than the current minimizing action, update
                if score_and_action[0] < min_score:
                    best_action = action
                    min_score = score_and_action[0]

                # apply pruning to avoid unnecessary checks
                if score_and_action[0] < a:
                    return score_and_action

                # update parameter b
                b = min(b, score_and_action[0])


        # return the min score and the action which produces it
        return min_score, best_action



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

        # pretty much self explanatory
        return self.ExpectiMax(gameState, self.depth, 0)



    # Expectimax search algorithm implemented
    def ExpectiMax(self, gameState, depth, player):

        # get the best move of its children
        max_value = self.MaxValue(gameState, depth, player)
        # max value[0] has the score, and max_value[1] has the action
        return max_value[1]


    # returns the max score of all the successor states, and the action which
    # produces it
    def MaxValue(self, gameState, depth, player):

        # if we reach a leaf, return the evaluation
        if depth == 0:
            return self.evaluationFunction(gameState), None


        # not sure if there is something like -infinity in python
        max_score = -9999999

        # get the legal actions of the maximizing player
        max_player_legal_actions = gameState.getLegalActions(player)
        # if there are no legal actions, then the state is evaluated with the
        # evaluation function
        if len(max_player_legal_actions) == 0:
            return self.evaluationFunction(gameState), None

        # Initialize and keep track of the best action in order to return it
        best_action = max_player_legal_actions[0]

        # for every action available
        for action in max_player_legal_actions:

            # get the successor state that is generated by doing this action
            new_state = gameState.generateSuccessor(player, action)
            # get the action info
            score_and_action = self.ExpValue(new_state, depth, player + 1)

            # if it's better than the current maximizing action, update
            if score_and_action > max_score and action != Directions.STOP:
                best_action = action
                max_score = score_and_action


        # return the max score and the action which produces it
        return max_score, best_action



    # returns the expected value of the state, which is the average of the
    # evaluation of all child states
    def ExpValue(self, gameState, depth, player):

        # if we reach a leaf, return the evaluation
        if depth == 0:
            return self.evaluationFunction(gameState)


        # get the legal actions of the expectimax random player
        exp_player_legal_actions = gameState.getLegalActions(player)
        # if there are no legal actions, then the state is evaluated with the
        # evaluation function
        if len(exp_player_legal_actions) == 0:
            return self.evaluationFunction(gameState)

        # get the number of legal actions
        number_of_legal_actions = len(exp_player_legal_actions)
        # get the probability of every action happening
        uniform_probability_of_child = float(1) / number_of_legal_actions

        # average score of child states
        average = 0.0

        # for every action available
        for action in exp_player_legal_actions:

            # get the successor state that is generated by doing this action
            new_state = gameState.generateSuccessor(player, action)

            # if this is the last random player (ghost) that is being explored
            if gameState.getNumAgents() == player + 1:

                # get the action info
                score_and_action = self.MaxValue(new_state, depth - 1, 0)
                # update the average
                average = average + uniform_probability_of_child * score_and_action[0]

            # else if another ghost will play
            else:

                # get the action info
                score = self.ExpValue(new_state, depth, player + 1)
                # update the average
                average = average + uniform_probability_of_child * score


        # return the average
        return average




def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    current_position = currentGameState.getPacmanPosition()
    current_food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()

    # check if there is a ghost nearby. If there is then the state is bad
    # and therefore it gets evaluated with 0
    for ghostState in GhostStates:
        if manhattanDistance(current_position, ghostState.getPosition()) <= 1:
            return 0

    # calculate the maximum distanced withing the given grid
    max_hor_dist = len(list(current_food))
    max_vert_dist = len(current_food[0])
    # max_manhattan_distance is an upper bound for the score
    max_manhattan_distance = max_hor_dist + max_vert_dist

    # get the food in the grid
    food_count = current_food.count()
    # if the food is 0, then the state is a goal state, so return the
    # highest possible score
    if food_count == 0:
        return 2 * max_hor_dist * max_vert_dist

    # get the current_food as a list
    foodList = current_food.asList()



    # find the closest point. The closest_point() function is defined above
    closest = closest_point(current_position, foodList)
    # calculate the distance to the closest point
    closest_dist = manhattanDistance(current_position, closest)



    # find the minimum distance of the successor states
    min = closest_dist
    # get the legal_actions that the pacman can make
    legal_actions = currentGameState.getLegalActions()

    # for every legal action possible == every new state possible
    for action in legal_actions:

        # get the successor state that is generated by doing this action
        new_state = currentGameState.generateSuccessor(0, action)

        # get the coordinates of the pacman in the new state
        new_state_pos = new_state.getPacmanPosition()
        # calculate the manhattanDistance of the new position form the closest
        # point
        man_dist = manhattanDistance(new_state_pos, closest)

        # update if new min found
        if man_dist < min:
            min = man_dist



    # get info about the capsules remaining
    capsule_list = currentGameState.getCapsules()
    capsule_count = len(capsule_list)



    # remaining food plays the biggest role in the evaluation of the state
    food_factor = (max_hor_dist * max_vert_dist - food_count)
    # remaining capsules play the second biggest role in achieving a high score
    capsule_factor = (1.0 / 2) * (max_hor_dist * max_vert_dist - capsule_count)
    # get the relative distance of the current position to the closest point
    closest_point_factor = float(closest_dist) / max_manhattan_distance
    # get the relative distance of the closest successor of the current position
    # to the closest point
    closest_point_succesors_factor = float(min) / max_manhattan_distance

    # get the evaluation
    evaluation = food_factor + capsule_factor - closest_point_factor - closest_point_succesors_factor
    return evaluation




# Abbreviation
better = betterEvaluationFunction
