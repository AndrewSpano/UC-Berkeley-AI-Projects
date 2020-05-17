# to run kakuro just enter in terminal: python3 kakuro.py

import csp
import time
from csp import *

# difficulty 0
kakuro1 = [['*', '*', '*', [6, ''], [3, '']],
           ['*', [4, ''], [3, 3], '_', '_'],
           [['', 10], '_', '_', '_', '_'],
           [['', 3], '_', '_', '*', '*']]

# difficulty 0
kakuro2 = [
    ['*', [10, ''], [13, ''], '*'],
    [['', 3], '_', '_', [13, '']],
    [['', 12], '_', '_', '_'],
    [['', 21], '_', '_', '_']]

# difficulty 1
kakuro3 = [
    ['*', [17, ''], [28, ''], '*', [42, ''], [22, '']],
    [['', 9], '_', '_', [31, 14], '_', '_'],
    [['', 20], '_', '_', '_', '_', '_'],
    ['*', ['', 30], '_', '_', '_', '_'],
    ['*', [22, 24], '_', '_', '_', '*'],
    [['', 25], '_', '_', '_', '_', [11, '']],
    [['', 20], '_', '_', '_', '_', '_'],
    [['', 14], '_', '_', ['', 17], '_', '_']]

# difficulty 2
kakuro4 = [
    ['*', '*', '*', '*', '*', [4, ''], [24, ''], [11, ''], '*', '*', '*', [11, ''], [17, ''], '*', '*'],
    ['*', '*', '*', [17, ''], [11, 12], '_', '_', '_', '*', '*', [24, 10], '_', '_', [11, ''], '*'],
    ['*', [4, ''], [16, 26], '_', '_', '_', '_', '_', '*', ['', 20], '_', '_', '_', '_', [16, '']],
    [['', 20], '_', '_', '_', '_', [24, 13], '_', '_', [16, ''], ['', 12], '_', '_', [23, 10], '_', '_'],
    [['', 10], '_', '_', [24, 12], '_', '_', [16, 5], '_', '_', [16, 30], '_', '_', '_', '_', '_'],
    ['*', '*', [3, 26], '_', '_', '_', '_', ['', 12], '_', '_', [4, ''], [16, 14], '_', '_', '*'],
    ['*', ['', 8], '_', '_', ['', 15], '_', '_', [34, 26], '_', '_', '_', '_', '_', '*', '*'],
    ['*', ['', 11], '_', '_', [3, ''], [17, ''], ['', 14], '_', '_', ['', 8], '_', '_', [7, ''], [17, ''], '*'],
    ['*', '*', '*', [23, 10], '_', '_', [3, 9], '_', '_', [4, ''], [23, ''], ['', 13], '_', '_', '*'],
    ['*', '*', [10, 26], '_', '_', '_', '_', '_', ['', 7], '_', '_', [30, 9], '_', '_', '*'],
    ['*', [17, 11], '_', '_', [11, ''], [24, 8], '_', '_', [11, 21], '_', '_', '_', '_', [16, ''], [17, '']],
    [['', 29], '_', '_', '_', '_', '_', ['', 7], '_', '_', [23, 14], '_', '_', [3, 17], '_', '_'],
    [['', 10], '_', '_', [3, 10], '_', '_', '*', ['', 8], '_', '_', [4, 25], '_', '_', '_', '_'],
    ['*', ['', 16], '_', '_', '_', '_', '*', ['', 23], '_', '_', '_', '_', '_', '*', '*'],
    ['*', '*', ['', 6], '_', '_', '*', '*', ['', 15], '_', '_', '_', '*', '*', '*', '*']]





