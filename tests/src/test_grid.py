import pytest
import pandas as pd
from loguru import logger

from src.grid import Grid
from src.cell import Cell
from src.tileset import Tileset


class TestGrid:
    @pytest.mark.repeat(3)
    def test_constructor(self, faker):
        # Arrange
        size = faker.random_digit_not_null()

        # Act
        grid = Grid(size=size)

        # Assert
        assert grid._size == size
        assert isinstance(grid._tileset, Tileset)

        for cell in grid._cells.flat:
            assert isinstance(cell, Cell)

        assert grid._collapsed_cells == 0

        for item in grid._map.flat:
            assert item == 0

    @pytest.mark.skip("not implemented yet.")
    def test_draw_board(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.repeat(3)
    def test__lowest_entropy_default(self, faker):
        # Arrange
        grid = Grid(size=faker.random_digit_not_null())

        # Act
        cell = grid._lowest_entropy()

        # Assert
        assert cell == grid._cells[0][0]

    @pytest.mark.repeat(3)
    def test__lowest_entropy_one_lower(self, faker):
        # Arrange
        elements = [d for d in range(0, 10)]
        row_index = faker.random_choices(elements=tuple(elements), length=1)[0]
        col_index = faker.random_choices(elements=tuple(elements), length=1)[0]

        grid = Grid(size=len(elements))
        grid._cells[row_index, col_index] = Cell(options=["Tile_0"])

        # Act
        cell = grid._lowest_entropy()

        # Assert
        assert cell == grid._cells[row_index, col_index]

    @pytest.mark.skip("not implemented yet.")
    def test__update_cell_options_cell(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.skip("not implemented yet.")
    def test__update_neighbours_cell_collapsed(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.skip("not implemented yet.")
    def test__update_neighbours(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.skip("not implemented yet.")
    def test_update(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.skip("not implemented yet.")
    def test_generate_map(self):
        # Arrange

        # Act

        # Assert
        assert False

    def print_grid(self, grid: Grid):
        """Debug statement to check entropy for the whole cells group.
        """
        entropies = []

        for column_index in range(grid._size):
            row = []

            for row_index in range(grid._size):
                curr_cell: Cell = grid._cells[row_index, column_index]
                row.append(curr_cell.entropy)

            entropies.append(row)

        columns = [f"col_{i}" for i in range(grid._size)]
        index = [[f"row_{i}" for i in range(grid._size)]]
        df = pd.DataFrame(entropies, columns=columns, index=index)

        logger.debug("\n{}", df)
