from additiveSolver import additiveSolve
from logicSolver import logicSolve
import numpy as np


board = np.zeros(shape=(9, 9))
isBoardComplete = False
maxIterations = 100
iterationCounter = 0


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
groups = [[0, 9], [1, 2], [3, 4, 12, 13], [5, 6, 14, 15, 24], [7, 8], [10, 11, 18, 19], [20, 21], [22, 23, 32, 33],
          [16, 17, 26], [25, 34], [27, 36], [28, 37], [29, 30, 31], [35, 43, 44, 52, 53], [38, 39], [40, 41],
          [42, 51, 60, 59], [45, 46], [47, 56], [48, 49, 50], [54, 63, 72], [55, 64, 65], [57, 58], [61, 62],
          [66, 67, 75, 76], [68, 77], [69, 70], [71, 80], [73, 74], [78, 79]]

sumPerGroup = np.array(
    [8, 15, 20, 21, 10, 16, 13, 22, 20, 7, 16, 7, 6, 27, 9, 14, 18, 14, 8, 14, 11, 19, 9, 11, 20, 14, 9, 10, 10, 7])


# First using additiveSolve to get initial values
additiveResults = additiveSolve(groups, sumPerGroup)

# Add results to board
for cell in additiveResults:
    cellIndex, cellValue = cell
    saveToBoardCell(cellIndex, cellValue)

# Logic solve until complete
logicResults = logicSolve(board, groups, sumPerGroup)
'''while (not isBoardComplete) and (iterationCounter < maxIterations):
    iterationCounter += 1

    logicResults = logicSolve(board, groups, sumPerGroup)

    # Add results to board
    for cell in logicResults:
        cellIndex, cellValue = cell
        saveToBoardCell(cellIndex, cellValue)

    if checkBoardComplete():
        isBoardComplete = True'''

print(board)
