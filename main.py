"""
To meet MVP:
- [DONE] make 3d board w/ cells
- make adjustable by height [make an input height, maybe by levels?]
---> easy, medium, hard [4, 6, 8] by height
- [DONE] make it recognize where you click
- [DONE] add place to click for cube and allow the cube to drop
--> stop cube when it reaches target square
- [DONE] if player clicks on cell, a cube pops up on cell
- [DONE] represent as a 3d list
- do win detection
- highlight whos turn it is
- do oop (maybe)

tp3 features:
- if have time: blue cube is like wild card
- if have time: add rotation
- if have time: fix minimax
- if have time: can claim cubes below the grid (random num of cubes)
"""

from cmu_112_graphics import *
import copy
import math

class ThreeDBoard:
    def __init__(self, width, height, marginMultiplier):
        self.rows = 4
        self.cols = 4
        self.margin = 60
        self.width = width
        self.height = height
        self.marginMultiplier = marginMultiplier
        self.board = [[None for i in range(self.cols)] for j in range(self.rows)]
        self.widthMargin = self.width/10
        self.heightMargin = self.height/40
        self.currRow = None
        self.currCol = None

    def getCellBounds(self, row, col):
        self.currRow = row
        self.currCol = col
        x0 = self.widthMargin + self.margin + ((col+row/2) * self.widthMargin)
        y0 = self.margin * (self.marginMultiplier - 1) - row*self.heightMargin
        x1, y1 = x0 + self.widthMargin/2, y0 - self.heightMargin
        x2, y2 = x1 + self.widthMargin, y1
        x3, y3 = x2 - self.widthMargin/2, y0

        return (x0, y0, x1, y1, x2, y2, x3, y3)

class CreateCube:
    def __init__(self, bottomFaceVertices):
        self.bottomFaceVertices = bottomFaceVertices
        self.points = []
        self.height = 30

    def getAllPoints(self):
        topFacePoints = copy.copy(self.bottomFaceVertices)
        self.points.append(self.bottomFaceVertices)
        for idx in range(len(topFacePoints)):
            if idx % 2 == 1:
                topFacePoints[idx] -= self.height
        self.points.append(topFacePoints)
        print(self.points)
        return self.points

class WinDetection:
    def __init__(self, boards):
        self.boards = boards

    def detectHorizontalOnGrid(self):
        tempList = []
        for board in self.boards:
            for b in board.board:
                tempList.append(b)
                print(tempList)

        for row in tempList:
            for element in row:
                if element != "orange":
                    pass
            return True

    def detectVerticalOnGrid(self):
        return

    def detectVerticalAcrossGrids(self):
        return

    def detectPositiveDiagonalonGrid(self):
        return

    def detectPositiveDiagonalAcrossGrids(self):
        return

    def detectNegativeDiagonalonGrid(self):
        return

    def detectNegativeDiagonalAcrossGrids(self):
        return

    # use flatten?
    def detectStack(self):
        return

def appStarted(app):
    app.selection = (-1, -1)
    app.numGrids = 4
    app.boards = []
    app.marginMultiplier = 3.6
    app.currPlayer = None
    app.players = {"red": "yellow"}
    app.bottomFacePoints = []
    app.dy = 10

def switchPlayers(app):
    return

def generateBoards(app):
    firstBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier)
    secondBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier + 2)
    thirdBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier + 4)
    fourthBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier + 6)
    fifthBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier + 8)
    app.boards.append(firstBoard)
    app.boards.append(secondBoard)
    app.boards.append(thirdBoard)
    app.boards.append(fourthBoard)
    app.boards.append(fifthBoard)
    return firstBoard

