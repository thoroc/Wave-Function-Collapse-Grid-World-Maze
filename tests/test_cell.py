import pytest
from src.cell import Cell


class TestCell:

    def test_constructor(self):
        # Arrange
        cell = Cell()

        # Act

        # Assert
        assert cell.options == [
            "Tile_0",
            "Tile_1",
            "Tile_2",
            "Tile_3",
            "Tile_4",
            "Tile_5",
            "Tile_6",
        ]
        assert cell.collapsed is False
        assert cell.state == "Tile_10"
        assert cell.entropy == 7

    @pytest.mark.repeat(3)
    def test_state(self, faker):
        # Arrange
        cell = Cell()
        new_state = faker.word()

        # Act
        cell._state = new_state

        # Assert
        assert cell.state == new_state

    @pytest.mark.repeat(3)
    def test_entropy(self, faker):
        # Arrange
        cell = Cell()
        nb_options = faker.random_digit_not_null()

        # Act
        cell._options = [faker.word() for _ in range(nb_options)]

        # Assert
        assert cell.entropy == nb_options

    @pytest.mark.repeat(3)
    def test_collapsed(self, faker):
        # Arrange
        cell = Cell()
        is_collapsed = faker.boolean()

        # Act
        cell._collapsed = is_collapsed

        # Assert
        assert cell.collapsed == is_collapsed

    @pytest.mark.repeat(3)
    def test_options(self, faker):
        # Arrange
        cell = Cell()
        nb_options = faker.random_digit_not_null()
        new_options = [faker.word() for _ in range(nb_options)]

        # Act
        cell._options = new_options

        # Assert
        assert cell.options == new_options

    def test_update_state_default(self, mocker, tileset_tile_list):
        # Arrange
        cell = Cell()
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=tileset_tile_list
        )

        # Act
        result = cell.update_state()

        # Assert
        assert result == "Tile_0"
        assert [] == cell.options
        assert 0 == cell.entropy
        assert cell.collapsed is True

    @pytest.mark.parametrize("new_state", [
        "Tile_0",
        "Tile_1",
        "Tile_2",
        "Tile_3",
        "Tile_4",
        "Tile_5",
        "Tile_6"
    ])
    def test_update_state_collapsed(self, new_state, mocker):
        # Arrange
        cell = Cell()
        logger = mocker.patch("loguru.logger.debug")

        # Act
        cell._collapsed = True
        result = cell.update_state(new_state)

        # Assert
        assert result == "Tile_10"
        assert [
            "Tile_0",
            "Tile_1",
            "Tile_2",
            "Tile_3",
            "Tile_4",
            "Tile_5",
            "Tile_6"
        ] == cell.options
        assert 7 == cell.entropy
        assert cell.collapsed is True
        logger.assert_called()

    @pytest.mark.parametrize("random_option", [
        "Tile_0",
        "Tile_1",
        "Tile_2",
        "Tile_3",
        "Tile_4",
        "Tile_5",
        "Tile_6"
    ])
    def test_update_state_random(self, mocker, random_option, tileset_tile_list):
        # Arrange
        cell = Cell()
        choice = mocker.patch("numpy.random.choice")
        choice.return_value = random_option
        logger = mocker.patch("loguru.logger.debug")
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=tileset_tile_list
        )

        # Act
        result = cell.update_state(method="random")

        # Assert
        assert result == random_option
        assert [] == cell.options
        assert 0 == cell.entropy
        assert cell.collapsed is True
        logger.assert_called()

    @pytest.mark.parametrize("new_state", [
        "Tile_0",
        "Tile_1",
        "Tile_2",
        "Tile_3",
        "Tile_4",
        "Tile_5",
        "Tile_6"
    ])
    def test_update_state_new_state(self, new_state, mocker, tileset_tile_list):
        # Arrange
        cell = Cell()
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=tileset_tile_list
        )

        # Act
        result = cell.update_state(new_state=new_state)

        # Assert
        assert result == cell.state
        assert [] == cell.options
        assert 0 == cell.entropy
        assert cell.collapsed is True

    @pytest.mark.parametrize("state_index, new_state", [
        (0, "Tile_0"),
        (1, "Tile_1"),
        (2, "Tile_2"),
        (3, "Tile_3"),
        (4, "Tile_4"),
        (5, "Tile_5"),
        (6, "Tile_6"),
    ])
    def test_update_state_int_ok(self, state_index, new_state, mocker, tileset_tile_list):
        # Arrange
        cell = Cell()
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=tileset_tile_list
        )

        # Act
        result = cell.update_state(new_state=state_index)

        # Assert
        assert result == new_state

    @pytest.mark.parametrize("state_index", [
        -1, 7
    ])
    def test_update_state_int_out_of_bound(self, state_index, mocker, tileset_tile_list):
        # Arrange
        cell = Cell()
        logger = mocker.patch("loguru.logger.debug")
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=tileset_tile_list
        )

        # Act
        cell.update_state(new_state=state_index)

        # Assert
        logger.assert_called()
