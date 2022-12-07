'''
Name: Riya Bhatia
Course: 15-112 Section C
Semester: F22
'''

from cmu_112_graphics import *
from createObjects import *
from detectWin import *
import random

def appStarted(app):
    '''
    Initializes all variables needed for app.
    '''
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
    '''
    Changes player turns after the current player has completed his/her move.
    '''
    if app.players.index(app.currPlayer) == 0:
        app.currPlayer = app.players[1]
    else:
        app.currPlayer = app.players[0]

def generateBoards(app, level):
    '''
    Generates boards at the appropriate height for each level of the game.

    Params:
    -level: positive natural number denoting current level that player is
    playing, which also gives number of grids to generate as each level has
    a distinct board
    '''
    for i in range(level + 1):
        if level == 3:
            app.boards.append(ThreeDBoard(app.width+150, app.height, level,
                                        level, app.marginMultiplier + (2 * i)))
        elif level == 4:
            app.boards.append(ThreeDBoard(app.width, app.height, level, level,
                                          app.marginMultiplier + (2 * i)))
        elif level == 5:
            app.boards.append(ThreeDBoard(app.width-100, app.height, level,
                                    level, app.marginMultiplier + (1.7 * i)))

def pointInGrid(app, x, y):
    '''
    Checks if the user has clicked inside of the topmost grid to input a piece,
    and returns the row and column of the board in a tuple that the click 
    targetted.

    Params:
    -x: x-coordinate of the user's click
    -y: y-coordinate of the user's click
    '''
    firstBoardPointsList = []
    counter = 0
    board = app.boards[0]

    for i in range(len(app.boards) - 1):
        firstBoardPointsList.append(board.getCellBounds(i, 0))

    for points in firstBoardPointsList:
        (x0, y0, x1, y1, x2, y2, x3, y3) = points
        # checks if point is in the grid itself
        if not(x0 <= x <= x0+((x2-x1)*board.cols) and y1 <= y <= y0):
            pass
        else:
            r = counter
            c = int((x - x0)/board.widthMargin)
            # indicates that user has clicked on that row and column in grid
            board.board[r][c] = "orange"
            return (r, c)
        counter += 1

def pointInLastGrid(app, x, y):
    '''
    Checks if the user has clicked on the last grid to pop out a piece.
    Returns the row and column of the grid square clicked.

    Params:
    -x: x-coordinate of the user's click
    -y: y-coordinate of the user's click
    '''
    lastBoardPointsList = []
    counter = 0
    lastBoard = app.boards[-1]

    for i in range(4):
        lastBoardPointsList.append(lastBoard.getCellBounds(i, 0))

    for points in lastBoardPointsList:
        (x0, y0, x1, y1, x2, y2, x3, y3) = points
        # checks if point is in the grid itself
        if not(x0 <= x <= x0+((x2-x1)*lastBoard.cols) and y1 <= y <= y0):
            pass
        else:
            r = counter
            c = int((x - x0)/lastBoard.widthMargin)
            # indicates that user has clicked on that row and column in grid,
            # so token is popped out
            lastBoard.board[r][c] = None
            return (r, c)
        counter += 1

def getClickedPoints(app):
    '''
    Finds points that have blocks placed on them so new tokens
    cannot be placed on them.
    '''
    pointList = []
    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                if board.board[row][col] != None:
                    pointList.append(board.getCellBounds(row, col))

def checkForOrange(app):
    '''
    Checks if a point on the topmost grid has been clicked for input.
    '''
    firstBoard = app.boards[0]
    row, col = app.selection[0], app.selection[1]
    if firstBoard.board[row][col] == "orange":
        (x0, y0, x1, y1, x2, y2, x3, y3) = firstBoard.getCellBounds(row, col)
        app.bottomFacePoints.append([x0, y0, x1, y1, x2, y2, x3, y3])
        return

def columnFull(app, x, y):
    '''
    Checks if a column that the user wants to add to is already full.

    Params:
    -x: x-coordinate of the user's click
    -y: y-coordinate of the user's click
    '''
    (row, col) = pointInGrid(app, x, y)
    for board in app.boards[1:]:
        if board.board[row][col] == None:
            return False
    return True

