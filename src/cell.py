from uuid import uuid4
import numpy as np
from loguru import logger
from src.tileset import Tileset


class Cell:
    """
    Class Cell.

    options - shows which states (from 0 to 6) are available for this cell
    collapsed - shows if the cell was collapsed, which means the state was defined
    state - shows which state was assigned to the cell (from 0 to 6), where
            10 means the state was not assigned yet
    """

    _id: str
    _collapsed: bool
    _state: str
    _entropy: int
    _row: int
    _column: int

    def __init__(self, options=None, row=None, column=None):
        """Class Cell constructor."""
        self._id = uuid4()

        self._options = options if options else [
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
        self._row = row
        self._column = column

    @property
    def id(self):
        return self._id

    @property
    def state(self):
        """State property."""
        return self._state

    @property
    def entropy(self):
        """Entropy property."""
        self._entropy = len(self._options)
        return self._entropy

    @property
    def collapsed(self):
        """Collapsed property."""
        return self._collapsed

    @property
    def options(self):
        """Options property."""
        return self._options

    @property
    def row(self):
        """Row property"""
        return self._row

    @property
    def column(self):
        """Column property"""
        return self._column

    @logger.catch()
    def update_state(self, new_state="Tile_0", method="direct"):
        """Update cell's state.

        Args:
            new_state (str, optional): state. Defaults to "Tile_0".
            method (str, optional): method. Defaults to "direct".

        Returns:
            str: the cell's state
        """
        if self._collapsed:
            logger.debug("The cell is already collapsed!")
            return self._state

        if method == "random":
            new_state = np.random.choice(self._options)
            logger.debug("All options: {}", self._options)
            logger.debug("Random selection: {} ", new_state)

        tileset = Tileset()

        if new_state in tileset.tile_list:
            self._state = new_state

        elif isinstance(new_state, int):
            if 0 <= new_state <= len(self._options) - 1:
                self._state = tileset.tile_list[new_state]
            else:
                logger.debug("Error. The state index is out of range (0,6)")
        else:
            logger.debug(
                "Error. Wrong state was given. Neither Tile name, nor Tile index")

        self._options = []
        self._entropy = 0
        self._collapsed = True

        return self._state

    def update_options(self, remove_options: list):
        """Update cell's options.

        Args:
            remove_options (list): list of options to remove for the cell

        Return:
            list: the current options for the cell
        """
        if self._collapsed:
            logger.debug(
                "This cell [{}] is already collapsed. Skipping",
                self
            )
            return self._options

        curr_options = self._options
        self._options = sorted(list(
            set(curr_options) - set(remove_options)
        ))

        logger.debug(
            "Cell [{}]. My new options: {}",
            self, self._options
        )

        return self._options

    def __repr__(self) -> str:
        return f"<{__name__}.{__class__.__name__} id={self._id} collapsed={self._collapsed} state={self._state} entropy={self._entropy}>"

    def __eq__(self, cell: object) -> bool:
        return self._id == cell.id
