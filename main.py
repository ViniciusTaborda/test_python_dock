from pathlib import Path
from pprint import pprint
from req_tools import check_requirements_version

file_path = str(Path(__file__).parent) + r"\requirements.txt"

if __name__ == "__main__":
    """
    Made by: Vinicius Taborda
    """
    pprint(check_requirements_version(file_path), sort_dicts=False)
