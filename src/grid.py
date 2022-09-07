import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
from src.tileset import Tileset
from src.cell import Cell


class Grid:
    """Class Grid."""

    def __init__(self, size: int):
        self._size = size
        self._tiles = Tileset()
        self._cells = np.ndarray(shape=(size, size), dtype=Cell)
        self._collapsed_cells = 0
        self._map = np.zeros(shape=(3 * size, 3 * size))

        for row in range(size):
            for column in range(size):
                self._cells[row][column] = Cell()

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
                    plt.imshow(self._tiles.tile(cell_state))

                    counter = counter + 1
            # fig.tight_layout()
            plt.show()

        elif tiles == "unite":
            plt.axis("off")
            plt.imshow(self._map)
            plt.show()

        else:
            logger.debug("error. Wrong tiles value was given!")

    def lowest_entropy(self) -> Cell:
        """Returns the cell with the lowest entropy.

        Returns:
            Cell: the cell found
        """
        lowest_entropy = 7
        lowest_entropy_index = [0, 0]
        # previousCellCollapse = self._cells[0][0].isCollapsed()

        for row in range(self._size):
            for column in range(self._size):
                cell: Cell = self._cells[row][column]
                if not cell.collapsed and cell.entropy < lowest_entropy:
                    lowest_entropy = cell.entropy
                    lowest_entropy_index = [row, column]

        logger.debug("Cell with lowest entropy: {}", lowest_entropy_index)
        logger.debug("Is the cell collapsed? {}",
                     self._cells[lowest_entropy_index[0]][lowest_entropy_index[1]].collapsed)
        return lowest_entropy_index

    def update_cell_options(self, cell_index: tuple, available_options: list):
        """Update cell's options.

        Args:
            cell_index (tuple): index where to find the cell
            available_options (list): new list of options for the cell

        Return:
            None
        """
        row, column = cell_index
        current_cell: Cell = self._cells[row][column]
        logger.debug("Available options: {}", available_options)
        logger.debug("My options: {}", current_cell.options)

        if current_cell.collapsed:
            logger.debug("This cell is already collapsed")
            return

        copy_options = current_cell.options.copy()
        for option in copy_options:
            if option in available_options:
                continue

            logger.debug("I deleted an option: {}", option)
            current_cell.options.remove(option)

        logger.debug("Cell [{}][{}]. My new options: {}",
                     row, column, current_cell.options)

    def update_options_of_others(self, cell_index: tuple):
        """Update the other cells' options.

        Args:
            cell_index (tuple): index where to find the cell of which neighbours
                                should be updated
        """
        row, column = cell_index
        collapsed_cell: Cell = self._cells[row][column]
        cell_state = collapsed_cell.state

        # update cell above
        if row > 0:
            available_options = self._tiles.connection_rules[cell_state]["UP"]
            self.update_cell_options([row - 1, column], available_options)

        # update cell below
        if row < self._size - 1:
            available_options = self._tiles.connection_rules[cell_state]["DOWN"]
            self.update_cell_options([row + 1, column], available_options)

        # update cell to the right
        if column < self._size - 1:
            available_options = self._tiles.connection_rules[cell_state]["RIGHT"]
            self.update_cell_options([row, column + 1], available_options)

        # update cell to the right
        if column > 0:
            available_options = self._tiles.connection_rules[cell_state]["LEFT"]
            self.update_cell_options([row, column - 1], available_options)

    def collapse_cell(self, cell_index: tuple):
        """Collapse cell at index.

        Args:
            cell_index (tuple): index where to find the cell
        """
        row, column = cell_index
        current_cell: Cell = self._cells[row][column]
        current_cell.update_state(method="random")

    def update(self):
        """Update grid's cells.

        Collapse one cell with the lowest entropy and changes available options
        of neighbours (makes update according to assigned state).
        """
        # Chose the cell with lowest entropy
        index = self.lowest_entropy()
        # Collapse the cell, select one state for it
        self.collapse_cell(index)
        # Propagate entropy to neighbours, change their available options
        self.update_options_of_others(index)
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
                cell_2d = self._tiles.tiles[state]

                for width in range(3):
                    for height in range(3):
                        row = row * 3 + width
                        col = column * 3 + height
                        self._map[row][col] = cell_2d[width][height]

        return self._map
