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

    # check if the starting state is a solution
    if problem.isGoalState(problem.getStartState()):
        return []

    # import the Stack class which will be used to pop the state the first state that was pushed (LIFO)
    from util import Stack
    stack = Stack()
    # the first item of the stack will be the starting state
    stack.push(problem.getStartState())

    # a dictionary (more like hash table) that is used to check if a state has already beem visited in O(1) time
    visited = {problem.getStartState(): True}
    # a dictionary (more like hash table) to store the path taken to reach every state
    path = {problem.getStartState(): []}

    # the currentState becomes the starting state
    currentState = problem.getStartState()

    while True:

        # if the stack is empty, then we have explored all states reachable from the StartState
        # and we did not get to the goal State. Therefore it is unreachable. So we return None.
        if stack.isEmpty():
            return None

        # pop the next state that will be visited
        currentState = stack.pop()
        # mark the state as visited in the dictionary
        visited[currentState] = True

        # check if the currentState is a solution to the problem, and if so return a list with the solution
        if problem.isGoalState(currentState):
            return path.get(currentState)

        # get the successors of the currentState
        successors = problem.getSuccessors(currentState)

        # REMEMBER: tuple[0] is the state, tuple[1] is the action and tuple[2] is the cost of the action
        for tuple in successors:

            # check if the state (tuple[0]) has already been visited
            if visited.get(tuple[0], None) == None:
                # if it hasn't, construct it's path in the path dictionary
                temp_list = path.get(currentState)[:]
                temp_list.append(tuple[1])
                path[tuple[0]] = temp_list

                # then push it into the stack
                stack.push(tuple[0])

    util.raiseNotDefined()





def breadthFirstSearch(problem):

    # check if the starting state is a solution
    if problem.isGoalState(problem.getStartState()):
        return []

    # import the Queue class which will be used to pop the state the first state that was pushed (FIFO)
    from util import Queue
    queue = Queue()
    # the first item of the queue will be the starting state
    queue.push(problem.getStartState())

    # a dictionary (more like hash table) that is used to check if a state has already beem visited in O(1) time
    visited = {problem.getStartState(): True}
    # a dictionary (more like hash table) to store the path taken to reach every state
    path = {problem.getStartState(): []}

    # the current state is initialized as the starting state
    currentState = problem.getStartState()

    while True:

        # if the queue is empty, then we have explored all states reachable from the StartState
        # and we did not get to the goal State. Therefore it is unreachable. So we return None.
        if queue.isEmpty():
            return None

        # pop the lastest state that was inserted
        currentState = queue.pop()
        # check if it is a solution, and if it is return the path
        if problem.isGoalState(currentState):
            return path.get(currentState)

        # get the successors of the current state
        successors = problem.getSuccessors(currentState)

        # REMEMBER: tuple[0] is the state, tuple[1] is the action and tuple[2] is the cost of the action
        for tuple in successors:

            # if the state has not been visited
            if visited.get(tuple[0], None) == None:
                # add the state (tuple[0]) to the visited dictionary and mark it's path using the path dictionary
                visited[tuple[0]] = True
                # the state's (tuple[0]) path is the path to it's predecessor (currentState) + the new action (tuple[2])
                temp_list = path.get(currentState)[:]
                temp_list.append(tuple[1])
                path[tuple[0]] = temp_list

                # push the state (tuple[0]) to the queue
                queue.push(tuple[0])

    util.raiseNotDefined()




