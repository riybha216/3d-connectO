"""
To meet MVP:
- [DONE] make 3d board w/ cells
- make adjustable by height [make an input height, maybe by levels?]
---> easy, medium, hard [4, 6, 8] by height
---> connect4, 6, 8, and put a [custom] button too
- [DONE] change player (red, yellow)
- [DONE] make it recognize where you click
- [DONE] add place to click for cube and allow the cube to drop
--> [DONE] stop cube when it reaches target square
- [DONE] if player clicks on cell, a cube pops up on cell
- [DONE] represent as a 3d list
- do win detection
- highlight whos turn it is
- [DONE] do oop (maybe)

tp3 features:
- if have time: blue cube is like wild card
- if have time: add rotation
- if have time: fix minimax
- [bad idea] if have time: can claim cubes below the grid (random num of cubes)
"""

from cmu_112_graphics import *
import copy
import random

class ThreeDBoard:
    def __init__(self, width, height, rows, cols, marginMultiplier):
        self.rows = rows
        self.cols = cols
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
    def __init__(self, boards, numGrids):
        self.boards = boards
        self.numGrids = numGrids

    def detectHorizontalOnGrid(self):
        for board in self.boards:
            for row in board.board:
                if row[0] != None and len(set(row)) == 1:
                    return True
        return False

    def detectHorizontalAcrossGrids(self):
        points = []
        counter = 0
        for boardIndex in range(len(self.boards)):
            points.append(self.boards[boardIndex].board[boardIndex][counter])
            counter += 1
        if points[0] != None and len(set(points)) == 1:
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
        allCols = self.getColumns()
        for grid in allCols:
            for col in grid:
                if col[0] != None and len(set(col)) == 1:
                    return True
        return False

    def detectVerticalAcrossGrids(self):
        """row = None
        temp = []
        allCols = self.getColumns()
        for row in allCols[-1]:
            for i in row:
                if row[i] != None:
                    row = i
                else:
                    break
        for col in row:
                print(col)
                if allCols[0][row][col] != None:
                    tempSet.add([allCols[0][row][col]])
                    r, c = row, col
        for grid in range(len(allCols)):
            tempSet.add()
        if len(tempSet) == 1:
            return True
        else:
            return False"""

    def detectPositiveDiagonalonGrid(self):
        temp = []
        for board in self.boards:
            for i, row in enumerate(board.board):
                temp.append(row[i])
            if temp[0] != None and len(set(temp)) == 1: return True
        return False

    def detectPositiveDiagonalAcrossGrids(self):
        return

    def detectNegativeDiagonalonGrid(self):
        temp = []
        for board in self.boards:
            for i, row in enumerate(board.board[::-1]):
                temp.append(row[i])
            if temp[0] != None and len(set(temp)) == 1: return True
        return False

    def detectNegativeDiagonalAcrossGrids(self):
        diagonalPoints = []
        board = self.boards[0]
        if board.board[board.cols-1][0] == None:
            return False
        for board in self.boards:
            for i in range(board.rows):
                diagonalPoints.append(board)


    def checkWin(self):
        if (self.detectHorizontalOnGrid() or 
            self.detectHorizontalAcrossGrids() or 
            self.detectVerticalOnGrid() or 
            self.detectVerticalAcrossGrids() or 
            self.detectPositiveDiagonalonGrid() or 
            self.detectPositiveDiagonalAcrossGrids() or 
            self.detectNegativeDiagonalonGrid() or
            self.detectNegativeDiagonalAcrossGrids()):
            return True
        return False

def appStarted(app):
    app.selection = (-1, -1)
    app.numGrids = None
    app.boards = []
    app.marginMultiplier = 3.6
    app.players = ["red", "gold"]
    app.currPlayer = app.players[random.randint(0, 1)]
    app.bottomFacePoints = []
    app.dy = 40
    app.marginError = 5
    app.page = 0
    app.margin = 50

def switchPlayers(app):
    if app.players.index(app.currPlayer) == 0:
        app.currPlayer = app.players[1]
    else:
        app.currPlayer = app.players[0]

def generateBoards(app, num):
    for i in range(num + 1):
        if num <= 3:
            app.boards.append(ThreeDBoard(app.width+150, app.height, num, num, app.marginMultiplier + (2 * i)))
        elif num == 4:
            app.boards.append(ThreeDBoard(app.width, app.height, num, num, app.marginMultiplier + (2 * i)))
        elif num == 5:
            app.boards.append(ThreeDBoard(app.width-100, app.height, num, num, app.marginMultiplier + (1.5 * i)))

