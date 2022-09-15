import pytest
import pandas as pd
import numpy as np
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

    @pytest.mark.parametrize(
        "row, column, neighbours",
        [
            (
                0, 0,
                {"RIGHT": (0, 1), "DOWN": (1, 0)}
            ),
            (
                0, 1,
                {"LEFT": (0, 0), "RIGHT": (0, 2), "DOWN": (1, 1)}
            ),
            (
                0, 2,
                {"LEFT": (0, 1), "DOWN": (1, 2)}
            ),
            (
                1, 0,
                {"UP": (0, 0), "RIGHT": (1, 1), "DOWN": (2, 0)}
            ),
            (
                1, 1,
                {"LEFT": (1, 0), "UP": (0, 1), "RIGHT": (1, 2), "DOWN": (2, 1)}
            ),
            (
                1, 2,
                {"LEFT": (1, 1), "UP": (0, 2), "DOWN": (2, 2)}
            ),
            (
                2, 0,
                {"UP": (1, 0), "RIGHT": (2, 1)}
            ),
            (
                2, 1,
                {"LEFT": (2, 0), "UP": (1, 1), "RIGHT": (2, 2)}
            ),
            (
                2, 2,
                {"LEFT": (2, 1), "UP": (1, 2)}
            )
        ])
    def test__update_neighbours_in_range(self, row, column, neighbours):
        # Arrange
        grid = Grid(size=3)
        collapsed_cell: Cell = grid._cells[row, column]
        collapsed_cell._state = "Tile_0"
        logger.debug("Cell: {}", collapsed_cell)

        expected = {}
        for key, value in neighbours.items():
            expected[key] = grid._cells[value[0], value[1]]

        # Act
        result = grid._update_neighbours(collapsed_cell=collapsed_cell)

        logger.debug("actual:   {}", result)
        logger.debug("expected: {}", expected)

        # Assert
        assert len(result) == len(expected)
        assert result == expected

    @pytest.mark.skip("not implemented yet.")
    def test__update_neighbours_out_of_range(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.repeat(3)
    def test__update_neighbouring_cell(self, mocker, faker, directions):
        # Arrange
        elements = [d for d in range(0, 10)]
        row = faker.random_choices(elements=tuple(elements), length=1)[0]
        column = faker.random_choices(elements=tuple(elements), length=1)[0]

        grid = Grid(size=len(elements))
        available_options = [faker.word()
                             for _ in range(faker.random_digit_not_null())]

        mocker.patch(
            "src.tileset.Tileset.get_connection_rules",
            return_value=available_options
        )

        mocker.patch(
            "src.cell.Cell.update_options",
            return_value=available_options
        )
        direction = faker.random_choices(
            elements=tuple(directions), length=1)[0]
        # Act
        actual = grid._update_neighbouring_cell(
            row, column, faker.word(), direction)

        # Assert
        assert actual == grid._cells[row, column]

    @pytest.mark.repeat(3)
    def test__update(self, mocker, faker):
        # Arrange
        grid = Grid(size=3)
        collapsed_cells = faker.random_digit()
        grid._collapsed_cells = collapsed_cells

        random_cell = faker.random_choices(
            elements=tuple(grid._cells.flat), length=1)[0]

        mocker.patch(
            "src.grid.Grid._lowest_entropy",
            return_value=random_cell
        )

        mocker.patch("src.cell.Cell.update_state")
        mocker.patch("src.grid.Grid._update_neighbours")

        # Act
        grid._update()

        # Assert
        assert grid._collapsed_cells == collapsed_cells + 1

    @pytest.mark.repeat(3)
    def test__populate_map(self, mocker, faker):
        # Arrange
        size = faker.random_digit_not_null()
        grid = Grid(size=size)
        expected = np.ndarray(shape=(size * 3, size * 3), dtype=float)
        expected.fill(0.)

        mocker.patch(
            "src.tileset.Tileset.get_tile",
            return_value=[
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        )

        # Act
        map = grid._populate_map()

        # Assert
        assert (map == expected).all()

    @pytest.mark.skip("not implemented yet.")
    def test_generate_map(self):
        # Arrange

        # Act

        # Assert
        assert False

    def print_grid(self, grid: Grid, attribute: str = "entropy"):
        """Debug statement to check entropy for the whole cells group.
        """
        data = []

        for column_index in range(grid._size):
            curr_row = []

            for row_index in range(grid._size):
                curr_cell: Cell = grid._cells[row_index, column_index]
                curr_row.append(getattr(curr_cell, attribute))
                # curr_row.append(curr_cell.entropy)

            data.append(curr_row)

        columns = [f"col_{i}" for i in range(grid._size)]
        index = [[f"row_{i}" for i in range(grid._size)]]
        df = pd.DataFrame(data, columns=columns, index=index)

        logger.debug("\n{}", df)
