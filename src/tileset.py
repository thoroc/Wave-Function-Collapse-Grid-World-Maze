from pathlib import Path
from requests import get
from loguru import logger

ARTS = {
    "edge": ["wang-2e", "pipe", "pipe2", "path"]
}


def tileset():
    base_url = "http://www.cr31.co.uk/stagecast/art"

    for type, styles in ARTS.items():
        for style in styles:
            download(base_url=base_url, type=type, style=style)


def download(base_url: str, type: str, style: str):
    logger.info("Downloading {} {}", type, style)
    for index in range(0, 15):
        response = get(f"{base_url}/{type}/{style}/{index}.gif")

        output_dir = Path(Path.cwd(), "tiles", type, style)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = Path(output_dir, f"{index}.gif")

        with output_file.open("wb") as file_handler:
            file_handler.write(response.content)
