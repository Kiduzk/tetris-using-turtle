from turtle import Turtle, Screen
from block import Block
from blockGenerator import *
from time import time

class Game:
    def __init__(self, screen, gravitySpeed, cellWidth, pieceColors, pieceEdgeColor, pieceEdgeThickness, gridColor, gridBorderColor, gridThickness, gridEdgeThickness, ghostColor, ghostBorderColor, ghostBorderThickness):
        self.grid = [[0 for x in range(10)] for y in range(20)]
        self.cellWidth = cellWidth
        self.blockGenerator = BlockGenerator(self.cellWidth / 2, self.cellWidth * 7.5, self.cellWidth, pieceColors, pieceEdgeColor, pieceEdgeThickness)
        self.nextBlockClone = []
        self.drawNextBlock()
        self.activeblock = self.blockGenerator.randomBlock()
        self.gravitySpeed = gravitySpeed
        self.pieceColors = pieceColors
        self.pieceEdgeColor = pieceEdgeColor
        self.pieceEdgeThickness = pieceEdgeThickness
        self.gridColor = gridColor
        self.gridBorderColor = gridBorderColor
        self.gridThickness = gridThickness
        self.gridEdgeThickness =  gridEdgeThickness
        self.ghostColor = ghostColor
        self.ghostBorderColor = ghostBorderColor
        self.ghostBorderThickness = ghostBorderThickness
        self.win = screen
        self.win.colormode(255)
        
    def move(self, turtle, x, y):
        turtle.up()
        turtle.goto(x, y)
        turtle.down()
    
    def drawRect(self, x, y, width, height, color, thickness):
        t = Turtle()
        t.pensize(thickness)
        t.hideturtle()
        self.move(t, x, y)
        for i in range(4):
            if i % 2:
                t.fd(height)
            else:
                t.fd(width)
            t.left(90)

    def drawGrid(self, x, y, width, height, gridColor, edgeColor, gridThickness, edgeThickness):
        t = Turtle()
        height *= self.cellWidth
        width *= self.cellWidth

        self.move(t, x, y)
        t.hideturtle()
        t.pencolor(gridColor)
        t.pensize(gridThickness)

        t.setheading(90)
        for i in range(x + self.cellWidth, x + width, self.cellWidth):
            self.move(t, i, y)
            t.fd(height)
        
        t.setheading(0)
        for i in range(y + self.cellWidth, y + height, self.cellWidth):
            self.move(t, x, i)
            t.fd(width)

        # drawing the borders
        self.drawRect(x, y, width, height, edgeColor, edgeThickness)
        
    def drawNextBlock(self):
        if self.nextBlockClone != []:
            for block in self.nextBlockClone:
                block.hideturtle()

        nextBlock = self.blockGenerator.getNextPiece()
        nextBlockClone = []
        for block in nextBlock.blocks:
            clone = block.clone()
            clone.showturtle()
            self.move(clone, self.cellWidth * 7 + block.xcor(), block.ycor())
            nextBlockClone.append(clone)
        
        self.nextBlockClone = nextBlockClone

    def addToGrid(self, block, grid):
        for block in block.blocks:
            gridX, gridY = (block.xcor() + 4.5 * self.cellWidth) / self.cellWidth, (block.ycor() + 9.5 * self.cellWidth) / self.cellWidth
            grid[int(gridY)][int(gridX)] = block
        
        for row in range(19, -1, -1):
            if self.canClearLine(row):
                for block in grid[row]:
                    block.reset()
                    block.hideturtle()
                    del block

                del grid[row]
                grid.append([0 for i in range(10)])
                for line in grid[row:]:
                    for block in line:
                        if block != 0:
                            self.move(block, block.xcor(), block.ycor() - self.cellWidth)

    def isPossibleMove(self, direction, block, grid):
        for block in block.blocks:
            gridX, gridY = (block.xcor() + 4.5 * self.cellWidth) / self.cellWidth, (block.ycor() + 9.5 * self.cellWidth) / self.cellWidth
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

    def moveLeft(self):
        if self.isPossibleMove("left", self.activeblock, self.grid):
            self.activeblock.moveLeft()

    def moveRight(self):
        if self.isPossibleMove("right", self.activeblock, self.grid):
            self.activeblock.moveRight()

    def rotateLeft(self, ):
        self.activeblock.rotateLeft()
        while not self.isPossibleMove(None, self.activeblock, self.grid):
            self.activeblock.moveUp()

    def canClearLine(self, lineIndex):
        for i in range(10):
            if self.grid[lineIndex][i] == 0:
                return False
        return True

    def softDrop(self):
        self.prevTime -= self.gravitySpeed / 1.5

    def hardDrop(self):
        while self.isPossibleMove("down", self.activeblock, self.grid):
            self.activeblock.moveDown()
        
        self.addToGrid(self.activeblock, self.grid)
        self.activeblock.makeInactive()
        self.activeblock = self.blockGenerator.randomBlock()
        self.drawNextBlock()

    def generateGhostPiece(self, parentBlock, ghostPiece=None):
        if ghostPiece != None:
            ghostPiece.hideBlock()
            del ghostPiece

        ghostBlocks = []
        fillcolor = self.ghostColor
        edgeColor = self.ghostBorderColor
        edgeThickness = self.ghostBorderThickness

        for block in parentBlock.blocks:
            ghostBlocks.append(block.clone())
        
        for block in ghostBlocks:
            block.fillcolor(fillcolor)
            block.pencolor(edgeColor)
            block.turtlesize(self.cellWidth / 20, self.cellWidth / 20, edgeThickness)
        
        ghostPiece = Block(parentBlock.x, parentBlock.y, self.cellWidth, fillcolor, edgeColor, edgeThickness, 0, 0, blocks=ghostBlocks)

        while self.isPossibleMove("down", ghostPiece, self.grid):
            ghostPiece.moveDown()
        parentBlock.redrawBlocks()
 
        return ghostPiece

    def main(self):
        ghostPiece = self.generateGhostPiece(self.activeblock)
        self.win.listen()
        gridX = self.cellWidth * -5
        gridY = self.cellWidth * -10
        gridWidth, gridHeight = 10, 20
        self.drawGrid(gridX, gridY, gridWidth, gridHeight, self.gridColor, self.gridBorderColor, self.gridThickness, self.gridEdgeThickness)
        self.drawGrid(gridX + gridWidth * self.cellWidth + self.cellWidth, gridY + gridHeight * self.cellWidth - self.cellWidth * 4, 4, 4, self.gridColor, self.gridBorderColor, self.gridThickness, self.gridEdgeThickness)
        self.prevTime = time()

        while True:
            self.win.onkeypress(self.moveLeft, "Left")
            self.win.onkeypress(self.moveRight, "Right")
            self.win.onkeypress(self.rotateLeft, "Up")
            self.win.onkeypress(self.softDrop, "Down")
            self.win.onkeypress(self.hardDrop, "space")

            ghostPiece = self.generateGhostPiece(self.activeblock, ghostPiece)

            if time() - self.prevTime > self.gravitySpeed:
                if self.activeblock.isInBoundary():
                    # checking for block-block collision
                    if not self.isPossibleMove("down", self.activeblock, self.grid):
                        self.addToGrid(self.activeblock, self.grid)
                        self.activeblock.makeInactive()
                        self.activeblock = self.blockGenerator.randomBlock()
                        self.drawNextBlock()
                        ghostPiece = self.generateGhostPiece(self.activeblock, ghostPiece)
                        
                        
                    self.activeblock.moveDown()
                else:
                    # adding inactive block to grid
                    self.addToGrid(self.activeblock, self.grid)
                    self.activeblock.makeInactive()
                    self.activeblock = self.blockGenerator.randomBlock()
                    self.drawNextBlock()
                    ghostPiece = self.generateGhostPiece(self.activeblock, ghostPiece)
                    
                self.prevTime = time()

            self.activeblock.redrawBlocks()
            self.win.update()

        self.win.mainloop()
        self.win.exitonclick()