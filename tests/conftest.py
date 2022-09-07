import pytest


@pytest.fixture(autouse=True)
def tileset_tile_list():
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
