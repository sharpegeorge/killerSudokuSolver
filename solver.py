from additiveSolver import additiveSolve
from logicSolver import logicSolve
import numpy as np


board = np.zeros(shape=(9, 9))
isBoardComplete = False
maxIterations = 1000
iterationCounter = 0


def numpyIndexesOf(array, value):
    return np.argwhere(array == value).flatten()


def numpyCount(array, value):
    return np.count_nonzero(array == value)


def checkBoardComplete():
    return np.any(board == 0)


def getCellPositionFromIndex(cellIndex):
    cellRow = int(cellIndex // 9)
    cellCol = int(cellIndex % 9)

    return cellRow, cellCol


def saveToBoardCell(cellIndex, cellValue):
    cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    board[cellRow, cellCol] = cellValue


# test data
groups = [[0, 1, 9, 10], [2, 11], [3, 4], [5, 6, 7, 16], [8, 17], [12, 21], [13, 22], [14, 15], [23, 24], [25, 26],
          [27, 36, 37], [28, 29], [30, 31, 32], [33, 42, 43, 44], [34, 35], [38, 46, 47], [39, 48], [40, 41, 49],
          [45, 54], [50, 58, 59], [51, 52], [53, 62], [55, 64], [56, 57], [60, 61], [63, 72], [65, 66], [67, 75, 76],
          [68, 69, 70, 79], [71, 80], [73, 74], [77, 78]]

sumPerGroup = np.array(
    [25, 8, 13, 18, 8, 7, 13, 9, 8, 14, 18, 12, 14, 18, 16, 9, 10, 13, 9, 16, 9, 8, 14, 6, 14, 6, 15, 18, 14, 7, 11, 13])


# First using additiveSolve to get initial values
additiveResults = additiveSolve(groups, sumPerGroup)

# Add results to board
for cell in additiveResults:
    cellIndex, cellValue = cell
    saveToBoardCell(cellIndex, cellValue)

# Using backtracking algorithm
logicResults = logicSolve(board, groups, sumPerGroup)

# Format result from algorithms into readable format
for rowNum, row in enumerate(logicResults):
    for colNum, cell in enumerate(row):

        if numpyCount(cell, True) == 0:
            print("Solver.py error - logicSolver returned a cell with no possible values - ", rowNum + 1, colNum + 1)

        if numpyCount(cell, True) != 1:
            continue

        value = numpyIndexesOf(cell, True)[0] + 1
        board[rowNum, colNum] = value

print(board)
