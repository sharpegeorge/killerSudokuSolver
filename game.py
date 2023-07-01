import numpy as np

max_cage_size = 5

#2d array
index = [
    [0,1,2,3,4,5],
    [],
    [],
]

#jagged list
cages = [
    [],
    [],
    [],
]

def generateBoard():
    for row in range(1, 10):
        for column in range(1, 10):
            newNumber = np.random.randint(low=1, high=9)

    return np.random.randint(low=1, high=9, size=(9, 9), dtype=int)

def generateItem():
    # get box values left
    # get column values left
    # get row values left
    # get row values left
    return 0

def defineCages():
    return 0

def main():
    board = generateBoard()
    print(board)

if __name__ == '__main__':
    main()