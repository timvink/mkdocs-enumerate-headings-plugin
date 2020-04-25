from collections import OrderedDict
from typing import List


def flatten(nav):
    """
    Flattens mkdocs navigation to list of markdown files.
    
    Some navigations include a source page twice.
    So also deduplicate.
    
    See tests/test_flatten.py for example
    
    Args:
        nav (list): nested list with dicts
    
    Returns:
        list: list of markdown pages
    """
    pages = []
    for item in nav:
        if type(item) == dict:
            item = list(item.values())[0]
        if type(item) == list:
            pages += flatten(item)
        else:
            pages.append(item)
    return list(OrderedDict.fromkeys(pages))


def read_md(path: str):
    """
    Reads markdown files

    Args:
        path (str): path to markdown file
        
    Returns:
        List[str]: list of lines
    """
    p = open(path, encoding="utf-8").readlines()
    return [line.rstrip("\n") for line in p]


def chapter_numbers(n_chapters_per_page: List):

    # First chapter should always be 1
    # Even if there is no heading 1
    if n_chapters_per_page[0] == 0:
        n_chapters_per_page[0] = 1

    chapters = []
    for i, c in enumerate(n_chapters_per_page):
        if i == 0:
            chapters.append(min(c, 1))
        else:
            chapters.append(min(c, 1) + sum(n_chapters_per_page[:i]))
    return chapters
