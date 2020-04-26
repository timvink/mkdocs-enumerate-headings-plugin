from typing import List


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