def mousePressed(app, event):
    '''
    Ensures all mouse presses lead to their corresponding pages, and
    mouse presses within the board lead to specific functions being
    carried out.
    '''
    x, y = event.x, event.y
    if pointToHelp(x, y):
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
    # ensures specific functions are carried out if the game is being played
    elif app.page in {1, 2, 3}:
        win = WinDetection(app.boards[1:], app.numGrids)
        currSelection = app.selection
        app.bottomFacePoints.clear()
        if pointToExit(app, x, y):
            app.page = 0

        if pointInLastGrid(app, x, y) != None:
            (row, col) = pointInLastGrid(app, x, y)
            switchPlayers(app)
        elif pointInGrid(app, x, y) == None:
            app.selection = (-1, -1)
        elif columnFull(app, x, y):
            try:
                (row, col) = pointInGrid(app, x, y)
                app.boards[0].board[row][col] = None
                return
            except Exception:
                return
        elif win.checkWin():
            return
        else:
            (row, col) = pointInGrid(app, x, y)
            if (row, col) == currSelection:
                app.selection = (-1, -1)
            else:
                app.selection = (row, col)
                checkForOrange(app)
    elif app.page == 4:
        if pointToExit(app, x, y):
            app.page = 0

def reached(app):
    '''
    Returns boolean value based on whether cube has reached its intended 
    location on the board.
    '''
    firstBoard = app.boards[0]
    (row, col) = (None, None)
    boardToBeReached = None

    # checks if token has been requested to be inputted
    for r in range(firstBoard.rows):
        for c in range(firstBoard.cols):
            if firstBoard.board[r][c] == "orange":
                (row, col) = (r, c)
                break
    
    # finds next empty board to place cube on
    possibleBoards = [i+1 for i in range(app.numGrids)]
    for boardNum in possibleBoards:
        if app.boards[boardNum].board[row][col] == None:
            boardToBeReached = boardNum

    if boardToBeReached != None:
        pointsToReach = app.boards[boardToBeReached].getCellBounds(row, col)
        if app.page in {2, 3}: app.marginError = 20
        for idx in range(len(pointsToReach)):
            # ensures that cube reaches the board, even if (x, y) coordinates
            # do not match perfectly, by using a margin of error
            if idx % 2 == 1 and (app.bottomFacePoints[0][idx] - app.marginError 
            <= pointsToReach[idx] <= app.bottomFacePoints[0][idx] + 
            app.marginError):
                # resets values now that cube has reached intended grid
                app.boards[0].board[row][col] = None
                app.boards[boardToBeReached].board[row][col] = app.currPlayer
                app.bottomFacePoints.clear()
                switchPlayers(app)
                return True
        return False
    else:
        app.selection = (-1, -1)

def timerFired(app):
    '''
    Controls animation of cube as it falls to its respective board.
    '''
    if len(app.bottomFacePoints) == 0:
        return
    else:
        hasReached = reached(app)
        if isinstance(hasReached, bool):
            if not hasReached:
                points = app.bottomFacePoints[0]
                for idx in range(len(points)):
                    # subtracts app.dy from all y-coordinates only
                    if idx % 2 == 1:
                        points[idx] += app.dy
            return
        else:
            return

def pointToLevelOne(app, x, y):
    '''
    Finds if the click has coordinates that are within the bounds of the 
    level one button.

    Params:
    -x: x-coordinate of user click
    -y: y-coordinate of user click
    '''
    return (app.width//2-80 <= x <= app.width//2+80 and
            app.height//2 - (2 * app.margin) <= y <= app.height // 2 - 
            app.margin)

