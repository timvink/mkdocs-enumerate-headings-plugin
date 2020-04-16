"""
Terminology:

Page: list of strings that make up a markdown page
Headings: OrderedDict with index in Page and string that are heading lines in a markdown page
section: number of a heading
chapter: first level of a section
"""

import re
from typing import List
from collections import OrderedDict


def headings(lines: List[str]) -> OrderedDict:
    """
    Findings lines that are markdown headings
    TODO: make sure empty headings are not counted like "#" or "# "
    
    Args:
        lines (list): List with lines (strings)
        
    Returns:
        headings (dict): line number (key) and line (str)
    """
    heading_lines = OrderedDict({})
    is_block = False
    n = 0
    while n < len(lines):
        if lines[n].startswith("```"):
            is_block = not is_block

        if not is_block and lines[n].startswith("#"):
            heading_lines[n] = lines[n]
        n += 1

    return heading_lines


def enumerate_headings(headings: OrderedDict) -> OrderedDict:
    """Adds heading numbers
    
    Example:
    
        headings = {
            1: '# test',
            2: '## test',
            3: '# test',
            4: '## test',
            5: '## test'
        }
        enumerate_headings(headings)
        #> {1: '# 1. test',
            2: '## 1.1 test',
            3: '# 2. test',
            4: '## 2.1 test',
            5: '## 2.2 test'}
    
    Args:
        headings (OrderedDict): Dict with line number: heading string
    
    Returns:
        OrderedDict: Updated headings dict
    """

    depths = [heading_depth(x) for x in headings.values()]

    h1 = heading_number(depths, heading_depth=1)
    h2 = heading_number(depths, heading_depth=2)
    h3 = heading_number(depths, heading_depth=3)
    h4 = heading_number(depths, heading_depth=4)
    h5 = heading_number(depths, heading_depth=5)
    h6 = heading_number(depths, heading_depth=6)

    h = list(map(list, zip(h1, h2, h3, h4, h5, h6)))
    h = [heading_string(x) for x in h]
    assert len(h) == len(depths)

    # insert heading number after markdown heading
    for i, key in zip(range(len(headings)), headings.keys()):
        headings[key] = insert_heading_number(headings[key], h[i])

    return headings


def heading_string(heading_number):
    """
    Example:
        heading_string([1, 0, 0, 0, 0, 0])
        #> "1."
        heading_string([2, 1, 0, 0, 0, 0])
        #> "2.1"
        # Skipped heading
        heading_string([2, 0, 1, 0, 0, 0])
        #> "2.1.1"
        # Missing h1
        heading_string([0, 1, 0, 0, 0, 0]) 
        #> "" or "0.1"
    
    """
    # Remove any trailing zeros
    while heading_number[-1] == 0:
        del heading_number[-1]

    # Deal with skipped heading levels
    # by replacing zeros with ones
    # heading_number = [1 if x == 0 else x for x in heading_number]

    # Join to string
    heading_string = [str(x) for x in heading_number]
    heading_string = ".".join(heading_string)

    # Add a trailing dot to level 1 headings
    # For example "1" should be "1."
    if "." not in heading_string:
        heading_string += "."

    return heading_string


def insert_heading_number(line: str, heading: str) -> str:
    """
    Inserts a heading number into a heading line
    
    Example:
    
        line = "## Example page"
        heading = "2.2"
        insert_heading_number(line, number)
        #> "## 2.2 Example page"
    
    Args:
        line (str): The heading line
        heading (str): The heading number
    
    Returns:
        str: the updated heading line
    """
    pattern = re.compile(r"(\#+) (.*)")
    matches = pattern.match(line)
    return "%s %s %s" % (matches.group(1), heading, matches.group(2))


def heading_number(depths: List[int], heading_depth: int) -> List[int]:
    """Determines for a heading level the current number
    
    This function contains the core algorithm for determining
    the heading level numbers.
    
    The main trick is that we look at each heading level separately
    and only combine afterwards.
    
    Example:
        depths = [1, 2, 1, 2, 2]
        heading_number(depths, heading_depth = 1)
        #> [1, 1, 2, 2, 2]
        heading_number(depths, heading_depth = 2)
        #> [0, 1, 0, 1, 2] 
    
    Args:
        depths (List[int]): The depths of the markdown heading (e.g. # is 1, ## is 2, etc)
        heading_depth ([type]): The heading level to determine the numbers for.
    
    Returns:
        List[int]: heading numbers
    """
    h = []
    for i, depth in enumerate(depths):
        if i == 0:
            h.append(int(depth == heading_depth))
        elif depth < heading_depth:
            h.append(0)
        elif depth == heading_depth:
            h.append(h[i - 1] + 1)
        else:
            h.append(h[i - 1])
    return h


def heading_depth(line: str) -> int:
    """
    Translates a markdown heading to a numeric heading
    
    Examples:
    
    '# heading' returns 1
    '### heading' returns 3
    
    Args:
        line (str): line in a markdown page
    """
    assert line.startswith("#")
    n = 0
    while line[n : n + 1] == "#":
        n += 1
    return n


def update_heading_chapter(line: str, chapter: int):
    """
    TODO DOCUMENT
    TODO write unit tests for this.
    
    Args:
        line (str): [description]
        chapter (int): [description]
    
    Returns:
        [type]: [description]
    """
    pattern = re.compile(r"(^[\#].+)(1)(\..+)")
    matches = pattern.match(line)
    if not matches:
        return line
    else:
        return "%s%s%s" % (matches.group(1), str(chapter), matches.group(3))
