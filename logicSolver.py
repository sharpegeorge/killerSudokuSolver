import numpy as np
import logging
from sympy.utilities.iterables import partitions
from itertools import chain, permutations

'''Could optimise by storing group partitions in a data structure
and also only run the function if the value changed belongs to that partition'''

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

groups = []
sumPerGroup = []

recursionCounter = 0


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


def getPartitions(total, numOfIntegers, requiredNumbers=None):

    maxCellValue = 9
    groupPartitions = []

    for currentPartition in partitions(total, k=maxCellValue, m=numOfIntegers):

        # Removing partitions which aren't feasible in sudoku
        duplicateValues = not all(x == 1 for x in currentPartition.values())
        partitionSize = len(currentPartition)

        if duplicateValues or (partitionSize != numOfIntegers):
            continue

        if requiredNumbers is not None:
            validPartition = True
            for number in tuple(currentPartition.keys()):
                if number not in requiredNumbers:
                    validPartition = False
                    break

            if not validPartition:
                continue

        # Finding all permutations
        partitionPermutations = permutations(currentPartition)

        for permutation in tuple(partitionPermutations):
            groupPartitions.append(permutation)

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
        groupValues.append(getPossibleCellValues(cellRow=currentRow, cellCol=currentCol))


    return groupValues


def getPossibleCellValues(cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition a")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    results = np.empty(0, dtype=int)

    cellValuesBool = possibleBoardValues[cellRow, cellCol]

    for cellIndex, cellValueBool in enumerate(cellValuesBool):
        if cellValueBool:
            cellValue = cellIndex + 1

            results = np.append(results, cellValue)

    return results


# Overrides current data, does not append. Only used in setting up data
def setPossibleCellValues(values, cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition b")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    possibleBoardValues[cellRow, cellCol].fill(False)

    for value in values:
        indexCorrected = int(value - 1)
        possibleBoardValues[cellRow, cellCol, indexCorrected] = True

    updatePossibleValues(cellRow, cellCol)


def setIndividualPossibleCellValue(value, cellIndex=None, cellRow=None, cellCol=None):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition c")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    indexCorrected = int(value - 1)
    possibleBoardValues[cellRow, cellCol, indexCorrected] = True

    updatePossibleValues(cellRow, cellCol)


# Main backtracking function
def removeIndividualPossibleCellValue(value, cellIndex=None, cellRow=None, cellCol=None, update=True):
    if cellIndex is None and (cellRow is None or cellCol is None):
        logging.debug("Not providing cellIndex or cellPosition d")

    if cellIndex is not None:
        cellRow, cellCol = getCellPositionFromIndex(cellIndex)

    indexCorrected = int(value - 1)
    possibleBoardValues[cellRow, cellCol, indexCorrected] = False

    possibleValues = getPossibleCellValues(cellRow=cellRow, cellCol=cellCol)

    if update or len(possibleValues) == 1:
        updatePossibleValues(cellRow, cellCol)


def removeIdenticalValuesFromColumnExcept(identicalCellRows, values, column):
    for currentRow in range(9):

        if currentRow in identicalCellRows:
            continue

        for value in values:
            removeIndividualPossibleCellValue(value, cellRow=currentRow, cellCol=column, update=False)


def removeIdenticalValuesFromRowExcept(identicalCellColumns, values, row):
    for currentCol in range(9):

        if currentCol in identicalCellColumns:
            continue

        for value in values:
            removeIndividualPossibleCellValue(value, cellRow=row, cellCol=currentCol, update=False)


def removeIdenticalValuesFromBoxExcept(identicalBoxCellIndexes, values, row, column):
    boxIndexes = getBoxIndexes(row, column)

    for index in boxIndexes:
        currentRow, currentCol = getCellPositionFromIndex(index)

        if index in identicalBoxCellIndexes:
            continue

        for value in values:
            removeIndividualPossibleCellValue(value, cellRow=currentRow, cellCol=currentCol, update=False)

def removeValueFromGroup(value, group):
    for currentCellIndex in group:
        removeIndividualPossibleCellValue(value, cellIndex=currentCellIndex, update=False)

def getUniqueValuesFromPartitions(passedPartitions):
    allUniqueNumInPartitions = []

    for partition in passedPartitions:
        allUniqueNumInPartitions.extend(list(partition))

    set(allUniqueNumInPartitions)

    return allUniqueNumInPartitions


def updatePossibleValues(cellRow, cellCol):
    global groups
    global sumPerGroup

    possibleValues = getPossibleCellValues(cellRow=cellRow, cellCol=cellCol)
    cellIndex = getCellIndexFromPosition(cellRow, cellCol)

    # Executes if the value of the cell is known
    if len(possibleValues) == 1:
        value = int(possibleValues[0])

        # Getting the group the cell belongs to
        groupIndex = getIndex2DList(cellIndex, groups)

        if groupIndex is None:
            return

        # Subtracting value from group sum
        currentGroupSum = sumPerGroup[groupIndex]
        newGroupSum = currentGroupSum - value
        sumPerGroup[groupIndex] = newGroupSum

        if newGroupSum < 0:
            print("logicSolver.py Error - GroupSum set below 0.")

        # Removing cell from group

        currentGroup = groups[groupIndex]
        currentGroup.remove(cellIndex)
        groups[groupIndex] = currentGroup

        # If group has no other cells left, delete it
        if newGroupSum == 0:
            sumPerGroup = np.delete(sumPerGroup, groupIndex)
            del groups[groupIndex]

        # Removes value of passed cell from any cells in the same group
        for currentCellIndex in currentGroup:
            if currentCellIndex == cellIndex:
                continue

            currentCellValues = getPossibleCellValues(cellIndex=currentCellIndex)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, cellIndex=currentCellIndex, update=False)

        # Removes value of passed cell from any cells in the same row
        for currentColumn in range(9):
            if currentColumn == cellCol:
                continue

            currentCellValues = getPossibleCellValues(cellRow=cellRow, cellCol=currentColumn)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, cellRow=cellRow, cellCol=currentColumn)

        # Removes value of passed cell from any cells in the same column
        for currentRow in range(9):
            if currentRow == cellRow:
                continue

            currentCellValues = getPossibleCellValues(cellRow=currentRow, cellCol=cellCol)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, cellRow=currentRow, cellCol=cellCol)

        # Getting the box the cell belongs to

        boxIndex = getIndex2DList(cellIndex, boxes)
        currentBox = boxes[boxIndex]

        # Removes value of passed cell from any cells in the same box

        for currentCellIndex in currentBox:
            if currentCellIndex == cellIndex:
                continue

            currentCellValues = getPossibleCellValues(cellIndex=currentCellIndex)

            if value in currentCellValues:
                removeIndividualPossibleCellValue(value, cellIndex=currentCellIndex)

        return


    # Identifying and removing any possible values from cells in the same column

    columnPossibleValues = getColumnValues(cellCol)
    numIdenticalCellsInCol = countSpecificArraysInListOfArrays(columnPossibleValues, possibleValues)
    identicalCellRows = indexesOfSpecificArrayInList(columnPossibleValues, possibleValues)

    if numIdenticalCellsInCol == len(possibleValues):
        removeIdenticalValuesFromColumnExcept(identicalCellRows, possibleValues, cellCol)


    # Identifying and removing any possible values from cells in the same row

    rowPossibleValues = getRowValues(cellRow)
    numIdenticalCellsInRow = countSpecificArraysInListOfArrays(rowPossibleValues, possibleValues)
    identicalCellCols = indexesOfSpecificArrayInList(rowPossibleValues, possibleValues)

    if numIdenticalCellsInRow == len(possibleValues):
        removeIdenticalValuesFromRowExcept(identicalCellCols, possibleValues, cellRow)


    # Identifying and removing any possible values from cells in the same box

    boxPossibleValues = getBoxValues(cellRow, cellCol)
    numIdenticalCellsInBox = countSpecificArraysInListOfArrays(boxPossibleValues, possibleValues)

    identicalBoxCells = indexesOfSpecificArrayInList(boxPossibleValues, possibleValues)
    boxIndexes = getBoxIndexes(cellRow, cellCol)
    identicalBoxCellIndexes = [boxIndexes[index] for index in identicalBoxCells]

    if numIdenticalCellsInBox == len(possibleValues):
        removeIdenticalValuesFromBoxExcept(identicalBoxCellIndexes, possibleValues, cellRow, cellCol)


    # Identifying and removing any possible values from cells in the same group

    groupIndex = getIndex2DList(cellIndex, groups)

    if groupIndex is None:
        return

    group = groups[groupIndex]
    groupSum = sumPerGroup[groupIndex]

    allUniqueNumInGroup = []
    for currentCellIndex in group:
        currentCellValues = getPossibleCellValues(cellIndex=currentCellIndex)
        allUniqueNumInGroup.extend(currentCellValues)
    allUniqueNumInGroup = set(allUniqueNumInGroup)

    currentPartitions = getPartitions(groupSum, len(group), requiredNumbers=allUniqueNumInGroup)
    allUniqueNumInPartitions = getUniqueValuesFromPartitions(currentPartitions)

    # Removing all partitions that don't work from all group cells
    for partition in currentPartitions:
        usedCellValues = []
        usedCells = []
        for num in partition:
            numFound = False

            for currentCellIndex in group:
                if currentCellIndex in usedCells:
                    continue

                currentPossibleValues = getPossibleCellValues(currentCellIndex)

                if num in currentPossibleValues:
                    usedCells.append(currentCellIndex)
                    usedCellValues.append(num)
                    numFound = True
                    break

            if not usedCells:
                currentPartitions.remove(partition)
                allUniqueNumInNewPartitions = set(getUniqueValuesFromPartitions(currentPartitions))

                for number in partition:
                    if number not in allUniqueNumInNewPartitions:
                        removeValueFromGroup(number, group)
                break

            if not numFound:
                currentPartitions.remove(partition)
                allUniqueNumInNewPartitions = set(getUniqueValuesFromPartitions(currentPartitions))

                for index, currentCellIndex in enumerate(usedCells):
                    value = usedCellValues[index]
                    if value not in allUniqueNumInNewPartitions:
                        removeIndividualPossibleCellValue(value, cellIndex=currentCellIndex, update=False)
                break

            if num not in allUniqueNumInGroup:
                currentPartitions.remove(partition)
                allUniqueNumInNewPartitions = getUniqueValuesFromPartitions(currentPartitions)

                for number in partition:
                    if number not in allUniqueNumInNewPartitions:
                        removeValueFromGroup(number, group)

                break


    # Removing all possible values that don't fit into a partition
    for currentCellIndex in group:
        currentCellValues = getPossibleCellValues(cellIndex=currentCellIndex)
        for value in currentCellValues:
            if value not in allUniqueNumInPartitions:
                removeIndividualPossibleCellValue(value, cellIndex=currentCellIndex, update=True)


# Main function
def logicSolve(board, groupsPassed, sumPerGroupPassed):
    # Extracting data from board

    global groups
    global sumPerGroup

    groups = groupsPassed
    sumPerGroup = sumPerGroupPassed

    filledCellRows, filledCellCols = np.nonzero(board)
    filledCells = zip(filledCellRows, filledCellCols)

    # Adding data to possibleBoardValues
    for cellRow, cellCol in filledCells:
        cellValue = board[cellRow, cellCol]
        setPossibleCellValues(np.array([cellValue]), cellRow=cellRow, cellCol=cellCol)

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

                removeIndividualPossibleCellValue(value, cellIndex=cellIndex)

    # Final output should be possibleBoardValues where each cell has only 1 value

    return possibleBoardValues