class Kakuro(csp.CSP):

    def __init__(self, puzzle):

        self.variables = []
        self.neighbors = {}
        self.domains = {}
        self.puzzle = puzzle

        # iterate through the puzzle to find the above information
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):

                # if we have a new variable
                if puzzle[i][j] == '_':

                    # mark it as a variable
                    var = (i, j)
                    self.variables.append(var)
                    self.neighbors[var] = []

                    # find its neighbors with the 4 ifs
                    if i > 0 and puzzle[i - 1][j] == '_':
                        neighbor = (i - 1, j)
                        self.neighbors[var].append(neighbor)

                    if i < len(puzzle) - 1 and puzzle[i + 1][j] == '_':
                        neighbor = (i + 1, j)
                        self.neighbors[var].append(neighbor)

                    if j > 0 and puzzle[i][j - 1] == '_':
                        neighbor = (i, j - 1)
                        self.neighbors[var].append(neighbor)

                    if j < len(puzzle[i]) - 1 and puzzle[i][j + 1] == '_':
                        neighbor = (i, j+ 1)
                        self.neighbors[var].append(neighbor)

                    # mark its domain
                    self.domains[var] = list(range(1, 10))


        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraints)





    # constraints function
    def constraints(self, varA, valueA, varB, valueB):

        # if they have the same value, return false
        if valueA == valueB:
            return False

        A_x, A_y = varA
        B_x, B_y = varB

        # get the current assignments
        assignment = self.infer_assignment()

        # determine whether the variables are horizontally or verctically placed
        is_row = True
        if A_x != B_x:
            is_row = False


        # get the current sum
        curr_sum = valueA + valueB
        # variable used to distinguish whether all variables of the same line
        # have been assigned values
        flag = True


        # if we have a row
        if is_row == True:

            row = A_x
            column = min(A_y, B_y) - 1

            # go the start to find the sum wanted, while checking for
            # non-satisfaction of the constraints
            while self.puzzle[row][column] == '_':

                if (row, column) not in assignment:
                    flag = False
                else:
                    value = assignment[(row, column)]
                    if value == valueA or value == valueB:
                        return False
                    curr_sum = curr_sum + value

                column = column - 1


            # get the sum tile
            pair = self.puzzle[row][column]

            # since we have a row, get the sum
            sum = pair[1]
            # see if current sums exceeds wanted sum
            if curr_sum > sum:
                return False


            # iterate to calculate the current sum
            column = min(A_y, B_y) + 1
            total_columns = len(self.puzzle[0])

            while column < total_columns and self.puzzle[row][column] == '_':

                if column != A_y and column != B_y:

                    if (row, column) not in assignment:
                        flag = False
                    else:
                        value = assignment[(row, column)]
                        if value == valueA or value == valueB:
                            return False
                        if curr_sum + value > sum:
                            return False
                        curr_sum = curr_sum + value

                column = column + 1




        # do exactly the same, but for columns instead of rows
        else:

            column = A_y
            row = min(A_x, B_x) - 1

            while self.puzzle[row][column] == '_':

                if (row, column) not in assignment:
                    flag = False
                else:
                    value = assignment[(row, column)]
                    if value == valueA or value == valueB:
                        return False
                    curr_sum = curr_sum + value

                row = row - 1

            pair = self.puzzle[row][column]

            sum = pair[0]
            if curr_sum > sum:
                return False

            row = min(A_x, B_x) + 1
            total_rows = len(self.puzzle)

            while row < total_rows and self.puzzle[row][column] == '_':

                if row != A_x and row != B_x:

                    if (row, column) not in assignment:
                        flag = False
                    else:
                        value = assignment[(row, column)]
                        if value == valueA or value == valueB:
                            return False
                        if curr_sum + value > sum:
                            return False
                        curr_sum = curr_sum + value

                row = row + 1



        # if all variables have been assigned values <=> flag == True and the
        # sum is not the wanted sum, return False
        if flag == True and curr_sum != sum:
            return False

        return True




    def solveBT(self):

        start = time.time()
        result = csp.backtracking_search(self,)
        end = time.time()

        print(result)
        print('total time in seconds for backtrack:')
        print(str(end - start))



    def solveMinCon(self):

        start = time.time()
        result = csp.min_conflicts(self,)
        end = time.time()

        print(result)
        print('total time in seconds for min-conflicts:')
        print(str(end - start))




# change below the puzzle used
# available puzzles are: kakuro1, kakuro2, kakuro3, kakuro4
mypuzzle = Kakuro(kakuro1)

mypuzzle.solveMinCon()
mypuzzle.solveBT()
