import numpy as np
import sympy
import sys


np.set_printoptions(threshold=sys.maxsize)

def solve(groups, sumPerGroup):
    numGroups = len(groups)
    matrix = np.zeros(shape=(27 + numGroups, 82))

    # equations for each board column
    for columnNum in range(0, 9):
        matrixRow = columnNum
        matrix[matrixRow] = np.concatenate((
            np.repeat(0, columnNum * 9), np.repeat(1, 9), np.repeat(0, 81 - (columnNum + 1) * 9), [45]
        ))

    # equations for each board row
    for rowNum in range(0, 9):
        zeros = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        zeros[rowNum] = 1

        matrixRow = rowNum + 9
        matrix[matrixRow] = np.concatenate((
            np.tile(zeros, 9), [45]
        ))

    # Equations for each board box
    for boxNum in range(0, 9):
        # There are 3 rows of boxes. Calculates the box row for current box
        boxRow = boxNum // 3

        # Generates empty output
        newRow = np.concatenate((np.repeat(0, 81), [45]))

        # Base values for the first box stating the index of the cells
        baseValues = np.array([0, 1, 2, 9, 10, 11, 18, 19, 20])
        # Adjust values to account for positioning of current box
        boxCells = baseValues + ((3 * boxNum) + (18 * boxRow))

        # Assigning 1s to cells of current box
        for _, cellIndex in enumerate(boxCells):
            newRow[cellIndex] = 1

        # Saving to matrix
        matrixRow = boxNum + 18
        matrix[matrixRow] = newRow

    # equations for each board cage
    for groupNum, group in enumerate(groups):
        groupSum = sumPerGroup[groupNum]

        # Generates empty output
        newRow = np.concatenate((np.repeat(0, 81), [groupSum]))

        for _, cellIndex in enumerate(group):
            newRow[cellIndex] = 1

        matrixRow = groupNum + 27
        matrix[matrixRow] = newRow



    print(sympy.Matrix(matrix).rref())


groups = [[0, 9], [1, 2], [3, 4, 12, 13], [5, 6, 14, 15, 24], [7, 8], [10, 11, 18, 19],
          [20, 21], [22, 23, 32, 33], [16, 17, 26], [25, 34], [27, 36], [28, 37], [29, 30, 31], [35, 43, 44, 52, 53],
        [38, 39], [40, 41], [42, 51, 60, 59], [45, 46], [47, 56], [48, 49, 50], [54, 63, 72] ,[55, 64, 65], [57,58],
          [61, 62], [66, 67, 75, 76], [68, 77], [69,70], [71, 80], [73,74], [78, 79]]

sumPerGroup = np.array([8, 15, 20, 21, 10, 16, 13, 22, 20, 7, 16, 7, 6, 27, 9, 14, 18, 14, 8, 14, 11, 19, 9, 11, 20, 14, 9, 10, 10, 7])
solve(groups, sumPerGroup)
