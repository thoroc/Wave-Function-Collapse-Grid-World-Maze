import matplotlib.pyplot as plt
from src.grid import Grid

# Example of drawing an empty board
grid = Grid(9)
grid.draw_board(include_entropy=True)

# Example of creating the full grid board
grid = Grid(9)
map = grid.generate_map(draw_stages=True)
grid.draw_board(tiles="unite")

plt.title("Generated and Exported map")
plt.imshow(map)
plt.show()

print(map)
