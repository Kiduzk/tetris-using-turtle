import turtle
from game import Game

turtle.tracer(0, 0)
# changable variables

win = turtle.Screen()
gravitySpeed = 1
cellWidth = 30
pieceColors = {
    "O": "yellow",
    "L": "orange",
    "J": "blue",
    "I": "cyan",
    "S": "green",
    "Z": "red",
    "T": "purple"
}
# piece
pieceEdgeColor = "black"
pieceEdgeThickness = 3

# grid
gridColor = "grey"
gridBorderColor = "black"
gridThickness = 1
gridEdgeThickness = 5

# ghostpiece
ghostColor = "black" 
ghostBorderColor = "black"
ghostBorderThickness = 3

game = Game(
    win, 
    gravitySpeed, 
    cellWidth, 
    pieceColors, 
    pieceEdgeColor, 
    pieceEdgeThickness,
    gridColor, 
    gridBorderColor, 
    gridThickness, 
    gridEdgeThickness,
    ghostColor, 
    ghostBorderColor, 
    ghostBorderThickness
)
game.main()
