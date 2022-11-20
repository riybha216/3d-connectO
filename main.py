from cmu_112_graphics import *
import random
import math
import copy

def appStarted(app):
    app.page = 0
    app.rows = 6
    app.cols = 7
    app.margin = 30
    app.currentPress = (-1, -1) # out of bounds coordinate
    app.color = "red"
    app.board = [[None for i in range(app.cols)] for j in range(app.rows)]
    app.colors = [("red", "yellow")]

def switchPlayers(app):
    if app.color == "red":
        app.color = "yellow"
    else:
        app.color = "red"

def switchPlayersAI(app):
    switchPlayers(app)
    if app.color == "yellow":
        processMinimaxOutput(app)
        print(app.color)
        app.color = "red"
        print(app.color)

def getBoard(app):
    return app.board

# getCell function inspired from
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y):
    if not(x <= app.width - app.margin and x >= app.margin and y >= 0 and
           y <= app.margin):
           return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    row = 5 - int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    (nRow, nCol) = enableStacking(app, row, col)
    return (nRow, nCol)

# recursive func bc we need to find the next empty cell to put the coin in
# and that is not necessarily app.board[row - 1][col]
def enableStacking(app, row, col):
    if row == -1:
        return (-1, -1)
    elif app.board[row][col] == None:
        return (row, col)
    else:
        return enableStacking(app, row - 1, col)

def update(app, row, col):
    app.board[row][col] = app.color

# getCellBounds function taken from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def initializeMoves():
    possibleCol = [(1, 0), (-1, 0)]
    possibleRow = [(0, 1), (0, -1)]
    possibleDiag = [(-1, 1), (1, -1), (-1, -1), (1, 1)]
    possibleMoves = possibleCol + possibleRow + possibleDiag
    return possibleMoves

def isInBounds(app, row, col):
    return row >= 0 and row <= 5 and col >= 0 and col <= 6

def checkGameEnd(app, canvas):
    possibleMoves = initializeMoves()
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col] != None:
                isWin = checkFour(app, row, col, possibleMoves, 
                        app.board[row][col])
                if isWin:
                    quitGame(app, canvas)

def checkFour(app, row, col, possibleMoves, originalPiece):
    for move in possibleMoves:
        if findIfWon(app, move, row, col, originalPiece, 1):
            return True
    return False

def findIfWon(app, move, row, col, originalPiece, count):
    if not(isInBounds(app, row, col)) or app.board[row][col] != originalPiece:
        return False
    elif count == 4 and app.board[row][col] == originalPiece:
        return True
    else:
        return findIfWon(app, move, row + move[0], col + move[1], originalPiece, 
                        count + 1)

def quitGame(app, canvas):
    gameOver(app, canvas)

def sortThroughWinningMoves(app, playerColor):
    for col in range(app.cols - 3):
        for row in range(app.rows):
            if isInBounds(app, row + 3, col) and (app.board[row][col] == 
                playerColor 
                and app.board[row+1][col] == playerColor and 
                app.board[row+2][col] == playerColor and app.board[row+3] == None):
                return True
    for col in range(app.cols):
        for row in range(app.rows - 3):
            if isInBounds(app, row, col + 3) and (app.board[row][col] == 
                playerColor 
                and app.board[row][col+1] == playerColor and 
                app.board[row][col+2] == playerColor and app.board[row][col+3] 
                == None):
                return True
    for col in range(app.cols - 3):
        for row in range(app.rows - 3):
            if isInBounds(app, row + 3, col + 3) and (app.board[row][col] 
                == playerColor 
                and app.board[row+1][col+1] == playerColor and 
                app.board[row+2][col+2] == playerColor and 
                app.board[row+3][col+3] == None):
                return True
    for col in range(app.cols - 3):
        for row in range(3, app.rows):
            if isInBounds(app, row - 3, col + 3) and (app.board[row][col] 
                == playerColor 
                and app.board[row-1][col+1] == playerColor and 
                app.board[row-2][col+2] == playerColor and 
                app.board[row-3][col+3] == None):
                return True

def noValidLocationsLeft(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col] == None:
                return False

    return True

