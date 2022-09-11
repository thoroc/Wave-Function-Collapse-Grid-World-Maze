import pytest
from loguru import logger

from src.grid import Grid
from src.cell import Cell


class TestGrid:
    @pytest.mark.skip("not implemented yet.")
    def test_constructor(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.skip("not implemented yet.")
    def test_draw_board(self):
        # Arrange

        # Act

        # Assert
        assert False

    def test_lowest_entropy_default(self):
        # Arrange
        grid = Grid(size=2)

        # Act
        cell = grid.lowest_entropy()
        logger.debug(grid)

        # Assert
        assert cell == grid._cells[0][0]

    @pytest.mark.repeat(3)
    def test_lowest_entropy_one_lower(self, faker):
        # Arrange
        elements = [d for d in range(0, 10)]
        row_index = faker.random_choices(elements=tuple(elements), length=1)[0]
        col_index = faker.random_choices(elements=tuple(elements), length=1)[0]

        grid = Grid(size=len(elements))
        grid._cells[row_index, col_index] = Cell(options=["Tile_0"])

        # Act
        cell = grid.lowest_entropy()

        # Assert
        assert cell == grid._cells[row_index, col_index]

    @pytest.mark.skip("not implemented yet.")
    def test_update_cell_options(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.skip("not implemented yet.")
    def test_update_options_of_others(self):
        # Arrange

        # Act

        # Assert
        assert False

    @pytest.mark.skip("not implemented yet.")
    def test_collapse_cell(self):
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
