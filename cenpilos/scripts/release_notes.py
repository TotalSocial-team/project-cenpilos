from typing import List
import os

release_notes = os.path.join(os.path.abspath(os.path.join("release_notes", os.pardir)))


def read_notes() -> List[List[str]]:
    """
    Reads the release note text file
    :return: a list of list containing:
        1. functional components
        2. partially functional components
        3. future features planned
    """

    with open(os.path.join(release_notes, "cenpilos", "release_notes", "release_notes.txt"), 'r') as notes:
        # splits the lines or splits the data at the \n character
        lines = notes.read().splitlines()

        # find the elements and save them in another list
        spaces = [i for i, line in enumerate(lines) if line == '']
        functional_end = spaces[0]
        partial_functional_end = spaces[1]

        functional = [lines[i] for i in range(0, functional_end)]

        partial_functional = [lines[i] for i in range(functional_end + 1, partial_functional_end)]

        new_features = [lines[i] for i in range(partial_functional_end + 1, len(lines))]

    return [functional, partial_functional, new_features]
