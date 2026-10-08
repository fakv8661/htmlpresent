import os
from pathlib import Path

import logs

LOGI = logs.getLogger(__file__)

class PathError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    

PREVIEW_IMG = Path(__file__).resolve().parent.joinpath("presentation_asset/preview_img")
PRESENTATIONS = Path(__file__).resolve().parent.joinpath("templates/presentations")

PATH_LIST = [
    PREVIEW_IMG,
    PRESENTATIONS
]

def path_tests():
    for path in PATH_LIST:
        if not os.path.exists(path):
            os.makedirs(path)
            LOGI.error("Path not found. [%s]", path)
            raise PathError(f"Path not found. [{path}]")

    LOGI.info("[Path] All files are exists!")