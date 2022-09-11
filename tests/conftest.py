import pytest

from src.cell import Cell


@pytest.fixture(autouse=True)
def complete_tile_list():
    return [
        "Tile_0",
        "Tile_1",
        "Tile_2",
        "Tile_3",
        "Tile_4",
        "Tile_5",
        "Tile_6",
        "Tile_10"
    ]


@pytest.fixture(autouse=True)
def cell_with_low_entropy():
    return Cell(options=["Tile_0"])
