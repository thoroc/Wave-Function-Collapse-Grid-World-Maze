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
        expected_state = faker.word()

        # Act
        cell._state = expected_state

        # Assert
        assert cell.state == expected_state

    @pytest.mark.repeat(3)
    def test_entropy(self, faker):
        # Arrange
        nb_options = faker.random_digit_not_null()
        options = [faker.word() for _ in range(nb_options)]

        # Act
        cell = Cell(options=options)

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
        nb_options = faker.random_digit_not_null()
        expected = [faker.word() for _ in range(nb_options)]

        # Act
        cell = Cell(options=expected)

        # Assert
        assert cell.options == expected

    @pytest.mark.repeat(3)
    def test_row(self, faker):
        # Arrange
        row_index = faker.random_digit()

        # Act
        cell = Cell(row=row_index)

        # Assert
        assert cell.row == row_index
        assert cell.column is None

    @pytest.mark.repeat(3)
    def test_column(self, faker):
        # Arrange
        column_index = faker.random_digit()

        # Act
        cell = Cell(column=column_index)

        # Assert
        assert cell.row is None
        assert cell.column == column_index

    def test_update_state_default(self, mocker, complete_tile_list):
        # Arrange
        cell = Cell()
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=complete_tile_list
        )

        # Act
        actual = cell.update_state()

        # Assert
        assert actual == "Tile_0"
        assert [] == cell.options
        assert 0 == cell.entropy
        assert cell.collapsed is True

    @pytest.mark.parametrize("expected_state", [
        "Tile_0",
        "Tile_1",
        "Tile_2",
        "Tile_3",
        "Tile_4",
        "Tile_5",
        "Tile_6"
    ])
    def test_update_state_collapsed(self, expected_state, mocker):
        # Arrange
        cell = Cell()
        logger = mocker.patch("loguru.logger.debug")

        # Act
        cell._collapsed = True
        actual = cell.update_state(expected_state)

        # Assert
        assert actual == "Tile_10"
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
    def test_update_state_random(self, mocker, random_option, complete_tile_list):
        # Arrange
        cell = Cell()
        choice = mocker.patch("numpy.random.choice")
        choice.return_value = random_option
        logger = mocker.patch("loguru.logger.debug")
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=complete_tile_list
        )

        # Act
        actual = cell.update_state(method="random")

        # Assert
        assert actual == random_option
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
    def test_update_state_new_state(self, new_state, mocker, complete_tile_list):
        # Arrange
        cell = Cell()
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=complete_tile_list
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
    def test_update_state_int_ok(self, state_index, new_state, mocker, complete_tile_list):
        # Arrange
        cell = Cell()
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=complete_tile_list
        )

        # Act
        result = cell.update_state(new_state=state_index)

        # Assert
        assert result == new_state

    @pytest.mark.parametrize("state_index", [
        -1, 7
    ])
    def test_update_state_int_out_of_bound(self, state_index, mocker, complete_tile_list):
        # Arrange
        cell = Cell()
        logger = mocker.patch("loguru.logger.debug")
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=complete_tile_list
        )

        # Act
        cell.update_state(new_state=state_index)

        # Assert
        logger.assert_called()

    @pytest.mark.repeat(3)
    def test_update_state_wrong_state(self, faker, mocker, complete_tile_list):
        # Arrange
        cell = Cell()
        logger = mocker.patch("loguru.logger.debug")
        mocker.patch(
            "src.cell.Tileset.tile_list",
            new_callable=mocker.PropertyMock,
            return_value=complete_tile_list
        )

        # Act
        cell.update_state(new_state=faker.word())

        # Assert
        logger.assert_called()

    def test_update_options_collapsed(self, faker):
        # Arrange
        cell = Cell()
        cell._collapsed = True
        options = [faker.word()
                   for _ in range(faker.random_digit_not_null())]

        # Act
        expected_options = cell._options
        actual = cell.update_options(keep_options=options)

        # Assert
        assert actual == expected_options

    @pytest.mark.parametrize("keep_options, expected_options", [
        (["Tile_0"], ["Tile_0"]),
        (["Tile_1"], ["Tile_1"]),
        (["Tile_2"], ["Tile_2"]),
        (["Tile_3"], ["Tile_3"]),
        (["Tile_4"], ["Tile_4"]),
        (["Tile_5"], ["Tile_5"]),
        (["Tile_6"], ["Tile_6"]),
    ])
    def test_update_options_valid(self, keep_options, expected_options):
        # Arrange
        cell = Cell()

        # Act
        actual = cell.update_options(keep_options=keep_options)

        # Assert
        assert actual == expected_options