def pointInGrid(app, x, y):
    pointsList = []
    counter = 0
    print(app.boards)
    board = app.boards[0]
    for i in range(4):
        pointsList.append(board.getCellBounds(i, 0))
    for points in pointsList:
        (x0, y0, x1, y1, x2, y2, x3, y3) = points
        print(x0, x, x0+((x2-x1)*board.cols))
        print(y1, y, y0)
        if not(x0 <= x <= x0+((x2-x1)*board.cols) and y1 <= y <= y0):
            pass
        else:
            r = counter
            c = int((x - x0)/board.widthMargin)
            board.board[r][c] = "orange"
            print(board.board)
            return (r, c)
        counter += 1

def getClickedPoints(app):
    pointList = []
    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                if board.board[row][col] != None:
                    pointList.append(board.getCellBounds(row, col))

def checkForOrange(app):
    firstBoard = app.boards[0]
    for row in range(firstBoard.rows):
        for col in range(firstBoard.cols):
            if firstBoard.board[row][col] == "orange":
                (x0, y0, x1, y1, x2, y2, x3, y3) = firstBoard.getCellBounds(row, col)
                app.bottomFacePoints.append([x0, y0, x1, y1, x2, y2, x3, y3])
                return

def keyPressed(app, event):
    # if starter screen button pressed
    if event.key == 'd':
        generateBoards(app)
        win = WinDetection(app.boards)
        print(win.detectHorizontalOnGrid())

def mousePressed(app, event):
    print(pointInGrid(app, event.x, event.y))
    app.bottomFacePoints.clear()
    if pointInGrid(app, event.x, event.y) == None:
        print("none")
        app.selection = (-1, -1)
    else:
        (row, col) = pointInGrid(app, event.x, event.y)
        app.selection = (row, col)
        checkForOrange(app)
        print(app.selection)

def reached(app):
    for board in app.boards:
        return

def timerFired(app):
    if not reached(app):
        if len(app.bottomFacePoints) == 0:
            return
        else:
            points = app.bottomFacePoints[0]
            for idx in range(len(points)):
                if idx % 2 == 1:
                    points[idx] += app.dy

def drawMovingCube(app, canvas):
    c = CreateCube(app.bottomFacePoints[0])
    allPoints = c.getAllPoints()
    (x0, y0, x1, y1, x2, y2, x3, y3) = allPoints[0]
    (nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3) = allPoints[1]

    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = "red", outline="white")
    canvas.create_polygon(x1, y1, nx1, ny1, nx2, ny2, x2, y2, fill="red", outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx1, ny1, x1, y1, fill="red", outline="white")
    canvas.create_polygon(x3, y3, nx3, ny3, nx2, ny2, x2, y2, fill="red", outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx3, ny3, x3, y3, fill="red", outline="white")
    canvas.create_polygon(nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3, fill = "red", outline="white")

def drawCube(app, canvas, bottomFacePoints):
    c = CreateCube(bottomFacePoints)
    allPoints = c.getAllPoints()
    (x0, y0, x1, y1, x2, y2, x3, y3) = allPoints[0]
    (nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3) = allPoints[1]

    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = "red", outline="white")
    canvas.create_polygon(x1, y1, nx1, ny1, nx2, ny2, x2, y2, fill="red", outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx1, ny1, x1, y1, fill="red", outline="white")
    canvas.create_polygon(x3, y3, nx3, ny3, nx2, ny2, x2, y2, fill="red", outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx3, ny3, x3, y3, fill="red", outline="white")
    canvas.create_polygon(nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3, fill = "red", outline="white")

def redrawAll(app, canvas):
    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1, x2, y2, x3, y3) = board.getCellBounds(row, col)
                canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                fill = "darkBlue", outline = "white")

    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1, x2, y2, x3, y3) = board.getCellBounds(row, col)
                pointsList = [x0, y0, x1, y1, x2, y2, x3, y3]
                if app.boards[0].board[row][col] == "orange":
                    drawMovingCube(app, canvas)
                elif ((app.boards[1].board[row][col] == "orange") or 
                    (app.boards[2].board[row][col] == "orange") or
                    (app.boards[3].board[row][col] == "orange")):
                    drawCube(app, canvas, pointsList)

runApp(width=700, height=700)
