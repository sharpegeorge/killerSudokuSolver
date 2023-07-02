import numpy as np
import sympy


def convertMatrixToNumpy(matrix):
    return np.array(matrix).astype(np.float64)


def convertMatrixToSympy(matrix):
    return sympy.Matrix(matrix)


def convertToRREF(matrix):
    # Requires matrix to be in sympy format
    return matrix.rref(pivots=False)


def additiveSolve(groups, sumPerGroup):
    # Each matrix column represents 1 cell from the board, if it needs to be solved, it's represented by a 1

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
        for cellIndex in boxCells:
            newRow[cellIndex] = 1

        # Saving to matrix
        matrixRow = boxNum + 18
        matrix[matrixRow] = newRow

    # equations for each board cage
    for groupNum, group in enumerate(groups):
        groupSum = sumPerGroup[groupNum]

        # Generates empty output
        newRow = np.concatenate((np.repeat(0, 81), [groupSum]))

        # Assigning 1s to cells of current group
        for cellIndex in group:
            newRow[cellIndex] = 1

        # Assigning to matrix
        matrixRow = groupNum + 27
        matrix[matrixRow] = newRow

    matrix = convertMatrixToSympy(matrix)
    matrix = convertToRREF(matrix)
    matrix = convertMatrixToNumpy(matrix)

    # Analysing rref matrix to extract final cell results

    rowIndexes = []
    pivotIndexes = []

    for rowNum, row in enumerate(matrix):
        counter = 0
        pivot = -1
        for elementNum, element in enumerate(row[:-1]):

            if element == 0:
                continue

            counter += 1
            if counter > 1:
                break

            if element == 1:
                pivot = elementNum

        if counter > 1 or pivot == -1:
            continue

        rowIndexes.append(rowNum)
        pivotIndexes.append(pivot)

    # Packing results to return

    results = np.empty(shape=(len(rowIndexes), 2))

    for rowNum, rowIndex in enumerate(rowIndexes):
        cellIndex = pivotIndexes[rowNum]
        cellValue = matrix[rowIndex][-1]

        results[rowNum] = cellIndex, cellValue

    return results
