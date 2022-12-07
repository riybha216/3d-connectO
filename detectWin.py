from cmu_112_graphics import *

class WinDetection:
    def __init__(self, boards, numGrids):
        '''
        Initializes variables for WinDetection objects.

        Params:
        -boards: 3D list of all boards initialized
        -numGrids: positive integer denoting number of boards initialized -
        topmost board, which is used for placing pieces
        '''
        self.boards = boards
        self.numGrids = numGrids

    def detectHorizontalOnGrid(self):
        '''
        Returns boolean value based on whether a horizontal connectO has been
        created on either board.
        '''
        for board in self.boards:
            for row in board.board:
                if row[0] != None and len(set(row)) == 1:
                    return True
        return False

    def detectPositiveHorizontalAcrossGrids(self):
        '''
        Returns boolean value based on whether 
        '''
        locationsBottom, pointsBottom = [], []
        allCols = self.getColumns()

        for i in range(self.numGrids - 1):
            if allCols[self.numGrids - 1][0][i] != None:
                locationsBottom.append((0, i))

        numGrids = self.numGrids - 1
        if len(locationsBottom) > 0:
            for loc in locationsBottom:
                for i in range(numGrids):
                    if (allCols[numGrids][loc[0]][loc[1]] != 
                       allCols[numGrids - (i + 1)][loc[1] + i + 1][loc[0]]):
                        break
                    else:
                        pointsBottom.append(allCols[numGrids][loc[0]][loc[1]])
                        pointsBottom.append(allCols[numGrids - (i + 1)]
                                                   [loc[1] + i + 1][loc[0]])
                if (None not in pointsBottom and 
                    len(pointsBottom) > self.numGrids and 
                    len(set(pointsBottom)) == 1):
                    return True
                else:
                    break

    def detectNegativeHorizontalAcrossGrids(self):
        locationsTop, pointsTop = [], []
        numGrids = self.numGrids - 1
        allCols = self.getColumns()

        for i in range(self.numGrids - 1):
            if allCols[0][0][i] != None:
                locationsTop.append((0, i))

        if len(locationsTop) > 0:
            for loc in locationsTop:
                for i in range(numGrids):
                    if (allCols[0][loc[0]][loc[1]] != 
                       allCols[i + 1][loc[1] + i + 1][loc[0]]):
                        break
                    else:
                        pointsTop.append(allCols[0][loc[0]][loc[1]])
                        pointsTop.append(allCols[i + 1][loc[1] + i + 1]
                                                [loc[0]])

                if (None not in pointsTop and len(pointsTop) > self.numGrids 
                    and len(set(pointsTop)) == 1):
                    return True
                else:
                    return False
            
    def getColumns(self):
        allCols = []
        for board in self.boards:
            columns = list(zip(*board.board))
            allCols.append(columns)
        return allCols

    def detectVerticalOnGrid(self):
        '''
        works
        '''
        allCols = self.getColumns()
        for grid in allCols:
            for col in grid:
                if col[0] != None and len(set(col)) == 1:
                    return True
        return False

    def detectVerticalAcrossGrids(self):
        '''
        works
        '''
        pointsToCompare = []
        candidates = []
        currBoard = self.boards[0]
        for row in range(currBoard.rows):
            for col in range(currBoard.cols):
                if currBoard.board[row][col] != None:
                    pointsToCompare.append((row, col))
    
        for point in pointsToCompare:
            (row, col) = point
            for idx in range(self.numGrids-1, -1, -1):
                if self.boards[idx].board[row][col] == currBoard.board[row][col]:
                    candidates.append(self.boards[idx].board[row][col])

        if len(candidates) > 0 and None not in candidates and (candidates.count("gold") == self.numGrids
            or candidates.count("red") == self.numGrids):
            return True
        return False

    def detectPositiveDiagonalonGrid(self):
        '''
        works
        '''
        temp = []
        for board in self.boards:
            for i, row in enumerate(board.board):
                temp.append(row[i])
            if temp[0] != None and len(set(temp)) == 1: return True
            temp.clear()
        return False

    def detectPositiveDiagonalAcrossGrids(self):
        '''
        works
        '''
        points = []
        for i in range(self.numGrids):
            points.append(self.boards[self.numGrids - (1 + i)].board[i][i])

        if None not in points and len(set(points)) == 1:
            return True
        else:
            return False
     
    def detectNegativeDiagonalonGrid(self):
        '''
        works
        '''
        temp = []
        for board in self.boards:
            for i, row in enumerate(board.board[::-1]):
                temp.append(row[i])
            if temp[0] != None and len(set(temp)) == 1: return True
            temp.clear()
        return False

    def detectNegativeDiagonalAcrossGrids(self):
        '''
        works
        '''
        points = []
        for i in range(self.numGrids):
            points.append(self.boards[self.numGrids - (1 + i)].board[i][(self.numGrids - 1) - i])

        if None not in points and len(set(points)) == 1:
            return True
        else:
            return False

    def checkWin(self):
        if (self.detectHorizontalOnGrid() or 
            self.detectPositiveHorizontalAcrossGrids() or 
            self.detectNegativeHorizontalAcrossGrids() or
            self.detectVerticalOnGrid() or 
            self.detectVerticalAcrossGrids() or 
            self.detectPositiveDiagonalonGrid() or 
            self.detectPositiveDiagonalAcrossGrids() or 
            self.detectNegativeDiagonalonGrid() or
            self.detectNegativeDiagonalAcrossGrids()):
            return True
        return False