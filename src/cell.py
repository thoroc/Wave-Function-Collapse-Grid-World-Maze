import numpy as np
from loguru import logger
from src.tile import Tiles


class Cell:
    """
    options - shows which states (from 0 to 6) are available for this cell
    collapsed - shows if the cell was collapsed, which means the state was defined
    state - shows which state was assigned to the cell (from 0 to 6), where
            10 means the state was not assigned yet
    """
    _collapsed: bool
    _state: str
    _entropy: int

    def __init__(self):
        self._options = [
            "Tile_0",
            "Tile_1",
            "Tile_2",
            "Tile_3",
            "Tile_4",
            "Tile_5",
            "Tile_6"
        ]
        self._collapsed = False
        self._state = "Tile_10"
        self._entropy = len(self._options)

    @property
    def state(self):
        return self._state

    @property
    def entropy(self):
        self._entropy = len(self._options)
        return self._entropy

    @property
    def collapsed(self):
        return self._collapsed

    @property
    def options(self):
        return self._options

    def update_state(self, new_state='Tile_0', method="direct"):

        if self._collapsed:
            logger.debug("The cell is already collapsed!")
            return

        if method == "random":
            new_state = np.random.choice(self._options)
            logger.debug("All options: {}", self._options)
            logger.debug("Random selection: {} ", new_state)

        temporal_tile_obj = Tiles()

        if new_state in temporal_tile_obj.list_of_tiles:
            self._state = new_state
        elif type(new_state) == int:
            if 0 <= new_state <= 6:
                self._state = temporal_tile_obj.list_of_tiles[new_state]
            else:
                logger.debug("Error. The state index is out of range (0,6)")
        else:
            logger.debug(
                "Error. Wrong state was given. Neither Tile name, nor Tile index")

        self._options = []
        self._entropy = 0
        self._collapsed = True
