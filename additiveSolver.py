import numpy as np
import sympy
from sympy.utilities.iterables import partitions


def numpyIndexesOf(array, value):
    return np.argwhere(array == value).flatten()


def numpyCount(array, value):
    return np.count_nonzero(array == value)


def convertMatrixToNumpy(matrix):
    return np.array(matrix).astype(np.float64)


def convertMatrixToSympy(matrix):
    return sympy.Matrix(matrix)


def convertToRREF(matrix):
    # Requires matrix to be in sympy format
    return matrix.rref(pivots=False)


def removeRowFromMatrix(rowIndex, matrix):
    # Works by taking other rows from before and after the deleted row
    # Then concatenates them together

    matrixPartOne = matrix[:rowIndex]
    matrixPartTwo = matrix[rowIndex + 1:]

    return np.vstack((matrixPartOne, matrixPartTwo))


def getPartitions(total, numOfIntegers):
    maxCellValue = 9
    groupPartitions = []

    for currentPartition in partitions(total, k=maxCellValue, m=numOfIntegers):

        # Removing partitions which aren't feasible in sudoku
        duplicateValues = not all(x == 1 for x in currentPartition.values())
        numEntries = len(currentPartition)

        if duplicateValues or (numEntries != numOfIntegers):
            continue

        # Changing format
        formattedPartition = tuple(currentPartition)
        groupPartitions.append(formattedPartition)

    return groupPartitions


# Assumes board is empty
def additiveSolve(groups, sumPerGroup):
    # Each matrix column represents 1 cell from the board, if it needs to be solved, it's represented by a 1

    numGroups = len(groups)
    matrix = np.zeros(shape=(27 + numGroups, 82))

    # Equations for each board column
    for columnNum in range(0, 9):
        matrixRow = columnNum
        matrix[matrixRow] = np.concatenate((
            np.repeat(0, columnNum * 9), np.repeat(1, 9), np.repeat(0, 81 - (columnNum + 1) * 9), [45]
        ))

    # Equations for each board row
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

    # Equations for each board cage
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

    # Using sympy function1
    matrix = convertMatrixToSympy(matrix)
    matrix = convertToRREF(matrix)
    matrix = convertMatrixToNumpy(matrix)

    # Removing any row of matrix ending with a negative number (or zero)
    # Removing any row of matrix with negative value for a cell

    # These are valid equations for the board, but are too problematic to use

    rowIndex = 0
    while rowIndex < matrix.shape[0]:
        row = matrix[rowIndex]

        # Checking end of row
        if row[-1] < 1:
            matrix = removeRowFromMatrix(rowIndex, matrix)

        # Checking cell values
        elif -1 in row[:-1]:
            matrix = removeRowFromMatrix(rowIndex, matrix)

        # Only increments in the else statement as the index will change everytime a row is removed
        else:
            rowIndex += 1

    # Analysing rref matrix to extract final cell results and possible cell values
    rowIndexes = []
    pivotIndexes = []
    '''numCellsThreshold = 4
    allPartitionsInfo = []'''

    for rowIndex, row in enumerate(matrix):

        rowWithoutSum = row[:-1]
        '''total = int(row[-1])'''
        numberOfOnes = numpyCount(rowWithoutSum, 1)

        '''# Optional, may improve speed by reducing unnecessary partitions with too many cells involved
        if numberOfOnes > numCellsThreshold:
            continue'''

        # Getting final values
        if numberOfOnes == 1:
            pivotIndex = numpyIndexesOf(rowWithoutSum, 1)[0]
            rowIndexes.append(rowIndex)
            pivotIndexes.append(pivotIndex)

        ''''# Getting possible cell values by looking at partitions provided by matrix
        if numberOfOnes > 1:
            pivots = numpyIndexesOf(rowWithoutSum, 1)

            currentPartitions = getPartitions(total, numberOfOnes)
            partitionInfo = (pivots, currentPartitions)
            allPartitionsInfo.append(partitionInfo)'''

    # Packing results to return
    results = np.empty(shape=(len(rowIndexes), 2))

    for rowNum, rowIndex in enumerate(rowIndexes):
        cellIndex = pivotIndexes[rowNum]
        cellValue = matrix[rowIndex][-1]

        results[rowNum] = cellIndex, cellValue

    return results

    ''', allPartitionsInfo'''
