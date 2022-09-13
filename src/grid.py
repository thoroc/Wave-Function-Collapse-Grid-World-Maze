
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
                    state = cell.state

                    ax = fig.add_subplot(self._size, self._size, counter)
                    # ax.set_title(state)

                    if include_entropy:
                        plt.text(
                            0.7,
                            0.7,
                            str(cell.entropy),
                            fontsize=12, color="w"
                        )

                    plt.axis("off")
                    plt.imshow(self._tileset.get_tile(state))

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

    def _update_neighbours(self, collapsed_cell: Cell) -> dict:
        """Update the options of the cells' neighbours.

        Args:
            cell (Cell): the cell to update

        Return:
            dict: dict containing updated cells per direction
        """
        row = collapsed_cell.row
        column = collapsed_cell.column
        state = collapsed_cell.state
        lower_bound = 0
        upper_bound = self._size - 1

        updated_cells = {}

        # update cell to the left
        if column > lower_bound:
            neighbour = self._update_neighbouring_cell(
                row=row, column=column - 1, state=state, direction="LEFT"
            )
            updated_cells["LEFT"] = neighbour

        # update cell above
        if row > lower_bound:
            neighbour = self._update_neighbouring_cell(
                row=row - 1, column=column, state=state, direction="UP"
            )
            updated_cells["UP"] = neighbour

        # update cell to the right
        if column < upper_bound:
            neighbour = self._update_neighbouring_cell(
                row=row, column=column + 1, state=state, direction="RIGHT"
            )
            updated_cells["RIGHT"] = neighbour

        # update cell below
        if row < upper_bound:
            neighbour = self._update_neighbouring_cell(
                row=row + 1, column=column, state=state, direction="DOWN"
            )
            updated_cells["DOWN"] = neighbour

        return updated_cells

    def _update_neighbouring_cell(self, row: int, column: int, state: str, direction: str) -> Cell:
        """Update a single neighbouring cell.

        Args:
            row (int): row position of the current cell
            column (int): column position of the current cell
            state (str): state of the current cell
            direction (str): direction to find the neighbour

        Returns:
            Cell: the neighbouring cell
        """
        # logger.debug(f"Checking cell {direction.lower()}.")
        available_options = self._tileset.get_connection_rules(
            state=state, direction=direction
        )
        neighbour: Cell = self._cells[row, column]

        # logger.debug("Available Options: {}", available_options)
        neighbour.update_options(available_options)

        return neighbour

    def _update(self) -> None:
        """Update grid's cells.

        Collapse one cell with the lowest entropy and changes available options
        of neighbours (makes update according to assigned state).
        """
        # Chose the cell with lowest entropy
        cell = self._lowest_entropy()
        # Collapse the cell, select one state for it
        cell.update_state(method="random")
        # Propagate entropy to neighbours, change their available options
        self._update_neighbours(cell)
        self._collapsed_cells = self._collapsed_cells + 1

    def _populate_map(self) -> np.ndarray:
        map = np.ndarray(shape=(3 * self._size, 3 * self._size))

        for cell in self._cells.flat:
            cell: Cell = self._cells[cell.row][cell.column]
            cell_2d = self._tileset.get_tile(cell.state)

            for width in range(3):
                for height in range(3):
                    pos_x = cell.row * 3 + width
                    pos_y = cell.column * 3 + height
                    map[pos_x][pos_y] = cell_2d[width][height]

        return map

    def generate_map(self, draw_stages=False) -> np.ndarray:
        """Generate map.

        Args:
            draw_stages (bool, optional): draw in stages. Defaults to False.

        Returns:
            np.ndarray: map array
        """
        max_number_collapsed_cells = int(self._size * self._size)
        percent_threshold = 10

        while self._collapsed_cells < max_number_collapsed_cells:
            self._update()
            percent = 100 * self._collapsed_cells / max_number_collapsed_cells

            if percent > percent_threshold or percent == 100:

                logger.debug(f"The map is generated by {percent:.1f}%")
                if draw_stages:
                    self.draw_board(
                        include_entropy=True,
                        title=percent_threshold
                    )
                percent_threshold = percent_threshold + 10

        # Fill 2D array to save the whole map
        self._map = self._populate_map()

        return self._map

    def __repr__(self) -> str:
        return f"<src.grid.Grid size={self._size} cells={list(self._cells)}>"