def pointToLevelTwo(app, x, y):
    '''
    Finds if the click has coordinates that are within the bounds of the 
    level two button.

    Params:
    -x: x-coordinate of user click
    -y: y-coordinate of user click
    '''
    return (app.width//2-80 <= x <= app.width//2+80 and
            app.height // 2 <= y <= app.height//2 + (1 * app.margin))

def pointToLevelThree(app, x, y):
    '''
    Finds if the click has coordinates that are within the bounds of the 
    level three button.

    Params:
    -x: x-coordinate of user click
    -y: y-coordinate of user click
    '''
    return (app.width//2-80 <= x <= app.width//2+80 and
            app.height // 2 + (2 *  app.margin) <= y <= app.height//2 + 
            (3 * app.margin))

def pointToExit(app, x, y):
    '''
    Finds if the click has coordinates that are within the bounds of the 
    exit button.

    Params:
    -x: x-coordinate of user click
    -y: y-coordinate of user click
    '''
    return (app.width // 2 - app.margin <= x <= app.width // 2 + app.margin and 
            app.height - 20 <= y <= app.height)

def pointToHelp(x, y):
    '''
    Finds if the click has coordinates that are within the bounds of the 
    help button.

    Params:
    -x: x-coordinate of user click
    -y: y-coordinate of user click
    '''
    return (20 <= x <= 100 and 20 <= y <= 40)

def drawMovingCube(app, canvas):
    '''
    Draws moving cube by creating six polygons for each face of the cube.
    '''
    fill = app.currPlayer
    c = CreateCube(app.bottomFacePoints[0])
    allPoints = c.getAllPoints()
    (x0, y0, x1, y1, x2, y2, x3, y3) = allPoints[0]
    (nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3) = allPoints[1]

    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = fill, 
                          outline="white")
    canvas.create_polygon(x1, y1, nx1, ny1, nx2, ny2, x2, y2, fill = fill, 
                          outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx1, ny1, x1, y1, fill = fill, 
                          outline="white")
    canvas.create_polygon(x3, y3, nx3, ny3, nx2, ny2, x2, y2, fill = fill, 
                          outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx3, ny3, x3, y3, fill = fill, 
                          outline="white")
    canvas.create_polygon(nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3, fill = fill, 
                          outline="white")

def drawCube(canvas, bottomFacePoints, fill):
    '''
    Draws stationary cube by creating six polygons for each face of the cube.

    Params:
    -bottomFacePoints: list of vertices for the bottom face of the cube
    -fill: string of the color to fill the cube
    '''
    c = CreateCube(bottomFacePoints)
    allPoints = c.getAllPoints()
    (x0, y0, x1, y1, x2, y2, x3, y3) = allPoints[0]
    (nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3) = allPoints[1]

    canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill = fill, 
                          outline="white")
    canvas.create_polygon(x1, y1, nx1, ny1, nx2, ny2, x2, y2, fill = fill, 
                          outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx1, ny1, x1, y1, fill = fill, 
                          outline="white")
    canvas.create_polygon(x3, y3, nx3, ny3, nx2, ny2, x2, y2, fill = fill, 
                          outline="white")
    canvas.create_polygon(x0, y0, nx0, ny0, nx3, ny3, x3, y3, fill = fill, 
                          outline="white")
    canvas.create_polygon(nx0, ny0, nx1, ny1, nx2, ny2, nx3, ny3, fill = fill, 
                          outline="white")

def drawHomeScreen(app, canvas):
    '''
    Draws home screen of the game.
    '''
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
    canvas.create_rectangle(app.width//2-80, app.height // 2 + (2 * app.margin), 
                            app.width//2+80, app.height//2 + (3 * app.margin),
                            fill="white")
    canvas.create_text(app.width//2, (app.height // 2 + 2.5 * app.margin), 
                        text="Hard", fill="black", font="Arial 25 bold")
    canvas.create_rectangle(20, 20, 100, 40, fill="white")
    canvas.create_text(60, 30, text="Help", fill="black", font="Arial 15 bold")

def drawExit(app, canvas):
    '''
    Draws exit button of the game.
    '''
    canvas.create_rectangle(app.width // 2 - app.margin, app.height - 20,
                            app.width // 2 + app.margin, app.height, 
                            fill="green")

    canvas.create_text(app.width//2, app.height-10, text="Exit")

def drawMap(app, canvas):
    '''
    Draws 2D map figure on top right of each screen by mapping 3D board points
    to 2D points.
    '''
    counter = 0
    canvas.create_text(app.width - 55, 15, text="2D Map", font="Arial 14 bold", 
                       fill="black")
    for board in app.boards[1:]:
        map = CreateGridForMap(100, app.height//8, board.rows, board.cols, 
                               app.width - 100, 7 + (80 * counter))
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1) = map.getCellBounds(board.rows - row, col)
                if board.board[row][col] == None: fill = "darkBlue"
                else: fill = board.board[row][col]
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
        counter += 1

