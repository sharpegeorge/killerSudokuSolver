import numpy as np
import logging
from sympy.utilities.iterables import partitions
from itertools import chain

logging.basicConfig(level=logging.DEBUG)

possibleBoardValues = np.full((9, 9, 9), True)

boxes = np.array([
    [0, 1, 2, 9, 10, 11, 18, 19, 20],
    [3, 4, 5, 12, 13, 14, 21, 22, 23],
    [6, 7, 8, 15, 16, 17, 24, 25, 26],
    [27, 28, 29, 36, 37, 38, 45, 46, 47],
    [30, 31, 32, 39, 40, 41, 48, 49, 50],
    [33, 34, 35, 42, 43, 44, 51, 52, 53],
    [54, 55, 56, 63, 64, 65, 72, 73, 74],
    [57, 58, 59, 66, 67, 68, 75, 76, 77],
    [60, 61, 62, 69, 70, 71, 78, 79, 80]
])


def indexesOfSpecificArrayInList(listArray, array):
    indexes = []

    for index, currentArray in enumerate(listArray):
        if np.array_equal(currentArray, array):
            indexes.append(index)

    return indexes


def countSpecificArraysInListOfArrays(listArrays, array):
    count = 0

    for currentArray in listArrays:
        if np.array_equal(currentArray, array):
            count += 1

    return count


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


def getIndex2DList(value, arr):
    for rowNum, row in enumerate(arr):
        if value in row:
            return rowNum

    return None


