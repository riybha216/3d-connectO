"""
To meet MVP:
- [DONE] make 3d board w/ cells and adjustable by height
    - [KINDA DONE?] make it recognize where you click
- if player clicks on cell, a cube pops up on cell
- you can stack cubes (up to 4 cubes)
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
from winDetection import *
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
        self.heightMargin = self.height/30

    def getCellBounds(self, row, col):
        x0 = self.widthMargin + self.margin + ((col+row/2) * self.widthMargin)
        y0 = self.margin * (self.marginMultiplier - 1) - row*self.heightMargin
        x1, y1 = x0 + self.widthMargin/2, y0 - self.heightMargin
        x2, y2 = x1 + self.widthMargin, y1
        x3, y3 = x2 - self.widthMargin/2, y0
        return (x0, y0, x1, y1, x2, y2, x3, y3)

def appStarted(app):
    app.selection = (-1, -1)
    app.numGrids = 4
    app.boards = []
    app.marginMultiplier = 3.6

def generateBoards(app):
    firstBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier)
    secondBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier + 3)
    thirdBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier + 6)
    fourthBoard = ThreeDBoard(app.width, app.height, app.marginMultiplier + 9)
    app.boards.append(firstBoard)
    app.boards.append(secondBoard)
    app.boards.append(thirdBoard)
    app.boards.append(fourthBoard)

def pointInGrid(app, x, y):
    for board in app.boards:
        (x0, y0, x1, y1, x2, y2, x3, y3) = board.getCellBounds(0, 0)
        print(x0, x, x0+((x2-x1)*board.cols))
        print(y0, y, y0+((y0-y1)*board.rows))
        if not(x0 <= x <= x0+((x2-x1)*board.cols) and y0-((y0-y1)*board.rows) <= y <= y0):
            pass
        else:
            r = int((y - y2)*(-1)/board.heightMargin)
            c = int((x - x1)/board.widthMargin)
            board.board[r][c] = "orange"
            print(board.board)
            return (r, c)

def keyPressed(app, event):
    if event.key == 'd':
        generateBoards(app)

def mousePressed(app, event):
    print(pointInGrid(app, event.x, event.y))
    if pointInGrid(app, event.x, event.y) == None:
        print("none")
        app.selection = (-1, -1)
    else:
        (row, col) = pointInGrid(app, event.x, event.y)
        app.selection = (row, col)
        print(app.selection)

def redrawAll(app, canvas):    
    for board in app.boards:
        for row in range(board.rows):
            for col in range(board.cols):
                (x0, y0, x1, y1, x2, y2, x3, y3) = board.getCellBounds(row, col)
                fill = "orange" if (board.board[row][col] == "orange") else "darkBlue"
                canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                fill = fill, outline = "white")

runApp(width=1000, height=760)