def drawHumanHumanGame(app, canvas):
    '''
    Draws two-player game for each screen.
    '''
    drawExit(app, canvas)
    drawMap(app, canvas)
    currFill, otherFill = None, None
    canvas.create_rectangle(20, 20, 100, 40, fill="black")
    canvas.create_text(60, 30, text="Help", fill="white", font="Arial 15 bold")

    # sets color of top center text, and writes player name in color
    # if it's their turn
    if app.currPlayer == app.players[0]:
        currFill = app.currPlayer
        otherFill = "black"
    else:
        currFill = "black"
        otherFill = app.currPlayer

    canvas.create_text(app.width//2 - 100, 30, text="Player 1", 
                       font="Arial 16 bold", fill = currFill)
    canvas.create_text(app.width//2 + 100, 30, text="Player 2", 
                       font="Arial 16 bold", fill = otherFill)

    # draws boards first, so tokens can be placed on them
    # inspired by https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1, x2, y2, x3, y3) = board.getCellBounds(row, col)
                canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                fill = "darkBlue", outline = "white")

    # draws stationary cubes on top of board in reverse order to seem like
    # objects placed closer to user are truly closer
    # inspired by https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    for i in range(len(app.boards)-1, 0, -1):
        for row in range(board.rows-1, -1, -1):
            for col in range(board.cols):
                if (app.boards[i].board[row][col] != None):
                    (x0, y0, x1, y1, x2, y2, x3, y3) = (app.boards[i].
                                                     getCellBounds(row, col))
                    pointsList = [x0, y0, x1, y1, x2, y2, x3, y3]
                    fill = app.boards[i].board[row][col]
                    drawCube(canvas, pointsList, fill)

    # draws moving cube
    try:
        firstBoard = app.boards[0]
        for row in range(firstBoard.rows):
            for col in range(firstBoard.cols):
                if firstBoard.board[row][col] == "orange":
                        drawMovingCube(app, canvas)
    except Exception:
        pass

    # checks for win after placing moving cube
    if len(app.boards) > 1:
        win = WinDetection(app.boards[1:], app.numGrids)
        if win.checkWin():
            drawGameOver(app, canvas)

def drawGameOver(app, canvas):
    '''
    Draws game over screen for the game.
    '''
    canvas.create_rectangle(app.width//2 - 100, (app.height / 2) - 50,
                            app.width//2 + 100, (app.height / 2) + 50, 
                            fill="light blue")
    player = "red" if app.currPlayer == "gold" else "gold"
    canvas.create_text(app.width//2, app.height/2, text="{} wins!".format
                      (player.capitalize()), fill="black", 
                      font="Arial 22 bold")

def drawHelpScreen(app, canvas):
    '''
    Draws help screen for game.
    '''
    canvas.create_rectangle(0, 0, app.width, app.height, fill="light blue")
    canvas.create_text(app.width//2, 40, text="Game Rules", 
                       font="Arial 20 bold", fill="black")
    canvas.create_text(app.width//2, 70, text="ConnectO is a two-player game.", 
                       font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 90, text="The goal is to be the first to"\
                       " place your pieces in a row, column, or diagonal.", 
                       font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 110, text="However, since the game is in"\
                       " 3D, you can align your pieces and win in 2D or 3D!", 
                       font="Arial 18", fill="gray")

    canvas.create_text(app.width//2, 160, text="TO PLAY:", font="Arial 30 bold",
                        fill="black")
    canvas.create_text(app.width//2, 180, text="Click on the topmost board to"\
                       " generate pieces.", font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 200, text="Pieces will fall to their"\
                       " respective slots based on available space.", 
                       font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 220, text="The player whose turn it"\
                       " currently is will be highlighted at the top of the "\
                       "screen.", font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 250, text="There are three levels: easy,"\
                       " medium, and hard.", font="Arial 20 bold", fill="black")
    canvas.create_text(app.width//2, 270, text="For easy mode, you win by"\
                       " connecting three pieces in any dimension.", 
                       font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 290, text="For medium and hard, you win"\
                       " by connecting four and five pieces, respectively.", 
                       font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 310, text="You can also pop out pieces "\
                       " from the bottom grid only by clicking on the piece.",
                       font="Arial 18", fill="black")
            
    canvas.create_text(app.width//2, 350, text="You can also click the green"\
                       " Exit screen at the bottom to go back to Home.", 
                       font="Arial 18", fill="black")
    canvas.create_text(app.width//2, 380, text="Now, think carefully, and have"\
                       " fun! :)", font="Arial 25 bold", fill="black")
    drawExit(app, canvas)

def redrawAll(app, canvas):
    '''
    Draws screens based on page numbers.
    '''
    if app.page == 0:
        drawHomeScreen(app, canvas)
    elif app.page in {1, 2, 3}:
        drawHumanHumanGame(app, canvas)
    elif app.page == 4:
        drawHelpScreen(app, canvas)

runApp(width=700, height=700)
