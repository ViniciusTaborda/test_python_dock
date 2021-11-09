import re
import requests
from io import TextIOWrapper
from packaging import version


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


def _is_out_of_date_external_pkg(current: str, latest: str) -> int:
    """
    Using the packaging module to compare string versions.
    Reference: https://stackoverflow.com/a/11887885
    """
    return version.parse(current) < version.parse(latest)


def _is_out_of_date_implemented(current: str, latest: str) -> int:
    """
    Creating tuple objects using the split function in the string to
    compare the values of the tuples.
    Reference:https://docs.python.org/3/reference/expressions.html#not-in
    """
    if current != "" and latest != "":
        current = tuple(map(int, (current.split("."))))
        latest = tuple(map(int, (latest.split("."))))
        return current < latest

    return False


def check_requirements_version(_file_path: str) -> list[dict]:
    """
    Opens a file in reading mode and iterates through the lines using `_parse_lines`.
    Inside the loop, gets the value from the pypi API and creates a constructs a dict.
    Reference: https://docs.python.org/3/library/functions.html#next
    """
    _default_data = list()
    with open(_file_path, "r") as _file:

        while True:
            try:
                _package_name, _version = next(_parse_lines(_file))
                response = requests.get(f"https://pypi.org/pypi/{_package_name}/json")

                if not response.status_code == 200:
                    return [dict]

                _default_data.append(
                    dict(
                        packageName=_package_name,
                        currentVersion=_version,
                        latestVersion=response.json()
                        .get("info", {})
                        .get("version", "n/a"),
                        outOfDate=_is_out_of_date_implemented(
                            current=_version,
                            latest=response.json()
                            .get("info", {})
                            .get("version", "n/a"),
                        ),
                    )
                )
            except StopIteration:
                return _default_data
