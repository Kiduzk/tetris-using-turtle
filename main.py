import turtle
from turtle import Turtle, Screen
from block import Block
from blockGenerator import *
from time import time

win = Screen()
t = Turtle()


cellWidth = 30

# t.speed(0)
t.hideturtle()
turtle.tracer(0, 0)

pieceColors = {
    "O": "yellow",
    "L": "orange",
    "J": "blue",
    "I": "cyan",
    "S": "green",
    "Z": "red",
    "T": "purple"
}
pieceEdgeColor = "black"
pieceEdgeThickness = 3

grid = [[0 for x in range(10)] for y in range(20)]
blockGenerator = BlockGenerator(cellWidth / 2, cellWidth * 7.5, cellWidth, pieceColors, pieceEdgeColor, pieceEdgeThickness)
activeblock = blockGenerator.randomBlock()

gravitySpeed = 1

def move(turtle, x, y):
    turtle.up()
    turtle.goto(x, y)
    turtle.down()

def drawGrid(gridColor, edgeColor, gridThickness, edgeThickness):
    t.pencolor(gridColor)
    t.pensize(gridThickness)
    # X
    t.setheading(90)
    for i in range(-5, 6):
        if i == -5 or i == 5:
            t.pencolor(edgeColor)
            t.pensize(edgeThickness)

        move(t, i * cellWidth,  - cellWidth * 10)
        t.fd(cellWidth * 20)

        if i == -5 or i == 5:
            t.pencolor(gridColor)
            t.pensize(gridThickness)
    
    # Y
    t.setheading(0)
    for i in range(-10, 11):
        if i == -10 or i == 10:
            t.pencolor(edgeColor)
            t.pensize(edgeThickness)

        move(t, -cellWidth * 5, i * cellWidth)
        t.fd(cellWidth * 10)

        if i == -10 or i  == 10:
            t.pencolor(gridColor)
            t.pensize(gridThickness)

def addToGrid(block, grid):
    for block in block.blocks:
        gridX, gridY = (block.xcor() + 4.5 * cellWidth) / cellWidth, (block.ycor() + 9.5 * cellWidth) / cellWidth
        grid[int(gridY)][int(gridX)] = block
    
    for row in range(19, -1, -1):
        if canClearLine(row):
            for block in grid[row]:
                block.reset()
                block.hideturtle()
                del block

            del grid[row]
            grid.append([0 for i in range(10)])
            for line in grid[row:]:
                for block in line:
                    if block != 0:
                        move(block, block.xcor(), block.ycor() - cellWidth)

def isPossibleMove(direction, block, grid):
    for block in block.blocks:
        gridX, gridY = (block.xcor() + 4.5 * cellWidth) / cellWidth, (block.ycor() + 9.5 * cellWidth) / cellWidth
        gridX = int(gridX)
        gridY = int(gridY)

        if direction == "down":
            gridY -= 1
        elif direction == "left":
            gridX -= 1
        elif direction == "right":
            gridX += 1

        if gridX < 0 or gridX > 9 or gridY > 19 or gridY < 0:
            return False
        
        if grid[gridY][gridX] != 0:
            return False
    
    return True

def moveLeft():
    if isPossibleMove("left", activeblock, grid):
        activeblock.moveLeft()

def moveRight():
    if isPossibleMove("right", activeblock, grid):
        activeblock.moveRight()

def rotateLeft():
    activeblock.rotateLeft()
    while not isPossibleMove(None, activeblock, grid):
        activeblock.moveUp()

def canClearLine(lineIndex):
    for i in range(10):
        if grid[lineIndex][i] == 0:
            return False
    return True

prevTime = time()

def softDrop():
    global prevTime
    prevTime -= gravitySpeed / 1.5

def hardDrop():
    global activeblock
    while isPossibleMove("down", activeblock, grid):
        activeblock.moveDown()
    
    addToGrid(activeblock, grid)
    activeblock.makeInactive()
    activeblock = blockGenerator.randomBlock()

def generateGhostPiece(parentBlock, ghostPiece=None, fillcolor="pink", edgeColor="black", edgeThickness="3"):
    if ghostPiece != None:
        ghostPiece.hideBlock()
        del ghostPiece

    ghostBlocks = []
    for block in parentBlock.blocks:
        ghostBlocks.append(block.clone())
    
    for block in ghostBlocks:
        block.fillcolor(fillcolor)
    
    for block in ghostBlocks:
        block.pencolor(edgeColor)
    
    ghostPiece = Block(parentBlock.x, parentBlock.y, cellWidth, fillcolor, edgeColor, edgeThickness, 0, 0, blocks=ghostBlocks)

    while isPossibleMove("down", ghostPiece, grid):
        ghostPiece.moveDown()
    
    return ghostPiece

ghostPiece = generateGhostPiece(activeblock)   
def main():
    global activeblock, prevTime, ghostPiece
    
    win.listen()
    drawGrid("grey", "black", 1, 5)

    while True:
        win.onkeypress(moveLeft, "Left")
        win.onkeypress(moveRight, "Right")
        win.onkeypress(rotateLeft, "Up")
        win.onkeypress(softDrop, "Down")
        win.onkeypress(hardDrop, "space")

        ghostPiece = generateGhostPiece(activeblock, ghostPiece)

        if time() - prevTime > gravitySpeed:
            if activeblock.isInBoundary():
                # checking for block-block collision
                if not isPossibleMove("down", activeblock, grid):
                    addToGrid(activeblock, grid)
                    activeblock.makeInactive()
                    activeblock = blockGenerator.randomBlock()
                    ghostPiece = generateGhostPiece(activeblock, ghostPiece)
                    
                activeblock.moveDown()
            else:
                # adding inactive block to grid
                addToGrid(activeblock, grid)
                activeblock.makeInactive()
                activeblock = blockGenerator.randomBlock()
                ghostPiece = generateGhostPiece(activeblock, ghostPiece)
            prevTime = time()

        win.update()

main()
win.mainloop()
win.exitonclick()