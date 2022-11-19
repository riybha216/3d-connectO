"""
To-dos:
* Put coins in appropriate slots
* allow them to stack
* update board when coins are added
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
    app.color = "yellow"
    app.board = [None for i in range(app.cols) for j in range(app.rows)]

def getBoard(app):
    print(app.board)
    return app.board

def update(app):
    return

# getCell and getCellBounds functions adapted from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y):
    if not(x <= app.width - app.margin and x >= app.margin and y >= 0 and
           y <= app.margin):
           return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)

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

def redrawAll(app, canvas):
    canvas.create_rectangle(app.margin, app.margin, 
                            app.width - app.margin, app.height - app.margin,
                            fill="black")
    
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            fill = f"{app.color}" if (app.currentPress == (row, col)) else "white"
            canvas.create_oval(x0+20, y0+10, x1-20, y1-10, fill=fill)
            update(app)


runApp(width=600, height=400)
