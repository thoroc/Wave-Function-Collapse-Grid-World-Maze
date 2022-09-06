import matplotlib.pyplot as plt
from src.grid import Grid
from src.tileset import tileset

tileset()

Game = Grid(9)
Map = Game.GenerateMap()

plt.title("Generated and Exported Map")
plt.axis('off')
plt.imshow(Map)
plt.show()
