from collections import defaultdict
import re
import requests
from io import TextIOWrapper
from typing import Generator
from pathlib import Path

file_path = str(Path(__file__).parent) + r"\requirements.txt"


def _parse_lines(_file: TextIOWrapper) -> list[str, str]:
    """
    Receives an open file wrapper and yields a list with package name
    and package version (if present). Uses an regex that matches:
    '==', '>=', '<=', '<', '>', '[', ']'.
    Reference for PEP508:
    https://www.python.org/dev/peps/pep-0508/
    """

    for _line in _file:
        _line = _line.strip()
        if _line:
            _parse_lines = re.split("==|<=|>=|>|<|\[|\]", _line)
            yield _parse_lines if len(_parse_lines) == 2 else (
                _parse_lines[0],
                "",
            )


def _parse_requirements_file(file_path: str) -> list[dict]:

    _default_data = list()

    with open(file_path, "r") as _file:
        while True:
            try:
                _package_name, _version = next(
                    _parse_lines(_file),
                )
                _default_data.append(dict(package_name=_package_name, version=_version))
            except StopIteration:
                return _default_data


def _is_out_of_date(current: str, latest: str) -> int:

    if current != "" or latest != "":
        current = tuple(current.split("."))
        latest = tuple(latest.split("."))

        if all(isinstance(n, int) for n in current) and all(
            isinstance(n, int) for n in latest
        ):
            return current < latest

    return False


def check_requirements_version(_packages: list) -> list[dict]:

    _default_data = list()

    for _package in _packages:
        response = requests.get(
            f"https://pypi.org/pypi/{_package.get('package_name', '')}/json"
        )
        _default_data.append(
            dict(
                packageName=_package.get("package_name", "n/a"),
                currentVersion=_package.get("version", "n/a"),
                latestVersion=response.json().get("info", {}).get("version", "n/a"),
                outOfDate=_is_out_of_date(
                    current=_package.get("version", "n/a"),
                    latest=response.json().get("info", {}).get("version", "n/a"),
                ),
            )
        )

    print(_default_data)


check_requirements_version(_parse_requirements_file(file_path=file_path))
