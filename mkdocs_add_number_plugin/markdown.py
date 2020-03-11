import re
from typing import List
from collections import OrderedDict

def headings(lines: List[str]):
    """Findings lines that are markdown headings 
    
    Args:
        lines (list): List with lines (strings)
        
    Returns:
        headings (dict): line number (key) and line (str)
    """
    heading_lines = OrderedDict({})
    is_block = False
    n = 0
    while n < len(lines):
        if lines[n].startswith('```'):
            is_block = not is_block

        if not is_block and lines[n].startswith('#'):
            heading_lines[n] = lines[n]
        n += 1
        
    return heading_lines
    
def heading_depth(line):
    """Returns depth of heading indent
    
    '# heading' returns 1
    '### heading' returns 3
    
    Args:
        line (str): line in a markdown page
    """
    assert line.startswith('#')
    n = 0
    while line[n:n + 1] == '#':
        n += 1

    return n

    
def update_heading_chapter(line: str, chapter: int):
    pattern = re.compile(r"(^[\#].+)(1)(\..+)")
    matches = pattern.match(line)
    if not matches:
        return line
    else:
        return "%s%s%s" % (
            matches.group(1),
            str(chapter),
            matches.group(3)
        )
