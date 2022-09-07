import numpy as np


class Tileset:
    """
    tiles - stores all possible states of cells representing patterns of walls
            for Grid World
    title_probability - stores probability for each state to appear. It is a way to
                        adjust how many walls will be placed and which wall
                        structure would be prefered
    """

    def __init__(self):
        """
        List of all available tiles where Tile_0 ... Tile_6 are defined tiles
        and Tile_10 is a tile of undefined cells (which are not collapsed)
        """
        self._tile_list = [
            "Tile_0",
            "Tile_1",
            "Tile_2",
            "Tile_3",
            "Tile_4",
            "Tile_5",
            "Tile_6",
            "Tile_10"
        ]

        self._tiles = {
            "Tile_0": np.array(
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]
                ]
            ),
            "Tile_1": np.array(
                [
                    [0, 1, 0],
                    [0, 1, 1],
                    [0, 1, 0]
                ]
            ),
            "Tile_2": np.array(
                [
                    [0, 0, 0],
                    [1, 1, 1],
                    [0, 1, 0]
                ]
            ),
            "Tile_3": np.array(
                [
                    [0, 1, 0],
                    [1, 1, 0],
                    [0, 1, 0]
                ]
            ),
            "Tile_4": np.array(
                [
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]
                ]
            ),
            "Tile_5": np.array(
                [
                    [0, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]
                ]
            ),
            "Tile_6": np.array(
                [
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0]
                ]
            ),
            "Tile_10": np.array(
                [
                    [1, 1, 1],
                    [1, 1, 1],
                    [1, 1, 1]
                ]
            ),
        }

        self.tile_probability = [0] * 8
        self.tile_probability[0] = 26
        self.tile_probability[1] = 9
        self.tile_probability[2] = 9
        self.tile_probability[3] = 9
        self.tile_probability[4] = 9
        self.tile_probability[5] = 20
        self.tile_probability[6] = 20
        self.tile_probability[7] = 0

        """
        The dictionary that stores options for neighbours of each Tile.
        When a Tileset is assigned to a certain state, all neighbour options must
        be updated according to the rules stored here. Therefore, entropy is
        propagated among the cells.
        """
        self._connections = {
            "wall": {
                "UP": ["Tile_0", "Tile_4", "Tile_5"],
                "RIGHT": ["Tile_0", "Tile_1", "Tile_6"],
                "DOWN": ["Tile_0", "Tile_2", "Tile_5"],
                "LEFT": ["Tile_0", "Tile_3", "Tile_6"]
            },
            "path": {
                "UP": ["Tile_1", "Tile_2", "Tile_3", "Tile_6"],
                "RIGHT": ["Tile_2", "Tile_3", "Tile_4", "Tile_5"],
                "DOWN": ["Tile_1", "Tile_3", "Tile_4", "Tile_6"],
                "LEFT": ["Tile_1", "Tile_2", "Tile_4", "Tile_5"]
            }
        }

        self._connection_rules = {
            "Tile_0": {
                "UP": self._connections["wall"]["UP"],
                "RIGHT": self._connections["wall"]["RIGHT"],
                "DOWN": self._connections["wall"]["DOWN"],
                "LEFT": self._connections["wall"]["LEFT"]
            },
            "Tile_1": {
                "UP": self._connections["path"]["UP"],
                "RIGHT": self._connections["path"]["RIGHT"],
                "DOWN": self._connections["path"]["DOWN"],
                "LEFT": self._connections["wall"]["LEFT"]
            },
            "Tile_2": {
                "UP": self._connections["wall"]["UP"],
                "RIGHT": self._connections["path"]["RIGHT"],
                "DOWN": self._connections["path"]["DOWN"],
                "LEFT": self._connections["path"]["LEFT"]
            },
            "Tile_3": {
                "UP": self._connections["path"]["UP"],
                "RIGHT": self._connections["wall"]["RIGHT"],
                "DOWN": self._connections["path"]["DOWN"],
                "LEFT": self._connections["path"]["LEFT"]
            },
            "Tile_4": {
                "UP": self._connections["path"]["UP"],
                "RIGHT": self._connections["path"]["RIGHT"],
                "DOWN": self._connections["wall"]["DOWN"],
                "LEFT": self._connections["path"]["LEFT"]
            },
            "Tile_5": {
                "UP": self._connections["wall"]["UP"],
                "RIGHT": self._connections["path"]["RIGHT"],
                "DOWN": self._connections["wall"]["DOWN"],
                "LEFT": self._connections["path"]["LEFT"]
            },
            "Tile_6": {
                "UP": self._connections["path"]["UP"],
                "RIGHT": self._connections["wall"]["RIGHT"],
                "DOWN": self._connections["path"]["DOWN"],
                "LEFT": self._connections["wall"]["LEFT"]
            }
        }

    @property
    def tile_list(self):
        return self._tile_list

    @property
    def tiles(self):
        return self._tiles

    @property
    def connection_rules(self):
        return self._connection_rules