def isTerminal(app):
    return (sortThroughWinningMoves(app, "red") or 
            sortThroughWinningMoves(app, "yellow")
            or noValidLocationsLeft(app))

def findOpenLoc(app):
    validSpots = list()
    for r in range(app.rows):
        for c in range(app.cols):
            if app.board[r][c] == None:
                validSpots.append(c)
    return validSpots

def getLists(app):
    currScore = 0

    for row in range(len(app.board)):
        lis = [i for i in app.board[row:]]
        for col in range(3):
            subset = lis[col:col + 4]
            currScore += getScores(subset)
    
    for col in range(len(app.board)):
        lis = [i for i in app.board[:col]]
        for row in range(3):
            subset = lis[row:row + 4]
            currScore += getScores(subset)

    for row in range(len(app.board) - 3):
        for col in range(len(app.board[0]) - 3):
            lis = [app.board[row][col] for i in range(4)]
            currScore += getScores(subset)

    for row in range(len(app.board) - 3):
        for col in range(len(app.board[0]) - 3):
            lis = [app.board[row + 3 - i][col] for i in range(4)]
            currScore += getScores(subset)

    return currScore

def getScores(subset):
    currScore = 0

    ai = "yellow"
    human = "red"

    if subset.count(ai) == 4:
        currScore += 200
    elif subset.count(ai) == 3 and subset.count(None) == 1:
        currScore += 10
    elif subset.count(ai) == 2 and subset.count(None) == 2:
        currScore += 3

    elif subset.count(human) == 3 and subset.count(None) == 1:
        currScore -= 9

    return currScore

# algorithm idea from
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-
# set-4-alpha-beta-pruning/,
# https://www.mygreatlearning.com/blog/alpha-beta-pruning-in-ai/, and
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduc
# tion/#:~:text=Minimax%20is%20a%20kind%20of,%2C%20Mancala%2C%20Chess%2C%20etc.

def minimax(app, board, depth, optimization, alpha, beta):
    locs = findOpenLoc(app)
    if isTerminal(app):
        if sortThroughWinningMoves(app, "yellow"):
            return (None, 10**6)
        elif sortThroughWinningMoves(app, "red"):
            return (None, (-1) * (10**6))
        else:
            return (None, 0)
    elif depth == 0:
        return (None, getLists(app))

    if optimization:
        best = -math.inf
        col = random.choice(locs)
        for c in locs:
            for r in range(app.rows):
                if board[r][c] == None:
                    tempBoard = copy.copy(board)
                    tempBoard[r][c] = "yellow"
                    updtdScore = minimax(app, tempBoard, depth-1, False, 
                                        alpha, beta)[1]
                    if updtdScore > best:
                        best = updtdScore
                        col = c
                    if alpha > best:
                        alpha = best
                    if alpha >= beta:
                        break
        return col, best

    else:
        best = math.inf
        col = random.choice(locs)
        for c in locs:
            for r in range(app.rows):
                if board[r][c] == None:
                    tempBoard = copy.copy(board)
                    tempBoard[r][c] = "yellow"
                    updtdScore = minimax(app, tempBoard, depth-1, True, 
                                        alpha, beta)[1]
                    if updtdScore < best:
                        best = updtdScore
                        col = c
                    if best < beta:
                        beta = best
                    if alpha >= beta:
                        break
        return col, best

def findEmptyRow(app, c):
    r = 0
    for row in range(len(app.board)):
        if app.board[row][c] == None:
            r = row
    return (r, c)

def processMinimaxOutput(app):
    board = copy.deepcopy(app.board)
    (c, best) = minimax(app, board, 5, True, -math.inf, math.inf)
    (r, c) = findEmptyRow(app, c)
    app.board[r][c] = "yellow"
    return

def pointToHumanVsHumanMode(app, x, y):
    return (app.width//2 - 140 <= x <= app.width//2 - 40 and
            app.height // 2 + app.margin <= y <= app.height//2 + 
            (2 * app.margin))

