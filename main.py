'''
Primary Functions and param descriptions:
About the Game (ConnectO): 
'''

from cmu_112_graphics import *
from createObjects import *
from detectWin import *
import random

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

# switches the color of the player
def switchPlayers(app):
    if app.players.index(app.currPlayer) == 0:
        app.currPlayer = app.players[1]
    else:
        app.currPlayer = app.players[0]

# generates boards at the appropriate height for each specific level
def generateBoards(app, num):
    for i in range(num + 1):
        if num <= 3:
            app.boards.append(ThreeDBoard(app.width+150, app.height, num, num, app.marginMultiplier + (2 * i)))
        elif num == 4:
            app.boards.append(ThreeDBoard(app.width, app.height, num, num, app.marginMultiplier + (2 * i)))
        elif num == 5:
            app.boards.append(ThreeDBoard(app.width-100, app.height, num, num, app.marginMultiplier + (1.7 * i)))

# checks if the user has clicked the appropriate point on the grid, and if
# the click itself is on the grid
def pointInGrid(app, x, y):
    firstBoardPointsList = []
    counter = 0
    board = app.boards[0]
    for i in range(len(app.boards) - 1):
        firstBoardPointsList.append(board.getCellBounds(i, 0))
    for points in firstBoardPointsList:
        (x0, y0, x1, y1, x2, y2, x3, y3) = points
        print(x, y)
        if not(x0 <= x <= x0+((x2-x1)*board.cols) and y1 <= y <= y0):
            pass
        else:
            r = counter
            c = int((x - x0)/board.widthMargin)
            board.board[r][c] = "orange"
            return (r, c)
        counter += 1

def pointInLastGrid(app, x, y):
    lastBoardPointsList = []
    counter = 0
    lastBoard = app.boards[-1]

    for i in range(4):
        lastBoardPointsList.append(lastBoard.getCellBounds(i, 0))

    for points in lastBoardPointsList:
        (x0, y0, x1, y1, x2, y2, x3, y3) = points
        if not(x0 <= x <= x0+((x2-x1)*lastBoard.cols) and y1 <= y <= y0):
            pass
        else:
            r = counter
            c = int((x - x0)/lastBoard.widthMargin)
            lastBoard.board[r][c] = None
            return (r, c)
        counter += 1

# finds points that have already been clicked so cubes cannot be placed on
# those points again
def getClickedPoints(app):
    pointList = []
    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                if board.board[row][col] != None:
                    pointList.append(board.getCellBounds(row, col))

# checks which point on the topmost grid has been clicked
def checkForOrange(app):
    firstBoard = app.boards[0]
    row, col = app.selection[0], app.selection[1]
    if firstBoard.board[row][col] == "orange":
        (x0, y0, x1, y1, x2, y2, x3, y3) = firstBoard.getCellBounds(row, col)
        app.bottomFacePoints.append([x0, y0, x1, y1, x2, y2, x3, y3])
        return

def columnFull(app, x, y):
    (row, col) = pointInGrid(app, x, y)
    for board in app.boards[1:]:
        if board.board[row][col] == None:
            return False
    return True

def mousePressed(app, event):
    x, y = event.x, event.y
    print(x, y)
    if pointToHelp(app, x, y):
        app.page = 4
    if app.page == 0:
        app.boards.clear()
        if pointToLevelOne(app, x, y):
            app.page = 1
            app.numGrids = 3
            generateBoards(app, app.numGrids)
        elif pointToLevelTwo(app, x, y):
            app.page = 2
            app.numGrids = 4
            generateBoards(app, app.numGrids)
        elif pointToLevelThree(app, x, y):
            app.page = 3
            app.numGrids = 5
            generateBoards(app, app.numGrids)
    elif app.page in {1, 2, 3}:
        win = WinDetection(app.boards[1:], app.numGrids)
        currSelection = app.selection
        if pointToExit(app, x, y):
            app.page = 0
        app.bottomFacePoints.clear()
        if pointInLastGrid(app, x, y) != None:
            (row, col) = pointInLastGrid(app, x, y)
            switchPlayers(app)
        if pointInGrid(app, event.x, event.y) == None:
            app.selection = (-1, -1)
        elif columnFull(app, x, y):
            return
        elif win.checkWin():
            return
        else:
            (row, col) = pointInGrid(app, event.x, event.y)
            if (row, col) == currSelection:
                app.selection = (-1, -1)
            else:
                print(row, col)
                app.selection = (row, col)
                checkForOrange(app)
    elif app.page == 4:
        if pointToExit(app, x, y):
            app.page = 0

# checks if the cube has reached the appropriate (x, y) coordinates
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

    if boardToBeReached != None:
        pointsToReach = app.boards[boardToBeReached].getCellBounds(row, col)
        if app.page in {2, 3}: app.marginError = 20
        for idx in range(len(pointsToReach)):
            if idx % 2 == 1 and (app.bottomFacePoints[0][idx] - app.marginError <= 
            pointsToReach[idx] <= app.bottomFacePoints[0][idx] + app.marginError):
                app.boards[0].board[row][col] = None
                app.boards[boardToBeReached].board[row][col] = app.currPlayer
                app.bottomFacePoints.clear()
                switchPlayers(app)
                return True
        return False
    else:
        app.selection = (-1, -1)
        return "No"

