"""Utils functions collection."""

import os
import csv
import json
import toml
import logging
from pathlib import Path
from typing import Optional


_logger = logging.getLogger(__name__)


def json_to_list(filepath: str) -> Optional[list[dict]]:
    """Read a JSON file to a List of dictionnaries."""
    data: Optional[list[dict]] = None
    if os.path.isfile(filepath):
        with open(filepath, mode="r", encoding="utf-8") as f:
            data = json.load(f)
    return data


def merge_list_dicts(list1: list[dict], list2: list[dict], remove_duplicates_on: str):
    """Merge two lists of dictionnaries."""
    merged_list = {d[remove_duplicates_on]: d for d in list1}
    for d in list2:
        merged_list.setdefault(d[remove_duplicates_on], {}).update(d)
    return list(merged_list.values())


def to_file(s: str, filepath: str):
    """Save string content into file."""
    if s is not None:
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(s)


def ensure_path(dirpath: str):
    """Ensure that directories path exists. Create it if not.

    Params
    ------
        dirpath (str): Directories path. e.g: foo/bar/

    Returns
    -------
        (str): dirpath
    """
    if not os.path.isdir(dirpath):
        try:
            os.makedirs(dirpath)
        except Exception as e:
            _logger.error("Unable to create path. Error: %s", e)
    return dirpath


def to_csv(data: list[dict], output_file: str, mode: Optional[str] = None):
    """Save list of dictionnaries to csv file.
    No effect if data is an empty array.
    """
    if len(data) == 0:
        return
    columns = data[0].keys()
    if mode is None:
        mode = "a" if os.path.isfile(output_file) else "w"

    with open(output_file, mode, encoding="utf-8", newline="") as f:
        dict_writer = csv.DictWriter(f, columns)
        if mode == "w":
            dict_writer.writeheader()
        dict_writer.writerows(data)


def version():
    """Get version from file."""
    project_dir = Path(__file__).parent.parent.parent
    config = toml.load(os.path.join(project_dir, "pyproject.toml"))
    return config["tool"]["poetry"]["version"]
