import matplotlib.pyplot as plt
from src.grid import Grid
from src.lib import tileset

# tileset()

grid = Grid(9)
map = grid.generate_map(draw_stages=True)

plt.title("Generated and Exported map")
plt.axis('off')
plt.imshow(map)
plt.show()
