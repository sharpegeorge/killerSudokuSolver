import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)

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

    if not cellIndex or not (cellRow and cellCol):
        logging.debug("Not providing cellIndex or cellPosition")

    if cellIndex:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    possibleBoardValues[cellRow, cellCol].fill(False)

    for value in values:
        indexCorrected = int(value - 1)
        possibleBoardValues[cellRow, cellCol, indexCorrected] = True

    updatePossibleValues(values, cellRow, cellCol)
    # triggers a check to see if it affects other possible cells
    # maybe remove it from func


def setIndividualPossibleCellValue(value, cellIndex=None, cellRow=None, cellCol=None):

    if not cellIndex or not (cellRow and cellCol):
        logging.debug("Not providing cellIndex or cellPosition")

    if cellIndex:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    indexCorrected = int(value - 1)
    possibleBoardValues[cellRow, cellCol, indexCorrected] = True

def removeIndividualPossibleCellValue(value, cellIndex=None, cellRow=None, cellCol=None):


# NEED TO MAKE FUNCTION TO SET INDIVIDUAL POSSIBLE VALUE OF A CELL


def updatePossibleValues(values, cellRow, cellCol):
    if len(values) == 1:
        print("placeholder updatePossibleValues ln50")
        # remove value from column, row, box and group (will need to take cages/pairings into account)

    # in column, row, box or group (individually tho):
    # check for v (num values) cells with identical values
        # if yes then remove values from all other set in the given column, row, box or group

    # something else i forgor




def logicSolve(board, groups, sumPerGroup):
    # Extracting data from board
    filledCellRows, filledCellCols = np.nonzero(board)
    filledCells = zip(filledCellRows, filledCellCols)

    # Adding data to possibleBoardValues
    for cellRow, cellCol in filledCells:
        cellValue = board[cellRow, cellCol]
        setPossibleCellValues(np.array([cellValue]), cellRow=cellRow, cellCol=cellCol)

    print(possibleBoardValues)
