"""
To-dos:
* [DONE] Put coins in appropriate slots
* [DONE] allow them to stack
* [DONE] update board when coins are added
* [DONE] solve index out of bounds error when column filled
* [DONE] switch players
* check board for win

* make home screen (2 options w/ buttons)
* human human mode should be done
* make AI minimax player on board

* do some 3D experimentation
"""

from cmu_112_graphics import *

def appStarted(app):
    app.rows = 6
    app.cols = 7
    app.margin = 30
    app.currentPress = (-1, -1) # out of bounds coordinate
    app.color = "red"
    app.board = [[None for i in range(app.cols)] for j in range(app.rows)]
    app.colors = [("red", "yellow"), ("yellow", "red")]

def switchPlayers(app):
    print(app.color)
    if app.color == "red":
        app.color = "yellow"
    else:
        app.color = "red"
    print(app.color)
    print(app.board)
    """for color in app.colors:
        if app.color == color[0]:
            app.color = color[1]
    print(app.color)"""

def getBoard(app):
    print(app.board)
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

    print(nRow, nCol)
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

# while not directly accessed while writing this function,
# this mousePressed function is inspired from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def mousePressed(app, event):
    x = event.x
    y = event.y
    if app.currentPress != getCell(app, x, y):
        app.currentPress = getCell(app, x, y)
    else:
        app.currentPress = (-1, -1)
    (row, col) = getCell(app, x, y)
    if row != -1:
        update(app, row, col)
        switchPlayers(app)

def redrawAll(app, canvas):
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


runApp(width=600, height=400)
