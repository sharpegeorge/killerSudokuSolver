from os import system
import solver

instructions = """
Instructions on how to enter your board to be solve.
-----------------------------------------------------
1. You will be asked for a "cage"/"group" total.
2. You will be asked to enter a row and column number for each cell.
3. A board will be shown to help. An 'X' indicates the cell is taken from another group. 
   A '■' indicates a cell has been already selected for this group. This will be repeated until you enter "stop".
4. If you enter more than 81 cells, you will be asked to repeat this process. Also no input validation

Press enter to continue.
"""

board = """
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝
"""
#41
#45
#118

groupTotalText = "Please enter the total for group"
cellRowText = "Please enter the row for the next cell in group"
cellColText = "Please enter the column for the next cell in group"

def getCellIndexFromPosition(row, col):
    index = ((row-1) * 9) + (col-1)

    return index

def getCellPositionFromIndex(index):
    row = int(index // 9) + 1
    col = int(index % 9) + 1

    return row, col

def getBoardSpliceIndex(row, col):
    spliceIndex = 40 + (76 * (row-1)) + (3 * (col-1)) + (col-1//3)
    return spliceIndex

def clearGroupMarks(groupIndexes):

    for index in groupIndexes:
        row, col = getCellPositionFromIndex(index)
        markBoard(row, col, space=True)

def markBoard(row, col, cross=False, square=False, space=False):
    global board

    mark = '!'

    if not cross and not square and not space:
        print("userInterface Error - Did not enter cross or square when editing board")

    if cross:
        mark = 'X'

    elif square:
        mark = '■'

    elif space:
        mark = ' '

    spliceIndex = getBoardSpliceIndex(row, col)
    board = board[:spliceIndex] + mark + board[spliceIndex+1:]


print(instructions)
input()
system('cls')

validInput = False
while not validInput:

    groupCounter = 0
    sumPerGroup = []
    groups = []
    cellsEntered = []

    inputtingData = True
    while inputtingData:
        groupCounter += 1
        currentGroup = []

        print(groupTotalText, groupCounter, "\nor STOP to finish.\n")
        currentGroupTotal = input()
        system('cls')

        if currentGroupTotal.upper() == "STOP":
            inputtingData = False
            break

        sumPerGroup.append(int(currentGroupTotal))

        inputtingCell = True
        while inputtingCell:
            print(board)

            print(cellRowText, str(groupCounter) + ", with total:", currentGroupTotal, "\nor STOP to select a new group or UNDO to delete last group entry\n")
            cellRow = input()

            if cellRow.upper() == "STOP":
                system('cls')
                break

            if cellRow.upper() == "UNDO":
                sumPerGroup.pop()
                clearGroupMarks(currentGroup)
                groupCounter -= 1
                system('cls')
                inputtingCell = False
                break

            cellRow = int(cellRow)
            system('cls')

            print(cellColText, str(groupCounter) + ", with total:", currentGroupTotal, "\nor UNDO to delete last group entry\n")
            cellCol = input()

            if cellCol.upper() == "UNDO":
                # Removing from lists
                sumPerGroup.pop()
                cellsUndone = len(currentGroup)
                del cellsEntered[-cellsUndone:]

                # Resetting board and counter
                clearGroupMarks(currentGroup)
                groupCounter -= 1

                system('cls')
                inputtingCell = False
                break

            cellCol = int(cellCol)
            system('cls')

            markBoard(cellRow, cellCol, square=True)

            cellIndex = getCellIndexFromPosition(cellRow, cellCol)

            currentGroup.append(cellIndex)
            cellsEntered.append(cellIndex)

        if inputtingCell:
            groups.append(currentGroup)
            for cellIndex in currentGroup:
                cellRow, cellCol = getCellPositionFromIndex(cellIndex)
                markBoard(cellRow, cellCol, cross=True)

    if len(cellsEntered) <= 81:
        print(groups)
        print(sumPerGroup)

        solver.solve(groups, sumPerGroup)
        validInput = True
        break

    system('cls')
    print("Error, more than 81 cells entered.")
