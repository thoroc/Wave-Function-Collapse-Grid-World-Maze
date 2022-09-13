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
        row = faker.random_choices(elements=tuple(elements), length=1)[0]
        column = faker.random_choices(elements=tuple(elements), length=1)[0]

        grid = Grid(size=len(elements))
        grid._cells[row, column] = Cell(options=["Tile_0"])

        # Act
        cell = grid._lowest_entropy()

        # Assert
        assert cell == grid._cells[row, column]

    @pytest.mark.parametrize("row, column, neibours", [
        (0, 0, 2), (0, 1, 3), (0, 2, 2),
        (1, 0, 3), (1, 1, 4), (1, 2, 3),
        (2, 0, 2), (2, 1, 3), (2, 2, 2)
    ])
    def test__update_neighbours(self, mocker, row, column, neibours):
        # Arrange
        grid = Grid(size=3)
        collapsed_cell: Cell = grid._cells[row, column]

        mocker.patch(
            "src.grid.Grid._update_neighbour",
            return_value=Cell()
        )

        # Act
        result = grid._update_neighbours(collapsed_cell=collapsed_cell)

        # Assert
        assert len(result) == neibours

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
        data = []

        for column_index in range(grid._size):
            row = []

            for row in range(grid._size):
                curr_cell: Cell = grid._cells[row, column_index]
                row.append(curr_cell.entropy)

            data.append(row)

        columns = [f"col_{i}" for i in range(grid._size)]
        index = [[f"row_{i}" for i in range(grid._size)]]
        df = pd.DataFrame(data, columns=columns, index=index)

        logger.debug("\n{}", df)