def timerFired(app):
    if len(app.bottomFacePoints) == 0:
        return
    else:
        hasReached = reached(app)
        if isinstance(hasReached, bool):
            if not hasReached:
                points = app.bottomFacePoints[0]
                for idx in range(len(points)):
                    if idx % 2 == 1:
                        points[idx] += app.dy
            return
        elif isinstance(hasReached, str):
            return

# finds if the click has coordinates that are within the bounds of the buttons
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

def pointToHelp(app, x, y):
    return (20 <= x <= 100 and 20 <= y <= 40)

# draws individual pieces, screens, and boards

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

def drawMap(app, canvas):
    canvas.create_text(app.width - 55, 15, text="2D Map", font="Arial 14 bold", fill="black")
    counter = 0
    for board in app.boards[1:]:
        map = CreateGridForMap(100, app.height//8, board.rows, board.cols, app.width - 100, 7 + (80 * counter))
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1) = map.getCellBounds(board.rows - row, col)
                fill = "darkBlue" if board.board[row][col] == None else board.board[row][col]
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
        counter += 1

def drawHumanHumanGame(app, canvas):
    drawExit(app, canvas)
    drawMap(app, canvas)
    currFill, otherFill = None, None
    canvas.create_rectangle(20, 20, 100, 40, fill="black")
    canvas.create_text(60, 30, text="Help", fill="white", font="Arial 15 bold")

    if app.currPlayer == app.players[0]:
        currFill = app.currPlayer
        otherFill = "black"
    else:
        currFill = "black"
        otherFill = app.currPlayer

    canvas.create_text(app.width//2 - 100, 30, text="Player 1", font="Arial 16 bold",
                        fill = currFill)
    canvas.create_text(app.width//2 + 100, 30, text="Player 2", font="Arial 16 bold",
                        fill = otherFill)

    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1, x2, y2, x3, y3) = board.getCellBounds(row, col)
                canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                fill = "darkBlue", outline = "white")

    for i in range(len(app.boards)-1, 0, -1):
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
    canvas.create_text(app.width//2, app.height/2, text="{} wins!".format(player.capitalize()), fill="black", 
                      font="Arial 22 bold")

def drawExit(app, canvas):
    canvas.create_rectangle(app.width // 2 - app.margin, app.height - 20,
                            app.width // 2 + app.margin, app.height, fill="green")

    canvas.create_text(app.width//2, app.height-10, text="Exit")

# add popping out thing to instructions
def drawHelpScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="light blue")
    canvas.create_text(app.width//2, 40, text="Game Rules", font="Arial 20 bold",
                        fill="black")
    canvas.create_text(app.width//2, 70, text="ConnectO is a two-player game.", font="Arial 18",
                        fill="black")
    canvas.create_text(app.width//2, 90, text="The goal is to be the first to place your pieces in a row, column, or diagonal.", font="Arial 18",
                        fill="black")
    canvas.create_text(app.width//2, 110, text="However, since the game is in 3D, you can align your pieces and win in 2D or 3D!", font="Arial 18",
                        fill="gray")

    canvas.create_text(app.width//2, 160, text="TO PLAY:", font="Arial 30 bold",
                        fill="black")
    canvas.create_text(app.width//2, 180, text="Click on the topmost board to generate pieces.", font="Arial 18",
                        fill="black")
    canvas.create_text(app.width//2, 200, text="Pieces will fall to their respective slots based on available space.", font="Arial 18",
                        fill="black")
    canvas.create_text(app.width//2, 220, text="The player whose turn it currently is will be highlighted at the top of the screen.", font="Arial 18",
                        fill="black")
    canvas.create_text(app.width//2, 250, text="There are three levels: easy, medium, and hard.", font="Arial 20 bold",
                        fill="black")
    canvas.create_text(app.width//2, 270, text="For easy mode, you win by connecting three pieces in any dimension.", font="Arial 18",
                        fill="black")
    canvas.create_text(app.width//2, 290, text="For medium and hard, you win by connecting four and five pieces, respectively.", font="Arial 18",
                        fill="black")
            
    canvas.create_text(app.width//2, 330, text="You can also click the green Exit screen at the bottom to go back to Home.", font="Arial 18",
                        fill="black")
    canvas.create_text(app.width//2, 360, text="Now, think carefully, and have fun! :)", font="Arial 25 bold",
                        fill="black")
    drawExit(app, canvas)

def redrawAll(app, canvas):
    if app.page == 0:
        drawHomeScreen(app, canvas)
    elif app.page in {1, 2, 3}:
        drawHumanHumanGame(app, canvas)
    elif app.page == 4:
        drawHelpScreen(app, canvas)

runApp(width=700, height=700)
