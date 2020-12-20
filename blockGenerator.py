from block import Block
import random

class BlockGenerator:
    def __init__(self, x, y, cellWidth, pieceColors, edgeColor, edgeThickness):
        self.x = x
        self.y = y
        self.cellWidth = cellWidth
        self.edgeColor = edgeColor
        self.edgeThickness = edgeThickness
        self.pieceColors = pieceColors
        self.currentBlocks = []
        self.resetBlocks()
    
    def resetBlocks(self):
        self.currentBlocks = [
            self.Oblock(self.pieceColors["O"]),
            self.Lblock(self.pieceColors["L"]),
            self.Iblock(self.pieceColors["I"]),
            self.Jblock(self.pieceColors["J"]),
            self.Zblock(self.pieceColors["Z"]),
            self.Sblock(self.pieceColors["S"]),
            self.Tblock(self.pieceColors["T"]),
        ]
        random.shuffle(self.currentBlocks)
    
    def getNextPiece(self):
        return self.currentBlocks[0]

    def randomBlock(self):
        if len(self.currentBlocks) > 1:
            randomBlock = self.currentBlocks[0]

            self.currentBlocks = self.currentBlocks[1:]
            randomBlock.unhideBlock()
            return randomBlock
        else:
            self.resetBlocks()
            return self.randomBlock()

    def Oblock(self, color):
        block = Block(self.x, self.y, self.cellWidth, color, self.edgeColor, self.edgeThickness, 0, 0)
        block.addBlock(0, 0)
        block.addBlock(-1, 0)
        block.addBlock(0, -1)
        block.addBlock(-1, -1)
        return block

    def Lblock(self, color):
        block = Block(self.x, self.y, self.cellWidth, color, self.edgeColor, self.edgeThickness, 0.5, 0.5)
        block.addBlock(0, 0)
        block.addBlock(-1, 0)
        block.addBlock(1, 0)
        block.addBlock(-1, -1)
        return block

    def Iblock(self, color):
        block = Block(self.x, self.y, self.cellWidth, color, self.edgeColor, self.edgeThickness, 1, 0)
        block.addBlock(0, 0)
        block.addBlock(-1, 0)
        block.addBlock(1, 0)
        block.addBlock(2, 0)
        return block

    def Tblock(self, color):
        block = Block(self.x, self.y, self.cellWidth, color, self.edgeColor, self.edgeThickness, 0.5, 0.5)
        block.addBlock(0, 0)
        block.addBlock(1, 0)
        block.addBlock(-1, 0)
        block.addBlock(0, -1)
        return block
    
    def Sblock(self, color):
        block = Block(self.x, self.y, self.cellWidth, color, self.edgeColor, self.edgeThickness, 0.5, -0.5)
        block.addBlock(1, 0)
        block.addBlock(0, 0)
        block.addBlock(-1, -1)
        block.addBlock(0, -1)
        return block
    
    def Zblock(self, color):
        block = Block(self.x, self.y, self.cellWidth, color, self.edgeColor, self.edgeThickness, 0.5, -0.5)
        block.addBlock(-1, 0)
        block.addBlock(0, 0)
        block.addBlock(1, -1)
        block.addBlock(0, -1)
        return block
    
    def Jblock(self, color):
        block = Block(self.x, self.y, self.cellWidth, color,self.edgeColor, self.edgeThickness, 0.5, 0.5)
        block.addBlock(0, 0)
        block.addBlock(-1, 0)
        block.addBlock(1, 0)
        block.addBlock(1, -1)
        return block
