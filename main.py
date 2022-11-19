from cmu_112_graphics import *
import math
import copy

class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [None for i in range(cols) for j in range(rows)]
        self.initialPlayer = None

    def getBoard(self):
        return self.board

    def saveOriginalBoard(self):
        originalBoard = copy.copy(self.board)
        return originalBoard

if __name__ == "__main__":
    rows = input("Choose num of rows")
    cols = input("Choose num of cols")
    g = Game(rows, cols)
    g.saveOriginalBoard()