def uniformCostSearch(problem):

    # check if the starting state is a solution
    if problem.isGoalState(problem.getStartState()):
        return []

    # import the Priority Queue class which will be used to pop the state with the lowest cost
    from util import PriorityQueue
    priority_queue = PriorityQueue()
    # the starting state has a cost of 0
    priority_queue.push(problem.getStartState(), 0)

    # a dictionary (more like hash table) that is used to check if a state has already beem visited in O(1) time
    visited = {problem.getStartState(): True}
    # a dictionary (more like hash table) to store the path taken to reach every state
    path = {problem.getStartState(): []}
    # a dictionary (more like hash table) to store the predecessor of every state
    # this dictionary is not needed in dfs and bfs because in those searches the predecessor
    # of a state is always the variable currentState
    predecessor = {problem.getStartState(): None}
    # a dictionary (more like hash table) to store lowest cost needed to reach every state
    # this dictionary was not used in the previous searches for the same reasons as above
    cost = {problem.getStartState(): 0}

    # the current state of the problem becomes the starting state
    currentState = problem.getStartState()

    while True:

        # if the priority queue is empty, then we have explored all states reachable from the StartState
        # and we did not get to the goal State. Therefore it is unreachable. So we return None.
        if priority_queue.isEmpty():
            return None

        # the new current state will become the successor state with the smallest priority (cost)
        currentState = priority_queue.pop()

        # check if the currentState is the goal State. If it is it means we have found a minimum cost
        # solution. Return the path we have built for it.
        if problem.isGoalState(currentState):
            return path.get(currentState);

        # get the successors states of the currentState
        successors = problem.getSuccessors(currentState)

        # REMEMBER: tuple[0] is the state, tuple[1] is the action and tuple[2] is the cost of the action
        for tuple in successors:

            if visited.get(tuple[0], None) == None:
                # mark state as visited
                visited[tuple[0]] = True
                # the predecessor of the state tuple[0] is the state from which we got the tuple, which is currentState
                predecessor[tuple[0]] = currentState
                # the cost of the state tuple[0] is equal to the cost to get to the previous state + the cost of the action
                cost[tuple[0]] = cost[predecessor[tuple[0]]] + tuple[2]
                # make the path
                temp_list = path.get(currentState)[:]
                temp_list.append(tuple[1])
                path[tuple[0]] = temp_list

                # push the state in the priority queue with its cost, which we calculated above
                priority_queue.push(tuple[0], cost[tuple[0]])

            else:
                # we have an already visited state, so we must check if the cost to get to it can be lowered.
                if cost[currentState] + tuple[2] < cost[tuple[0]]:
                    # if the above condition is true, we have found a lower cost for the state tuple[0]
                    # therefore we update the cost, the predecessor and the path of the state
                    cost[tuple[0]] = cost[currentState] + tuple[2]
                    predecessor[tuple[0]] = currentState
                    temp_list = path.get(currentState)[:]
                    temp_list.append(tuple[1])
                    path[tuple[0]] = temp_list

                    # update the new priority (cost) of the already visited state
                    priority_queue.update(tuple[0], cost[tuple[0]])

    util.raiseNotDefined()





def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0





def aStarSearch(problem, heuristic=nullHeuristic):

    # check if the starting state is a solution
    if problem.isGoalState(problem.getStartState()):
        return []

    # import the Priority Queue class which will be used to pop the state with the lowest cost
    from util import PriorityQueue
    priority_queue = PriorityQueue()
    # the starting state has a cost of 0
    priority_queue.push(problem.getStartState(), heuristic(problem.getStartState(), problem))

    # a dictionary (more like hash table) that is used to check if a state has already beem visited in O(1) time
    visited = {problem.getStartState(): True}
    # a dictionary (more like hash table) to store the path taken to reach every state
    path = {problem.getStartState(): []}
    # a dictionary (more like hash table) to store the predecessor of every state
    # this dictionary is not needed in dfs and bfs because in those searches the predecessor
    # of a state is always the variable currentState
    predecessor = {problem.getStartState(): None}
    # a dictionary (more like hash table) to store lowest cost needed to reach every state
    # this dictionary was not used in the previous searches for the same reasons as above
    cost = {problem.getStartState(): 0}

    # the current state of the problem becomes the starting state
    currentState = problem.getStartState()

    while True:

        # if the priority queue is empty, then we have explored all states reachable from the StartState
        # and we did not get to the goal State. Therefore it is unreachable. So we return None.
        if priority_queue.isEmpty():
            return None

        # the new current state will become the successor state with the smallest priority (cost)
        currentState = priority_queue.pop()

        # check if the currentState is the goal State. If it is it means we have found a minimum cost
        # solution. Return the path we have built for it.
        if problem.isGoalState(currentState):
            return path.get(currentState);

        # get the successors states of the currentState
        successors = problem.getSuccessors(currentState)

        # REMEMBER: tuple[0] is the state, tuple[1] is the action and tuple[2] is the cost of the action
        for tuple in successors:

            if visited.get(tuple[0], None) == None:
                # mark state as visited
                visited[tuple[0]] = True
                # the predecessor of the state tuple[0] is the state from which we got the tuple, which is currentState
                predecessor[tuple[0]] = currentState
                # the cost of the state tuple[0] is equal to the cost to get to the previous state + the cost of the action
                cost[tuple[0]] = cost[predecessor[tuple[0]]] + tuple[2]
                # make the path
                temp_list = path.get(currentState)[:]
                temp_list.append(tuple[1])
                path[tuple[0]] = temp_list

                # push the state in the priority queue with its cost + heuristic, which we calculated above
                priority_queue.push(tuple[0], cost[tuple[0]] + heuristic(tuple[0], problem))

            else:
                # we have an already visited state, so we must check if the cost to get to it can be lowered.
                if cost[currentState] + tuple[2] < cost[tuple[0]]:
                    # if the above condition is true, we have found a lower cost for the state tuple[0]
                    # therefore we update the cost, the predecessor and the path of the state
                    cost[tuple[0]] = cost[currentState] + tuple[2]
                    predecessor[tuple[0]] = currentState
                    temp_list = path.get(currentState)[:]
                    temp_list.append(tuple[1])
                    path[tuple[0]] = temp_list

                    # update the new priority (cost + heuristic) of the already visited state
                    priority_queue.update(tuple[0], cost[tuple[0]] + heuristic(tuple[0], problem))

    util.raiseNotDefined()




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