def pointToHumanVsAIMode(app, x, y):
    return (app.width//2 + 40 <= x <= app.width//2 + 140 and 
    app.height // 2 + app.margin <= y <= app.height//2 + (2 * app.margin))

def pointToExit(app, x, y):
    return (app.width // 2 - app.margin <= x <= app.width // 2 + app.margin and 
            app.height - 20 <= y <= app.height)

# while not directly accessed while writing this function,
# this mousePressed function is inspired from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def mousePressed(app, event):
    x = event.x
    y = event.y
    if app.page == 0:
        if pointToHumanVsHumanMode(app, x, y):
            app.page = 1
        elif pointToHumanVsAIMode(app, x, y):
            app.page = 2
    if app.page == 1:
        if app.currentPress != getCell(app, x, y):
                app.currentPress = getCell(app, x, y)
        else:
            app.currentPress = (-1, -1)
        (row, col) = getCell(app, x, y)
        if row != -1:
            update(app, row, col)
            switchPlayers(app)
        if pointToExit(app, x, y):
            app.page = 0
            app.board = [[None for i in range(app.cols)] for j in range(app.rows)]
    elif app.page == 2:
        if app.color == "red":
            if app.currentPress != getCell(app, x, y):
                    app.currentPress = getCell(app, x, y)
            else:
                app.currentPress = (-1, -1)
            (row, col) = getCell(app, x, y)
            if row != -1:
                update(app, row, col)
                switchPlayersAI(app)
        elif app.color == "yellow":
            pass
        if pointToExit(app, x, y):
            app.page = 0
            app.board = [[None for i in range(app.cols)] for j in range(app.rows)]

def drawHomeScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="light blue")
    canvas.create_text(app.width/2, 80, text="Welcome to 2.5D Connect4!", 
                        fill="black", font="Arial 35 bold")
    canvas.create_text(app.width/2, 110, text="Choose a mode to begin.", 
                        fill="black", font="Arial 20")
    canvas.create_rectangle(app.width//2 - 140, app.height // 2 + app.margin, 
                            app.width//2 - 40, app.height//2 + (2 * app.margin),
                            fill="white")
    canvas.create_text(app.width//2 - 90, (app.height // 2 + 1.5 * app.margin), 
                        text="Two Player", fill="black", font="Arial 13 bold")
    canvas.create_rectangle(app.width//2 + 140, app.height // 2 + app.margin, 
                            app.width//2 + 40, app.height//2 + (2 * app.margin),
                            fill="white")
    canvas.create_text(app.width//2 + 90, (app.height // 2 + 1.5 * app.margin), 
                        text="Human vs. AI", fill="black", font="Arial 13 bold")

def drawExit(app, canvas):
    canvas.create_rectangle(app.width // 2 - app.margin, app.height - 20,
                            app.width // 2 + app.margin, app.height, fill="green")

    canvas.create_text(app.width//2, app.height-10, text="Exit")

def drawHumanToHumanGame(app, canvas):
    canvas.create_rectangle(app.margin, app.margin, 
                            app.width - app.margin, app.height - app.margin,
                            fill="black")

    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if app.board[row][col] != None or app.currentPress == (row, col):
                fill = app.board[row][col]
            else:
                fill = "white"

            canvas.create_oval(x0+20, y0+10, x1-20, y1-10, fill=fill)

    drawExit(app, canvas)
    checkGameEnd(app, canvas)

def drawHumanToAIGame(app, canvas):
    canvas.create_rectangle(app.margin, app.margin, 
                            app.width - app.margin, app.height - app.margin,
                            fill="black")

    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if app.board[row][col] != None or app.currentPress == (row, col):
                fill = app.board[row][col]
            else:
                fill = "white"

            canvas.create_oval(x0+20, y0+10, x1-20, y1-10, fill=fill)

    drawExit(app, canvas)
    checkGameEnd(app, canvas)

def gameOver(app, canvas):
    canvas.create_rectangle(140, (app.height / 2) - 50,
                            460, (app.height / 2) + 50, fill="light blue")
    canvas.create_text(300, app.height/2, text=f"Game over!", fill="black", 
                      font="Arial 22 bold")

def redrawAll(app, canvas):
    if app.page == 0:
        drawHomeScreen(app, canvas)
    elif app.page == 1:
        drawHumanToHumanGame(app, canvas)
    elif app.page == 2:
        drawHumanToAIGame(app, canvas)
        pass

runApp(width=600, height=400)
