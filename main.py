from Grid import *
import numpy as np
import matplotlib.pyplot as plt

Game = Grid(15)
Map = Game.GenerateMap()

plt.title("Generated and Exported Map")
plt.imshow(Map)
plt.show()
