import numpy as np
import matplotlib.pyplot as plt
from loguru import logger


class Tiles:
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
        self.list_of_tiles = ["Tile_0", "Tile_1", "Tile_2", "Tile_3", "Tile_4",
                              "Tile_5", "Tile_6", "Tile_10"]

        self.tiles = {
            "Tile_0": np.array([[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]]),

            "Tile_1": np.array([[0, 1, 0],
                                [0, 1, 1],
                                [0, 1, 0]]),

            "Tile_2": np.array([[0, 0, 0],
                                [1, 1, 1],
                                [0, 1, 0]]),

            "Tile_3": np.array([[0, 1, 0],
                                [1, 1, 0],
                                [0, 1, 0]]),

            "Tile_4": np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 0, 0]]),

            "Tile_5": np.array([[0, 0, 0],
                                [1, 1, 1],
                                [0, 0, 0]]),

            "Tile_6": np.array([[0, 1, 0],
                                [0, 1, 0],
                                [0, 1, 0]]),

            "Tile_10": np.array([[1, 1, 1],
                                 [1, 1, 1],
                                 [1, 1, 1]]),
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
        When a Tiles is assigned to a certain state, all neighbour options must
        be updated according to the rules stored here. Therefore, entropy is
        propagated among the cells.
        """
        self.connection = {
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

        self.connection_rules = {
            "Tile_0": {
                "UP": self.connection["wall"]["UP"],
                "RIGHT": self.connection["wall"]["RIGHT"],
                "DOWN": self.connection["wall"]["DOWN"],
                "LEFT": self.connection["wall"]["LEFT"]
            },
            "Tile_1": {
                "UP": self.connection["path"]["UP"],
                "RIGHT": self.connection["path"]["RIGHT"],
                "DOWN": self.connection["path"]["DOWN"],
                "LEFT": self.connection["wall"]["LEFT"]
            },
            "Tile_2": {
                "UP": self.connection["wall"]["UP"],
                "RIGHT": self.connection["path"]["RIGHT"],
                "DOWN": self.connection["path"]["DOWN"],
                "LEFT": self.connection["path"]["LEFT"]
            },
            "Tile_3": {
                "UP": self.connection["path"]["UP"],
                "RIGHT": self.connection["wall"]["RIGHT"],
                "DOWN": self.connection["path"]["DOWN"],
                "LEFT": self.connection["path"]["LEFT"]
            },
            "Tile_4": {
                "UP": self.connection["path"]["UP"],
                "RIGHT": self.connection["path"]["RIGHT"],
                "DOWN": self.connection["wall"]["DOWN"],
                "LEFT": self.connection["path"]["LEFT"]
            },
            "Tile_5": {
                "UP": self.connection["wall"]["UP"],
                "RIGHT": self.connection["path"]["RIGHT"],
                "DOWN": self.connection["wall"]["DOWN"],
                "LEFT": self.connection["path"]["LEFT"]
            },
            "Tile_6": {
                "UP": self.connection["path"]["UP"],
                "RIGHT": self.connection["wall"]["RIGHT"],
                "DOWN": self.connection["path"]["DOWN"],
                "LEFT": self.connection["wall"]["LEFT"]
            }
        }

    def draw_tiles(self):
        """
        Draws all Tiles and shows probability for each of them
        """

        counter = 1
        fig = plt.figure(figsize=(8, 8))
        fig.suptitle("Tiles", fontsize=16)

        for _, tile in self.tiles.items():
            ax = fig.add_subplot(3, 4, counter)
            ax.set_title("Tile_" + str(counter - 1))
            # ax.set_title("Prbability: " + str(self.tile_probability[counter-1]) + "%")
            plt.imshow(tile)
            counter = counter + 1
        plt.show()

    def get_tile(self, index):
        if index in self.list_of_tiles:
            return self.tiles[index]
        else:
            logger.debug("Error! Wrong index was given. Expexted index: Tile_x where \
      x is 0, 1, ..., 6")
