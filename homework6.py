import numpy as np
def findprimus(num):
    if num < 2:
        return False
    for i in range(2, int(np.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def primusfound(arr):
    result = []
    for row in arr:
        if any(findprimus(num) for num in row):
            result.append(row)
    return np.array(result)
arr = np.array([[2, 3, 5], [4, 6, 8], [11, 13, 17], [7, 10, 13]])
print(primusfound(arr))

def checkerboard():
    return np.zeros((8,8), dtype=int)
print(checkerboard())

def oddcboard():
    board = np.empty((8,8), dtype=int)
    board[1::2] = np.tile([0, 1], 4)
    return board
print(oddcboard())

def fullboard():
    board = np.empty((8,8), dtype=int)
    board[1::2] = np.tile([0, 1], 4)
    board[0::2] = np.tile([1, 0], 4)
    return board
print(fullboard())

def backfull():
    board = np.empty((8,8), dtype=int)
    board[1::2] = np.tile([1, 0], 4)
    board[0::2] = np.tile([0, 1], 4)
    return board
print(backfull())

def expand(arr, num_spaces):
    space = ' ' * num_spaces
    return np.array([space.join(list(word)) for word in arr])
universe = np.array(['galaxy', 'clusters'])
print(expand(universe, 1))
print(expand(universe, 2))

def firstloser(arr):
    sadfind = np.partition(arr, 1, axis=0)
    return sadfind[1, :]
np.random.seed(123)
stars=np.random.randint(500, 2000, (5, 5))
print(firstloser(stars))

ebo=np.random.seed(123)
ebos=np.random.randint(500, 2000, (5, 5))
print(ebos)