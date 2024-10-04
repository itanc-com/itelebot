import logging
from pathlib import Path
import json


logger = logging.getLogger(__name__)
ROOT_DIR = Path(__file__).resolve().parent.parent
STATIC_PATH = Path("messages")

BASE_PATH = ROOT_DIR / STATIC_PATH


def load_messages(file_name: str):
    file_path = BASE_PATH / file_name
    print(f"--> {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"File {file_name} not found in {BASE_PATH}")
        return {}
