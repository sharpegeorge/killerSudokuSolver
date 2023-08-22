import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

possibleBoardValues = np.full((9, 9, 9), True)


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
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition")

    if cellIndex:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    possibleBoardValues[cellRow, cellCol].fill(False)

    for value in values:
        indexCorrected = int(value - 1)
        possibleBoardValues[cellRow, cellCol, indexCorrected] = True

    updatePossibleValues(values, cellRow, cellCol)
    # triggers a check to see if it affects other possible cells
    # would affect cage,row,column,box

    # maybe remove it from func


def setIndividualPossibleCellValue(value, cellIndex=None, cellRow=None, cellCol=None):
    if not cellIndex or not (cellRow and cellCol):
        logging.debug("Not providing cellIndex or cellPosition")

    if cellIndex:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    indexCorrected = int(value - 1)
    possibleBoardValues[cellRow, cellCol, indexCorrected] = True


# Kept as a separate function from setValue function for abstraction
def removeIndividualPossibleCellValue(value, cellIndex=None, cellRow=None, cellCol=None):
    if not cellIndex or not (cellRow and cellCol):
        logging.debug("Not providing cellIndex or cellPosition")

    if cellIndex:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    indexCorrected = int(value - 1)
    possibleBoardValues[cellRow, cellCol, indexCorrected] = False


def updatePossibleValues(values, cellRow, cellCol):
    if len(values) == 1:
        print("placeholder updatePossibleValues ln78 logicSolver")
        # remove value from column, row, box and cage
        # (will need to update cages/pairings)

    # if values = values (in another len(values) cell(s) from same cage/col/row/box)
    # remove values from that cage/col/row/box
    # (will need to update cages/pairings)


# Main function
def logicSolve(board, groups, sumPerGroup):
    # Extracting data from board
    filledCellRows, filledCellCols = np.nonzero(board)
    filledCells = zip(filledCellRows, filledCellCols)

    # Adding data to possibleBoardValues
    for cellRow, cellCol in filledCells:
        cellValue = board[cellRow, cellCol]
        setPossibleCellValues(np.array([cellValue]), cellRow=cellRow, cellCol=cellCol)

    # final output should be possibleBoardValues where each cell has only 1 value
    return possibleBoardValues
