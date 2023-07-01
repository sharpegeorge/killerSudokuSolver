import numpy as np

# columns of matrix - first row of board is index 0-8, second row 9-17, etc
matrixWithoutGroups = np.array([
    # columns of board
    np.concatenate((np.repeat(1, 9), np.repeat(0, 81 - 9), [45])),
    np.concatenate((np.repeat(0, 9), np.repeat(1, 9), np.repeat(0, 81 - 18), [45])),
    np.concatenate((np.repeat(0, 18), np.repeat(1, 9), np.repeat(0, 81 - 27), [45])),
    np.concatenate((np.repeat(0, 27), np.repeat(1, 9), np.repeat(0, 81 - 36), [45])),
    np.concatenate((np.repeat(0, 36), np.repeat(1, 9), np.repeat(0, 81 - 45), [45])),
    np.concatenate((np.repeat(0, 45), np.repeat(1, 9), np.repeat(0, 81 - 54), [45])),
    np.concatenate((np.repeat(0, 54), np.repeat(1, 9), np.repeat(0, 81 - 63), [45])),
    np.concatenate((np.repeat(0, 63), np.repeat(1, 9), np.repeat(0, 81 - 72), [45])),
    np.concatenate((np.repeat(0, 72), np.repeat(1, 9), [45])),

    # rows of board

    # boxes of board
])


def solve(groups, sumPerGroup):
    groups = np.array([[0, 1, 79], [79, 7, 80]])
    sumPerGroup = np.array([19, 21])

    numGroups = groups.shape[0]
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

    print(matrix)


solve(5, 5)
