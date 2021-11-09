from pathlib import Path
from pprint import pprint
from req_tools import check_requirements_version

file_path = str(Path(__file__).parent) + r"\requirements.txt"

if __name__ == "__main__":

    pprint(check_requirements_version(file_path))
