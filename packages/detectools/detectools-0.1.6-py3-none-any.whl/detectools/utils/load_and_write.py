import json
from pathlib import Path
from typing import Any, Dict, Union

def load_json(json_path: Union[str, Path]) -> Dict[str, Any]:
    """Load JSON file into dict.

    Args:
        json_path (``Union[str, Path]``): Path to JSON.

    Returns:
        ``Dict[str, Any]``:
            - Json data as dict.
    """
    if isinstance(json_path, str):
        json_path = Path(json_path)

    return json.load(json_path.open())


def write_json(filename: str, dic: dict):
    """Write a dictionnary in json format

    Args:
        filename (``str``): Path to write JSON.
        dic (``dict``): Dictionnary to write in JSON format.
    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    Path(filename).write_text(json.dumps(dic))