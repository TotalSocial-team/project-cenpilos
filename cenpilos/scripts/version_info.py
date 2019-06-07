from typing import List
import os
info = os.path.join(os.path.abspath(os.path.join("version_info", os.pardir)), 'cenpilos', 'version_info', 'info.txt')


def version_information() -> List[str]:
    """
    Reads the release note text file
    :return: a list of list containing:
        1. functional components
        2. partially functional components
        3. future features planned
    """

    with open(info, 'r') as notes:
        # splits the lines or splits the data at the \n character
        lines = notes.read().splitlines()

    return [lines[0], lines[1] , lines[2], lines[3]]