def pointInGrid(app, x, y):
    pointsList = []
    counter = 0
    board = app.boards[0]
    for i in range(4):
        pointsList.append(board.getCellBounds(i, 0))
    for points in pointsList:
        (x0, y0, x1, y1, x2, y2, x3, y3) = points
        if not(x0 <= x <= x0+((x2-x1)*board.cols) and y1 <= y <= y0):
            pass
        else:
            r = counter
            c = int((x - x0)/board.widthMargin)
            board.board[r][c] = "orange"
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

def mousePressed(app, event):
    x, y = event.x, event.y
    num = 1
    if app.page == 0:
        if pointToLevelOne(app, x, y):
            app.page = 1
            app.numGrids = 3
            generateBoards(app, app.numGrids)
        elif pointToLevelTwo(app, x, y):
            app.page = 2
            app.numGrids = 4
            generateBoards(app, app.numGrids)
            print(app.boards)
        elif pointToLevelThree(app, x, y):
            app.page = 3
            app.numGrids = 5
            generateBoards(app, app.numGrids)
    elif app.page in {1, 2, 3}:
        app.bottomFacePoints.clear()
        if pointInGrid(app, event.x, event.y) == None:
            app.selection = (-1, -1)
        else:
            (row, col) = pointInGrid(app, event.x, event.y)
            app.selection = (row, col)
            checkForOrange(app)

def reached(app):
    firstBoard = app.boards[0]
    (row, col) = (None, None)
    boardToBeReached = None
    for r in range(firstBoard.rows):
        for c in range(firstBoard.cols):
            if firstBoard.board[r][c] == "orange":
                (row, col) = (r, c)
                break
    
    possibleBoards = [i+1 for i in range(app.numGrids)]
    for boardNum in possibleBoards:
        if app.boards[boardNum].board[row][col] == None:
            boardToBeReached = boardNum

    pointsToReach = app.boards[boardToBeReached].getCellBounds(row, col)
    if app.page in {2, 3}: app.marginError = 20
    for idx in range(len(pointsToReach)):
        if idx % 2 == 1 and (app.bottomFacePoints[0][idx] - app.marginError <= 
        pointsToReach[idx] <= app.bottomFacePoints[0][idx] + app.marginError):
            app.boards[0].board[row][col] = None
            app.boards[boardToBeReached].board[row][col] = app.currPlayer
            app.bottomFacePoints.clear()
            switchPlayers(app)
            return (row, col, boardToBeReached, True)
    return (row, col, boardToBeReached, False)

def timerFired(app):
    if len(app.bottomFacePoints) == 0:
        return
    else:
        (row, col, boardToBeReached, hasReached) = reached(app)
        if not hasReached:
            points = app.bottomFacePoints[0]
            for idx in range(len(points)):
                if idx % 2 == 1:
                    points[idx] += app.dy
        return

