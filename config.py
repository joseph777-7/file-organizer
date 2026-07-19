import json
from pathlib import Path


def load_categories():
    """Load categories from config.json."""
    config_path = Path(__file__).parent / "config.json"

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


FILE_CATEGORIES = load_categories()