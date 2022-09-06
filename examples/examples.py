import matplotlib.pyplot as plt
from src.grid import Grid

# Example of drawing an empty board
Game = Grid(9)
Game.DrawBoard(includeEntropy=True)

# Example of creating the full game board
Game = Grid(9)
Map = Game.GenerateMap(drawStages=True)
Game.DrawBoard(tiles="unite")

plt.title("Generated and Exported Map")
plt.imshow(Map)
plt.show()

print(Map)
