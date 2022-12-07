from cmu_112_graphics import *
import copy


class ThreeDBoard:
    def __init__(self, width, height, rows, cols, marginMultiplier):
        '''
        Initializes board variables for ThreeDBoard objects.

        Params:
        -width: positive integer denoting width of board
        -height: positive integer denoting height of board
        -rows: positive integer denoting total num of rows on board
        -cols: positive integer denoting total num of columns on board
        -marginMultiplier: natural number denoting margin between subsequent 
        boards drawn
        '''
        self.rows = rows
        self.cols = cols
        self.margin = 60
        self.width = width
        self.height = height
        self.marginMultiplier = marginMultiplier
        self.board = [[None for i in range(self.cols)] 
                       for j in range(self.rows)]
        self.widthMargin = self.width/10
        self.heightMargin = self.height/40
        self.currRow = None
        self.currCol = None

    # inspired from (but not copied from) 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    def getCellBounds(self, row, col):
        '''
        Calculates cell bounds using (x, y) coordinates 
        for each cell on the board.

        Each cell on the board is modeled as a parallelogram.
        
        Params:
        -row: a positive integer denoting current row on the board
        -col: a positive integer denoting current column on the board
        '''
        x0 = self.widthMargin + self.margin + ((col+row/2) * self.widthMargin)
        y0 = self.margin * (self.marginMultiplier - 1) - row*self.heightMargin
        x1, y1 = x0 + self.widthMargin/2, y0 - self.heightMargin
        x2, y2 = x1 + self.widthMargin, y1
        x3, y3 = x2 - self.widthMargin/2, y0
        return (x0, y0, x1, y1, x2, y2, x3, y3)


class CreateCube:
    def __init__(self, bottomFaceVertices):
        '''
        Initializes variables for CreateCube objects.

        Params:
        -bottomFaceVertices: a list of floats [x0, y0, x1, y1, x2, y2, x3, y3]
        storing points of the bottom face of the cube
        '''
        self.bottomFaceVertices = bottomFaceVertices
        self.points = []
        self.height = 30

    def getAllPoints(self):
        '''
        Returns a 2D list with [[bottomFaceVertices], [topFaceVertices]] for
        each cube generated, and calculates topFaceVertices given the
        bottomFaceVertices.
        '''
        topFaceVertices = copy.copy(self.bottomFaceVertices)
        self.points.append(self.bottomFaceVertices)

        # creates top face points by decreasing the y-coordinate by a fixed 
        # height of the cube
        for idx in range(len(topFaceVertices)):
            if idx % 2 == 1:
                topFaceVertices[idx] -= self.height
        self.points.append(topFaceVertices)
        return self.points


class CreateGridForMap:
    def __init__(self, width, height, rows, cols, startX, startY):
        '''
        Initializes variables for CreateGridForMap objects.
        '''
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.margin = 5
        self.startX = startX
        self.startY = startY

    # inspired from (but not copied from) 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    def getCellBounds(self, row, col):
        '''
        Calculates and returns bounds of each grid square of the 2D map in the
        form (x0, y0, x1, y1).

        Params:
        -row: positive integer denoting current row on grid
        -col: positive integer denoting current column on grid
        '''
        gridWidth  = self.width - 2*self.margin
        gridHeight = self.height - 2*self.margin
        cellWidth = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        x0 = self.startX + col * cellWidth
        x1 = self.startX + (col+1) * cellWidth
        y0 = self.startY + row * cellHeight
        y1 = self.startY + (row+1) * cellHeight
        return (x0, y0, x1, y1)