def pointToLevelOne(app, x, y):
    return (app.width//2-80 <= x <= app.width//2+80 and
            app.height//2 - (2 * app.margin) <= y <= app.height // 2 - app.margin)

def pointToLevelTwo(app, x, y):
    return (app.width//2-80 <= x <= app.width//2+80 and
            app.height // 2 <= y <= app.height//2 + (1 * app.margin))

def pointToLevelThree(app, x, y):
    return (app.width//2-80 <= x <= app.width//2+80 and
            app.height // 2 + (2 *  app.margin) <= y <= app.height//2 + (3 * app.margin))

def pointToExit(app, x, y):
    return (app.width // 2 - app.margin <= x <= app.width // 2 + app.margin and 
            app.height - 20 <= y <= app.height)

def drawMovingCube(app, canvas):
    fill = app.currPlayer
    c = CreateCube(app.bottomFacePoints[0])
    allPoints = c.getAllPoints()
    (x0, y0, x1, y1, x2, y2, x3, y3) = allPoints[0]
    (nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3) = allPoints[1]

    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = fill, outline="white")
    canvas.create_polygon(x1, y1, nx1, ny1, nx2, ny2, x2, y2, fill = fill, outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx1, ny1, x1, y1, fill = fill, outline="white")
    canvas.create_polygon(x3, y3, nx3, ny3, nx2, ny2, x2, y2, fill = fill, outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx3, ny3, x3, y3, fill = fill, outline="white")
    canvas.create_polygon(nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3, fill = fill, outline="white")

def drawCube(app, canvas, bottomFacePoints, fill):
    c = CreateCube(bottomFacePoints)
    allPoints = c.getAllPoints()
    (x0, y0, x1, y1, x2, y2, x3, y3) = allPoints[0]
    (nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3) = allPoints[1]

    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = fill, outline="white")
    canvas.create_polygon(x1, y1, nx1, ny1, nx2, ny2, x2, y2, fill = fill, outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx1, ny1, x1, y1, fill = fill, outline="white")
    canvas.create_polygon(x3, y3, nx3, ny3, nx2, ny2, x2, y2, fill = fill, outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx3, ny3, x3, y3, fill = fill, outline="white")
    canvas.create_polygon(nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3, fill = fill, outline="white")

def drawHomeScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="SkyBlue3")
    canvas.create_text(app.width/2, 80, text="3D ConnectO", 
                        fill="black", font="Arial 60 bold")
    canvas.create_text(app.width/2, 130, text="Choose a level to begin.", 
                        fill="black", font="Arial 30")
    canvas.create_rectangle(app.width//2-80, app.height // 2 - app.margin, 
                            app.width//2+80, app.height//2 - (2 * app.margin),
                            fill="white")
    canvas.create_text(app.width//2, (app.height // 2 - 1.5 * app.margin), 
                        text="Easy", fill="black", font="Arial 25 bold")
    canvas.create_rectangle(app.width//2-80, app.height // 2 , 
                            app.width//2+80, app.height//2 + (1 * app.margin),
                            fill="white")
    canvas.create_text(app.width//2, (app.height // 2 + 0.5 * app.margin), 
                        text="Medium", fill="black", font="Arial 25 bold")
    canvas.create_rectangle(app.width//2-80, app.height // 2 + (2 * app.margin) , 
                            app.width//2+80, app.height//2 + (3 * app.margin),
                            fill="white")
    canvas.create_text(app.width//2, (app.height // 2 + 2.5 * app.margin), 
                        text="Hard", fill="black", font="Arial 25 bold")
    canvas.create_rectangle(20, 20, 100, 40, fill="white")
    canvas.create_text(60, 30, text="Help", fill="black", font="Arial 15 bold")

def drawExit(app, canvas):
    canvas.create_rectangle(app.width // 2 - app.margin, app.height - 20,
                            app.width // 2 + app.margin, app.height, fill="green")

    canvas.create_text(app.width//2, app.height-10, text="Exit")

def drawHumanHumanGame(app, canvas):
    canvas.create_rectangle(20, 20, 100, 40, fill="black")
    canvas.create_text(60, 30, text="Help", fill="white", font="Arial 15 bold")

    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1, x2, y2, x3, y3) = board.getCellBounds(row, col)
                canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                fill = "darkBlue", outline = "white")

    for i in range(1, len(app.boards)):
        for row in range(board.rows-1, -1, -1):
            for col in range(board.cols):
                if (app.boards[i].board[row][col] != None):
                    (x0, y0, x1, y1, x2, y2, x3, y3) = app.boards[i].getCellBounds(row, col)
                    pointsList = [x0, y0, x1, y1, x2, y2, x3, y3]
                    fill = app.boards[i].board[row][col]
                    drawCube(app, canvas, pointsList, fill)

    try:
        firstBoard = app.boards[0]
        for row in range(firstBoard.rows):
            for col in range(firstBoard.cols):
                if firstBoard.board[row][col] == "orange":
                        drawMovingCube(app, canvas)
    except Exception:
        pass

    if len(app.boards) > 1:
        win = WinDetection(app.boards[1:], app.numGrids)
        if win.checkWin():
            drawGameOver(app, canvas)

def drawGameOver(app, canvas):
    canvas.create_rectangle(app.width//2 - 100, (app.height / 2) - 50,
                            app.width//2 + 100, (app.height / 2) + 50, fill="light blue")
    player = "red" if app.currPlayer == "gold" else "gold"
    canvas.create_text(app.width//2, app.height/2, text="{} wins!".format(player), fill="black", 
                      font="Arial 22 bold")

def drawHelpScreen(app, canvas):
    return

def redrawAll(app, canvas):
    if app.page == 0:
        drawHomeScreen(app, canvas)
        drawHelpScreen(app, canvas)
    elif app.page in {1, 2, 3}:
        drawHumanHumanGame(app, canvas)
        drawHelpScreen(app, canvas)

runApp(width=700, height=700)
