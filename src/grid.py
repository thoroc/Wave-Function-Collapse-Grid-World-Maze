
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
from src.tileset import Tileset
from src.cell import Cell


class Grid:
    """Class Grid."""

    _size: int
    _tileset: Tileset
    _cells: np.ndarray
    _collapsed_cells: int
    _map: np.ndarray

    def __init__(self, size: int):
        self._size = size
        self._tileset = Tileset()
        self._cells = np.ndarray(shape=(size, size), dtype=Cell)
        self._collapsed_cells = 0
        self._map = np.zeros(shape=(3 * size, 3 * size))

        for row_index in range(size):
            for column_index in range(size):
                self._cells[row_index, column_index] = Cell(
                    row=row_index, column=column_index
                )

    def draw_board(self, include_entropy=False, tiles="separate", title=""):
        """Draw board.

        Args:
            include_entropy (bool, optional): show entropy. Defaults to False.
            tiles (str, optional): show borders between tiles. Defaults to "separate".
            title (str, optional): set title. Defaults to "".
        """
        if tiles == "separate":
            counter = 1
            fig = plt.figure(figsize=(8, 8))

            if isinstance(title, str):
                fig.suptitle("tiles", fontsize=16)
            elif isinstance(title, int):
                fig.suptitle(str(title) + "%", fontsize=16)

            for row_cell in self._cells:
                for cell in row_cell:
                    cell_state = cell.state

                    ax = fig.add_subplot(self._size, self._size, counter)
                    # ax.set_title(cell_state)

                    if include_entropy:
                        plt.text(
                            0.7,
                            0.7,
                            str(cell.entropy),
                            fontsize=12, color="w"
                        )

                    plt.axis("off")
                    plt.imshow(self._tileset.tile(cell_state))

                    counter = counter + 1
            # fig.tight_layout()
            plt.show()

        elif tiles == "unite":
            plt.axis("off")
            plt.imshow(self._map)
            plt.show()

        else:
            logger.debug("error. Wrong tiles value was given!")

    def _lowest_entropy(self) -> Cell:
        """Returns the cell with the lowest entropy.

        Returns:
            Cell: the cell found
        """
        _lowest_entropy = 7
        candidate = self._cells[0, 0]

        for cell in self._cells.flat:

            if not cell.collapsed and cell.entropy < _lowest_entropy:
                candidate = cell
                _lowest_entropy = cell.entropy

        logger.debug(
            "The cell with the lowest entropy: {}", candidate)

        return candidate

    def _update_neighbours(self, collapsed_cell: Cell):
        """Update the options of the cells' neighbours.

        Args:
            cell (Cell): the cell to update
        """
        row = collapsed_cell.row
        column = collapsed_cell.column
        cell_state = collapsed_cell.state

        # update cell above
        if row > 0:
            available_options = self._tileset.connection_rules[cell_state]["UP"]
            neighbour: Cell = self._cells[row - 1, column]
            neighbour.update_options(available_options)

        # update cell below
        if row < self._size - 1:
            available_options = self._tileset.connection_rules[cell_state]["DOWN"]
            neighbour: Cell = self._cells[row + 1, column]
            neighbour.update_options(available_options)

        # update cell to the right
        if column < self._size - 1:
            available_options = self._tileset.connection_rules[cell_state]["RIGHT"]
            neighbour: Cell = self._cells[row, column + 1]
            neighbour.update_options(available_options)

        # update cell to the right
        if column > 0:
            available_options = self._tileset.connection_rules[cell_state]["LEFT"]
            neighbour: Cell = self._cells[row, column - 1]
            neighbour.update_options(available_options)

    def update(self):
        """Update grid's cells.

        Collapse one cell with the lowest entropy and changes available options
        of neighbours (makes update according to assigned state).
        """
        # Chose the cell with lowest entropy
        cell = self._lowest_entropy()
        # Collapse the cell, select one state for it
        cell.update_state(method="random")
        # Propagate entropy to neighbours, change their available options
        self._update_neighbours(cell.row, cell.column)
        self._collapsed_cells = self._collapsed_cells + 1

    def generate_map(self, draw_stages=False):
        """Generate map.

        Args:
            draw_stages (bool, optional): draw in stages. Defaults to False.

        Returns:
            np.ndarray: map array
        """
        max_number_collapsed_cells = int(self._size * self._size)
        percent_threshold = 10

        while self._collapsed_cells < max_number_collapsed_cells:
            self.update()
            percent = 100 * self._collapsed_cells / max_number_collapsed_cells

            if percent > percent_threshold or percent == 100:

                logger.debug(f"The map is generated by {percent:.1f}%")
                if draw_stages:
                    self.draw_board(include_entropy=True,
                                    title=percent_threshold)
                percent_threshold = percent_threshold + 10

        # Fill 2D array to save the whole map
        for row in range(self._size):
            for column in range(self._size):
                cell = self._cells[row][column]
                state = cell.state
                cell_2d = self._tileset.tiles[state]

                for width in range(3):
                    for height in range(3):
                        pos_x = row * 3 + width
                        pos_y = column * 3 + height
                        self._map[pos_x][pos_y] = cell_2d[width][height]

        return self._map

    def __repr__(self) -> str:
        return f"<src.grid.Grid size={self._size} cells={list(self._cells)}>"
