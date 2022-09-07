import numpy as np
from src.tileset import Tileset


class TestTileset:
    def test_constructor(self):
        # Arrange
        tileset = Tileset()

        # Act

        # Assert
        assert isinstance(tileset.tile_list, list)
        assert isinstance(tileset.tiles, dict)
        assert isinstance(tileset.connection_rules, dict)

    def test_tile_list(self):
        # Arrange
        tileset = Tileset()

        # Act

        # Assert
        assert tileset.tile_list == [
            "Tile_0",
            "Tile_1",
            "Tile_2",
            "Tile_3",
            "Tile_4",
            "Tile_5",
            "Tile_6",
            "Tile_10"
        ]

    def test_tiles(self):
        # Arrange
        tileset = Tileset()

        # Act

        # Assert
        assert (tileset.tiles["Tile_0"] == np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])).all()
        assert (tileset.tiles["Tile_1"] == np.array([
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0]
        ])).all()
        assert (tileset.tiles["Tile_2"] == np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ])).all()
        assert (tileset.tiles["Tile_3"] == np.array([
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 0]
        ])).all()
        assert (tileset.tiles["Tile_4"] == np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ])).all()
        assert (tileset.tiles["Tile_5"] == np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ])).all()
        assert (tileset.tiles["Tile_6"] == np.array([
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ])).all()
        assert (tileset.tiles["Tile_10"] == np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ])).all()

    def test_connection_rules(self):
        # Arrange
        tileset = Tileset()

        # Act

        # Assert
        assert tileset.connection_rules == {
            "Tile_0": {
                "UP": ["Tile_0", "Tile_4", "Tile_5"],
                "RIGHT": ["Tile_0", "Tile_1", "Tile_6"],
                "DOWN": ["Tile_0", "Tile_2", "Tile_5"],
                "LEFT": ["Tile_0", "Tile_3", "Tile_6"]
            },
            "Tile_1": {
                "UP": ["Tile_1", "Tile_2", "Tile_3", "Tile_6"],
                "RIGHT": ["Tile_2", "Tile_3", "Tile_4", "Tile_5"],
                "DOWN": ["Tile_1", "Tile_3", "Tile_4", "Tile_6"],
                "LEFT": ["Tile_0", "Tile_3", "Tile_6"]
            },
            "Tile_2": {
                "UP": ["Tile_0", "Tile_4", "Tile_5"],
                "RIGHT": ["Tile_2", "Tile_3", "Tile_4", "Tile_5"],
                "DOWN": ["Tile_1", "Tile_3", "Tile_4", "Tile_6"],
                "LEFT": ["Tile_1", "Tile_2", "Tile_4", "Tile_5"]
            },
            "Tile_3": {
                "UP": ["Tile_1", "Tile_2", "Tile_3", "Tile_6"],
                "RIGHT": ["Tile_0", "Tile_1", "Tile_6"],
                "DOWN": ["Tile_1", "Tile_3", "Tile_4", "Tile_6"],
                "LEFT": ["Tile_1", "Tile_2", "Tile_4", "Tile_5"]
            },
            "Tile_4": {
                "UP": ["Tile_1", "Tile_2", "Tile_3", "Tile_6"],
                "RIGHT": ["Tile_2", "Tile_3", "Tile_4", "Tile_5"],
                "DOWN": ["Tile_0", "Tile_2", "Tile_5"],
                "LEFT": ["Tile_1", "Tile_2", "Tile_4", "Tile_5"]
            },
            "Tile_5": {
                "UP": ["Tile_0", "Tile_4", "Tile_5"],
                "RIGHT": ["Tile_2", "Tile_3", "Tile_4", "Tile_5"],
                "DOWN": ["Tile_0", "Tile_2", "Tile_5"],
                "LEFT": ["Tile_1", "Tile_2", "Tile_4", "Tile_5"]
            },
            "Tile_6": {
                "UP": ["Tile_1", "Tile_2", "Tile_3", "Tile_6"],
                "RIGHT": ["Tile_0", "Tile_1", "Tile_6"],
                "DOWN": ["Tile_1", "Tile_3", "Tile_4", "Tile_6"],
                "LEFT": ["Tile_0", "Tile_3", "Tile_6"]
            }
        }
