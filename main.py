from pathlib import Path
from pprint import pprint
from req_tools import check_requirements_version

file_path = str(Path(__file__).parent) + r"\requirements.txt"

if __name__ == "__main__":

    print("Dock's Python Software Engineer technical test.")
    print("Made by: Vinicius Taborda \n")
    pprint(check_requirements_version(file_path), sort_dicts=False)
