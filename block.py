from turtle import Turtle

class Block:
    def __init__(self, x, y, cellWidth, color, edgeColor, edgeThickness, relpivotX, relpivotY, blocks=[], active=True):
        self.cellWidth = cellWidth
        self.x = x
        self.y = y
        self.active = active
        if blocks != []:
            self.blocks = blocks
        else:
            self.blocks = []
        self.edgeThickness = edgeThickness
        self.edgeColor = edgeColor
        self.color = color
        self.pivotX = self.x + relpivotX * cellWidth
        self.pivotY = self.y + relpivotY * cellWidth
    
    def move(self, block, x, y):
        block.up()
        block.goto(x, y)
        block.down()

    def addBlock(self, relativeX, relativeY):
        newBlock = Turtle()
        newBlock.hideturtle()
        newBlock.resizemode("user")
        newBlock.turtlesize(self.cellWidth / 20, self.cellWidth / 20, self.edgeThickness)
        newBlock.shape("square")
        newBlock.pencolor(self.edgeColor)
        newBlock.fillcolor(self.color)
        self.move(newBlock, self.x + relativeX * self.cellWidth, self.y + relativeY * self.cellWidth)
        self.blocks.append(newBlock)

    def isActive(self):
        return self.active
    
    def makeInactive(self):
        self.active = False
    
    def moveDown(self):
        if self.isActive():
            self.pivotY -= self.cellWidth
            for block in self.blocks:
                self.move(block, block.xcor(), block.ycor() - self.cellWidth)

    def isValidMove(self, grid):
        for block in self.blocks:
            pass

    def isInBoundary(self):
        for block in self.blocks:
            if block.ycor() + self.cellWidth * 10 - self.cellWidth // 2 == 0:
                self.active = False
                return False
        return True

    def moveRight(self):
        if self.isActive():
            self.pivotX += self.cellWidth
            for block in self.blocks:
                self.move(block, block.xcor() + self.cellWidth, block.ycor())

    def moveLeft(self):
        if self.isActive():
            self.pivotX -= self.cellWidth
            for block in self.blocks:
                self.move(block, block.xcor() - self.cellWidth, block.ycor()) 
    
    def moveUp(self):
        if self.isActive():
            self.pivotY += self.cellWidth
            for block in self.blocks:
                self.move(block, block.xcor(), block.ycor() + self.cellWidth)
        
    def rotateLeft(self):
        outRight, outLeft, outDown = 0, 0, 0 # if the block is outside of boundary after rotation
        for block in self.blocks:
            blockX, blockY = block.xcor(), block.ycor()
            newX = blockY - self.pivotY + self.pivotX
            newY = self.pivotX + self.pivotY - blockX - self.cellWidth
            if newX < -self.cellWidth * 4.5:
                outLeft += 1
            elif newX > self.cellWidth * 4.5:
                outRight += 1

            if newY < -self.cellWidth * 9.5:
                outDown += 1                  
            
            self.move(block, newX, newY)

        for _ in range(outLeft):
            self.moveRight()
        for _ in range(outRight):
            self.moveLeft()
        for _ in range(outDown):
            for block in self.blocks:
                self.move(block, block.xcor(), block.ycor() + self.cellWidth)

    def rotateRight(self):
        for block in self.blocks:
            blockX, blockY = block.xcor(), block.ycor()
            newX = self.pivotX + self.pivotY - blockY - self.cellWidth
            newY = blockX + self.pivotY - self.pivotX
            self.move(block, newX, newY)

    def unhideBlock(self):
        for block in self.blocks:
            block.showturtle()
    
    def hideBlock(self):
        for block in self.blocks:
            block.hideturtle()
    
    def redrawBlocks(self):
        newBlocks = []
        for block in self.blocks:
            newBlocks.append(block.clone())
            block.hideturtle()
            del block
        self.blocks = newBlocks
        