def getCellPositionFromIndex(cellIndex):
    cellRow = int(cellIndex // 9)
    cellCol = int(cellIndex % 9)

    return cellRow, cellCol


def getCellIndexFromPosition(cellRow, cellCol):
    cellIndex = (cellRow * 9) + cellCol

    return cellIndex


def getColumnValues(cellCol):
    columnValues = []

    for row in range(9):
        columnValues.append(getPossibleCellValues(cellRow=row, cellCol=cellCol))

    return columnValues


def getRowValues(cellRow):
    rowValues = []

    for col in range(9):
        rowValues.append(getPossibleCellValues(cellRow=cellRow, cellCol=col))

    return rowValues


def getBoxIndexes(cellRow, cellCol):
    groupIndexes = []
    groupRow = cellRow // 3
    groupCol = cellCol // 3

    for cell in range(9):
        currentRow = (cell // 3) + (groupRow * 3)
        currentCol = (cell % 3) + (groupCol * 3)

        groupIndexes.append(getCellIndexFromPosition(currentRow, currentCol))

    return groupIndexes



def getBoxValues(cellRow, cellCol):
    groupValues = []
    groupRow = cellRow // 3
    groupCol = cellCol // 3


    for cell in range(9):
        currentRow = (cell // 3) + (groupRow * 3)
        currentCol = (cell % 3) + (groupCol * 3)
        groupValues.append(getPossibleCellValues(cellRow=currentRow, cellCol= currentCol))


    return groupValues


def getPossibleCellValues(cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition a")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    results = np.array([])

    cellValuesBool = possibleBoardValues[cellRow, cellCol]

    for cellIndex, cellValueBool in enumerate(cellValuesBool):
        if cellValueBool:
            cellValue = cellIndex + 1

            results = np.append(results, cellValue)

    return results


# Overrides current data, does not append. Only used in setting up data
def setPossibleCellValues(values, groups, sumPerGroup, cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition b")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    possibleBoardValues[cellRow, cellCol].fill(False)

    for value in values:
        indexCorrected = int(value - 1)
        possibleBoardValues[cellRow, cellCol, indexCorrected] = True

    updatePossibleValues(cellRow, cellCol, groups, sumPerGroup)


def setIndividualPossibleCellValue(value, groups, sumPerGroup, cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition c")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    indexCorrected = int(value - 1)
    possibleBoardValues[cellRow, cellCol, indexCorrected] = True

    updatePossibleValues(cellRow, cellCol, groups, sumPerGroup)


# Main backtracking function
def removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition d")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    indexCorrected = int(value - 1)
    possibleBoardValues[cellRow, cellCol, indexCorrected] = False

    updatePossibleValues(cellRow, cellCol, groups, sumPerGroup)


def removeIdenticalValuesFromColumnExcept(identicalCellRows, values, column, groups, sumPerGroup):
    for currentRow in range(9):

        if currentRow in identicalCellRows:
            continue

        for value in values:
            removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellRow=currentRow, cellCol=column)


def removeIdenticalValuesFromRowExcept(identicalCellColumns, values, row, groups, sumPerGroup):
    for currentCol in range(9):

        if currentCol in identicalCellColumns:
            continue

        for value in values:
            removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellRow=row, cellCol=currentCol)


def removeIdenticalValuesFromBoxExcept(identicalBoxCellIndexes, values, row, column, groups, sumPerGroup):
    boxIndexes = getBoxIndexes(row, column)

    for index in boxIndexes:
        currentRow, currentCol = getCellPositionFromIndex(index)

        if index in identicalBoxCellIndexes:
            continue

        for value in values:
            removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellRow=currentRow, cellCol=currentCol)


def updatePossibleValues(cellRow, cellCol, groups, sumPerGroup):
    possibleValues = getPossibleCellValues(cellRow=cellRow, cellCol=cellCol)
    cellIndex = getCellIndexFromPosition(cellRow, cellCol)

    # Executes if the value of the cell is known
    if len(possibleValues) == 1:
        value = possibleValues[0]

        # Removes value of passed cell from any cells in the same row
        for currentColumn in range(9):
            if currentColumn == cellCol:
                continue

            currentCellValues = getPossibleCellValues(cellRow=cellRow, cellCol=currentColumn)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellRow=cellRow, cellCol=currentColumn)

        # Removes value of passed cell from any cells in the same column
        for currentRow in range(9):
            if currentRow == cellRow:
                continue

            currentCellValues = getPossibleCellValues(cellRow=currentRow, cellCol=cellCol)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellRow=currentRow, cellCol=cellCol)

        # Getting the box the cell belongs to

        boxIndex = getIndex2DList(cellIndex, boxes)
        currentBox = boxes[boxIndex]

        # Removes value of passed cell from any cells in the same box

        for currentCellIndex in currentBox:
            if currentCellIndex == cellIndex:
                continue

            currentCellValues = getPossibleCellValues(cellIndex=currentCellIndex)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellIndex=currentCellIndex)

        # Getting the group the cell belongs to

        groupIndex = getIndex2DList(cellIndex, groups)
        currentGroup = groups[groupIndex]

        # Removes value of passed cell from any cells in the same group
        for currentCellIndex in currentGroup:
            if currentCellIndex == cellIndex:
                continue

            currentCellValues = getPossibleCellValues(cellIndex=currentCellIndex)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellIndex=currentCellIndex)

        # subtract value from specific groupsum

        # Needs to update rest of group base on groupsum (use partitions)
        '''2//////////////////////'''
        return


    # Identifying and removing any possible values from cells in the same column

    columnPossibleValues = getColumnValues(cellCol)
    numIdenticalCellsInCol = countSpecificArraysInListOfArrays(columnPossibleValues, possibleValues)
    identicalCellRows = indexesOfSpecificArrayInList(columnPossibleValues, possibleValues)

    if numIdenticalCellsInCol == len(possibleValues):
        removeIdenticalValuesFromColumnExcept(identicalCellRows, possibleValues, cellCol, groups, sumPerGroup)


    # Identifying and removing any possible values from cells in the same row

    rowPossibleValues = getRowValues(cellRow)
    numIdenticalCellsInRow = countSpecificArraysInListOfArrays(rowPossibleValues, possibleValues)
    identicalCellCols = indexesOfSpecificArrayInList(rowPossibleValues, possibleValues)

    if numIdenticalCellsInRow == len(possibleValues):
        removeIdenticalValuesFromRowExcept(identicalCellCols, possibleValues, cellRow, groups, sumPerGroup)


    # Identifying and removing any possible values from cells in the same box

    boxPossibleValues = getBoxValues(cellRow, cellCol)
    numIdenticalCellsInGroup = countSpecificArraysInListOfArrays(boxPossibleValues, possibleValues)

    identicalGroupCells = indexesOfSpecificArrayInList(boxPossibleValues, possibleValues)
    groupIndexes = getBoxIndexes(cellRow, cellCol)
    identicalGroupCellIndexes = [groupIndexes[index] for index in identicalGroupCells]

    if numIdenticalCellsInGroup == len(possibleValues):
        removeIdenticalValuesFromBoxExcept(identicalGroupCellIndexes, possibleValues, cellRow, cellCol, groups, sumPerGroup)

        # if len(partitions of cellRow and cellCol) == 1
        # subtract sum(partitions) from specific groupsum
        # remove possibleValues from other cells in the group


    # Identifying and removing any possible values from cells in the same group

    '''1//////////////////////////////////'''
    # count possibleValues in 2d array of group values
    # if ^count == len(possibleValues):
    # remove possibleValues from other cells in the box


    #

    '''groupIndex = getIndex2DList(cellIndex, groups)
    groupTotal = sumPerGroup[groupIndex]
    numGroupEntries = len(groups[groupIndex])'''



    '''3//////////////////////'''
    # (will need to update cages/pairings)


# Main function
def logicSolve(board, groups, sumPerGroup):
    # Extracting data from board
    filledCellRows, filledCellCols = np.nonzero(board)
    filledCells = zip(filledCellRows, filledCellCols)

    # Adding data to possibleBoardValues
    for cellRow, cellCol in filledCells:
        cellValue = board[cellRow, cellCol]
        setPossibleCellValues(np.array([cellValue]), groups, sumPerGroup, cellRow=cellRow, cellCol=cellCol)

    # Using group data to fill possible cell values
    for count, group in enumerate(groups):
        numCells = len(group)
        totalSum = sumPerGroup[count]
        possibleCombinations = getPartitions(totalSum, numCells)

        possibleValues = list(set(chain.from_iterable(possibleCombinations)))

        for cellIndex in group:
            for value in range(1, 10):

                if value in possibleValues:
                    continue

                removeIndividualPossibleCellValue(value, groups, sumPerGroup, cellIndex=cellIndex)

    # final output should be possibleBoardValues where each cell has only 1 value

    print(possibleBoardValues)

    return possibleBoardValues
