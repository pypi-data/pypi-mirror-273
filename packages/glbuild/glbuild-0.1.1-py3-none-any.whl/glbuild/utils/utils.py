"""Utils functions collection."""

import os
import csv
import json
from typing import Optional


def json_to_list(filepath: str) -> Optional[list[dict]]:
    """Read a JSON file to a List of dictionnaries."""
    data: list[dict] = None
    if os.path.isfile(filepath):
        with open(filepath) as f:
            data = json.load(f)
    return data


def merge_list_dicts(list1: list[dict], list2: list[dict], remove_duplicates_on: str):
    """Merge two lists of dictionnaries."""
    list1 = {d[remove_duplicates_on]: d for d in list1}
    for d in list2:
        list1.setdefault(d[remove_duplicates_on], dict()).update(d)
    return list(list1.values())


def to_file(s: str, filepath: str):
    """Save string content into file."""
    if s is not None:
        with open(filepath, "w") as file:
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
        except Exception:
            pass
    return dirpath


def to_csv(data: list[dict], output_file: str, mode: str = None):
    """Save list of dictionnaries to csv file.
    No effect if data is an empty array.
    """
    if len(data) == 0:
        return
    columns = data[0].keys()
    if mode is None:
        mode = "a" if os.path.isfile(output_file) else "w"

    with open(output_file, mode, newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, columns)
        if mode == "w":
            dict_writer.writeheader()
        dict_writer.writerows(data)
