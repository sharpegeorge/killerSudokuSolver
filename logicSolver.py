import numpy as np

possibleBoardValues = np.zeros(shape=(9, 9, 9), dtype=bool)
possibleBoardValues.fill(True)



def getCellPositionFromIndex(cellIndex):
    cellRow = int(cellIndex // 9)
    cellCol = int(cellIndex % 9)

    return cellRow, cellCol


def getPossibleCellValues(cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    cellValuesBool = possibleBoardValues[cellRow, cellCol]
    results = np.array([])

    for cellIndex, cellValueBool in enumerate(cellValuesBool):
        if cellValueBool:
            cellValue = cellIndex + 1

            results = np.append(results, cellValue)

    return results


# Overrides current data, does not append
def setPossibleCellValues(values, cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    possibleBoardValues[cellRow, cellCol].fill(False)

    for value in values:
        indexCorrected = int(value - 1)
        possibleBoardValues[cellRow, cellCol, indexCorrected] = True

    # triggers a check to see if it affects other possible cells


def logicSolve(board, groups, sumPerGroup):
    # Extracting data from board
    filledCellRows, filledCellCols = np.nonzero(board)
    filledCells = zip(filledCellRows, filledCellCols)

    # Adding data to possibleBoardValues
    for cellRow, cellCol in filledCells:
        cellValue = board[cellRow, cellCol]
        setPossibleCellValues(np.array([cellValue]), cellRow=cellRow, cellCol=cellCol)

    print(possibleBoardValues)
